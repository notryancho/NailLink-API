from datetime import datetime
from models.db import db


class Service(db.Document):
    name = db.StringField(required=True)
    description = db.StringField(required=True)
    price = db.FloatField(required=True)
    creation_date = db.DateTimeField(default=datetime.now)
    modified_date = db.DateTimeField(default=datetime.now)