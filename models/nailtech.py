from datetime import datetime
from models.db import db
from models.user import User

class NailTech(db.Document):
    user_id = db.ReferenceField(User, required=True)
    service = db.ListField(db.ReferenceField('Service'))
    name = db.StringField(required=True)
    phone = db.IntField(required=True)
    bio = db.StringField(required=True)
    profile_pic = db.StringField(required=True)
    appointments = db.ListField(db.ReferenceField('Appointment'))
    reviews = db.ListField(db.ReferenceField('Review'))
    creation_date = db.DateTimeField(default=datetime.now)
    modified_date = db.DateTimeField(default=datetime.now)