from mongoengine import Document, EmailField, StringField, BooleanField
from datetime import datetime
from models.db import db

class User(db.Document):
    name = db.StringField(required = True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    is_customer = db.BooleanField(required=True, default=False)
    is_nail_tech = db.BooleanField(required=True, default=False)
    creation_date = db.DateTimeField(default=datetime.now)
    modified_date = db.DateTimeField(default=datetime.now)
    
 