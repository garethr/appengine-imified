from google.appengine.ext import db
from google.appengine.api.users import User

class Message(db.Model):
    userkey = db.StringProperty(required=True)
    network = db.StringProperty(required=True)
    msg = db.StringProperty(required=True)
    step = db.IntegerProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)