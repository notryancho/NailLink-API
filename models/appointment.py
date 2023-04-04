from datetime import datetime
from models.db import db
from mongoengine import Document, ReferenceField, StringField, BooleanField
from models.customer import Customer
from models.service import Service
from models.nailtech import NailTech
from models.user import User
from mongoengine.fields import DateField, DateTimeField, ReferenceField, StringField, BooleanField, DateTimeField


class Appointment(Document):
    customer_id = ReferenceField(Customer, required=False)
    nail_tech_id = ReferenceField(NailTech, required=False)
    appt_date = DateField(required=True)
    appt_time = StringField(required=True)
    service_id = ReferenceField(Service, required=True)
    status = StringField(required=False, choices=('booked', 'cancelled', 'completed'))
    creation_date = DateTimeField(default=datetime.now)
    modified_date = DateTimeField(default=datetime.now)

    def clean(self):
        super(Appointment, self).clean()
        if self.appt_time is not None:
            self.appt_time = datetime.strptime(self.appt_time, '%H:%M:%S').time()

    meta = {
        'indexes': [
            {'fields': ['customer_id', 'nail_tech_id', 'appt_date', 'appt_time'], 'unique': True}
        ]
    }












