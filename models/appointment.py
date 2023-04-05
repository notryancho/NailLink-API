from datetime import datetime, time
from mongoengine import Document, StringField, DateTimeField, ReferenceField, DateField
from models.customer import Customer
from models.nailtech import NailTech
from models.service import Service

class Appointment(Document):
    customer_id = ReferenceField(Customer, required=False)
    nail_tech_id = ReferenceField(NailTech, required=False)
    appt_date = DateField(required=True)
    appt_time = StringField(required=True)
    service_id = ReferenceField(Service, required=True)
    status = StringField(required=False, choices=('booked', 'cancelled', 'completed'))
    creation_date = DateTimeField(default=datetime.now)
    modified_date = DateTimeField(default=datetime.now)

    # def clean(self):
    #     super(Appointment, self).clean()
    #     if self.appt_time is not None:
    #         if isinstance(self.appt_time, time):
    #             self.appt_time = self.appt_time.strftime('%H:%M:%S')
    #         else:
    #             raise ValueError('Invalid appointment time format')

    meta = {
        'indexes': [
            {'fields': ['customer_id', 'nail_tech_id', 'appt_date', 'appt_time'], 'unique': True}
        ]
    }
