#!/usr/bin/env python

import os
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

from models import Message
import settings

class Index(webapp.RequestHandler):
    def get(self):
        output = memcache.get("index")
        if output is None:
            messages = Message.all()
            messages.order('-date')
            # prepare the context for the template
            context = {
                'messages': messages,
                'debug': settings.DEBUG,
            }
            # calculate the template path
            path = os.path.join(os.path.dirname(__file__), 'templates',
                'index.html')
            # render the template with the provided context
            output = template.render(path, context)
            memcache.add("index", output, settings.CACHE_TIME)
        self.response.out.write(output)
                
class IMified(webapp.RequestHandler):
    def post(self):
        userkey = self.request.get('userkey')
        network = self.request.get('network')
        msg = self.request.get('msg')
        step = self.request.get('step')
                     
        try:
            message = Message(
                userkey = userkey,
                network = network,
                msg = msg,
                step = int(step)
            )   
            message.put()
            memcache.delete("index")
            logging.info("Saved new message")
            self.response.out.write('Message saved')
        except:
            logging.error("Error occured creating new message")
            self.response.out.write('An error ocured, message not saved')
                        
# wire up the views
application = webapp.WSGIApplication([
    ('/', Index),
    ('/endpoint', IMified),
], debug=True)

def main():
    "Run the application"
    run_wsgi_app(application)

if __name__ == '__main__':
    main()