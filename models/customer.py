from datetime import datetime
from models.db import db
from models.user import User

class Customer(db.Document):
    user_id = db.ReferenceField(User, required=False)
    name = db.StringField(required=True)
    appointments = db.ListField(db.ReferenceField('Appointment'))
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    creation_date = db.DateTimeField(default=datetime.now)
    modified_date = db.DateTimeField(default=datetime.now)
