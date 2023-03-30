from mongoengine import Document, EmailField, StringField, BooleanField
from datetime import datetime
from models.db import db

class User(db.Document):
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    is_customer = db.BooleanField(required=True)
    is_nail_tech = db.BooleanField(required=True)
    creation_date = db.DateTimeField(default=datetime.now)
    modified_date = db.DateTimeField(default=datetime.now)