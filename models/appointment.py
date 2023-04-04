from datetime import datetime
from models.db import db
from mongoengine import Document, ReferenceField, StringField, BooleanField
from models.customer import Customer
from models.service import Service
from models.nailtech import NailTech



class Appointment(Document):
    customer_id = db.ReferenceField(Customer, required=False)
    nail_tech_id = db.ReferenceField(NailTech, required=True)
    appt_date = db.DateField(required=True)
    appt_time = db.DateTimeField(required=True)
    service_id = db.ReferenceField(Service, required=True)
    status = db.StringField(required=True, choices=('booked', 'cancelled', 'completed'))
    creation_date = db.DateTimeField(default=datetime.now)
    modified_date = db.DateTimeField(default=datetime.now)
