from datetime import datetime
from models.db import db
from models.user import User

class Customer(db.Document):
    user_id = db.ReferenceField(User, required=True)
    name = db.StringField(required=True)
    appointments = db.ListField(db.ReferenceField('Appointment'))
    creation_date = db.DateTimeField(default=datetime.now)
    modified_date = db.DateTimeField(default=datetime.now)
