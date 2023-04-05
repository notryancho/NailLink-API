from mongoengine import Document, EmailField, StringField, BooleanField
from datetime import datetime
from models.db import db

class User(db.Document):
    name = db.StringField()
    email = db.EmailField(unique=True)
    password = db.StringField()
    is_customer = db.BooleanField(default=False)
    is_nail_tech = db.BooleanField(default=False)
    creation_date = db.DateTimeField(default=datetime.now)
    modified_date = db.DateTimeField(default=datetime.now)
    
 