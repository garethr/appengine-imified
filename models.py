from google.appengine.ext import db
from google.appengine.api.users import User

class Message(db.Model):
    "Represents an IM message from the IMified service"
    userkey = db.StringProperty(required=True)
    network = db.StringProperty(required=True)
    msg = db.StringProperty(required=True)
    step = db.IntegerProperty(required=True)
    # we store the date automatically so we can filter the list
    # but this isn't provided by the callback
    date = db.DateTimeProperty(auto_now_add=True)