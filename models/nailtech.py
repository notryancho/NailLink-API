from datetime import datetime
from models.db import db
from models.user import User

class NailTech(db.Document):
    user_id = db.ReferenceField(User, required=False)
    service = db.ListField(db.ReferenceField('Service'))
    name = db.StringField(required=True)
    email = db.EmailField(required=True)
    password = db.StringField(required=True)
    phone = db.IntField(required=False)
    bio = db.StringField(required=False)
    profile_pic = db.StringField(required=False)
    appointments = db.ListField(db.ReferenceField('Appointment'))
    reviews = db.ListField(db.ReferenceField('Review'))
    creation_date = db.DateTimeField(default=datetime.now)
    modified_date = db.DateTimeField(default=datetime.now)
