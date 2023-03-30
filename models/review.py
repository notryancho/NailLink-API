from datetime import datetime
from models.db import db
from models.nailtech import NailTech
from models.customer import Customer


class Review(db.Document):
    nail_tech_id = db.ReferenceField(NailTech, required=True)
    customer_id = db.ReferenceField(Customer, required=True)
    rating = db.IntField(required=True, min_value=1, max_value=5)
    comment = db.StringField()
    creation_date = db.DateTimeField(default=datetime.now)
    modified_date = db.DateTimeField(default=datetime.now)