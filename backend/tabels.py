from __future__ import annotations
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from flask_sqlalchemy import SQLAlchemy
import os

from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy import text

from typing import Optional

class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)

# Secondary tale for user and roles many to many storage
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', ForeignKey('user.id')),
    Column('role_id', ForeignKey('role.id'))
)

# Role table
class Role(db.Model):
    __tablename__ = 'role'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]

    users: Mapped[list[User]] = relationship(secondary=user_roles, back_populates="roles")
    def __repr__(self):
       return f"Role({self.name})"
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

# User table
class User(db.Model):
    __tablename__ = 'user'

    roles: Mapped[list[Role]] = relationship(secondary=user_roles, back_populates="users")
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column()
    phone: Mapped[str] = mapped_column()
    address: Mapped[str] = mapped_column()
    pincode: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default= datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(onupdate= datetime.utcnow, nullable=True)
    doc_loc: Mapped[str] = mapped_column(default=None, nullable=True)

    service_id: Mapped[Optional[int]] = mapped_column(ForeignKey('service.id'), default=None, nullable=True)
    service: Mapped[Optional[Service]] = relationship('Service', back_populates="users")
    

    service_request_as_customer: Mapped[list[ServiceRequest]] = relationship('ServiceRequest', foreign_keys='ServiceRequest.customer_id', back_populates='customer')
    service_request_as_professional: Mapped[list[ServiceRequest]] = relationship('ServiceRequest', foreign_keys='ServiceRequest.professional_id', back_populates='professional')

    def __repr__(self):
        return f"User({self.name}, {self.email}, {self.roles}, {self.created_at}, {self.updated_at})"
    def to_dict(self):
        # print("----------", self.name, self.service_id)
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'pincode': self.pincode,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'doc_loc': self.doc_loc,
            'roles': [role.to_dict() for role in self.roles],
            'service': self.service.name if self.service else None,
            'service_id': self.service_id,
            # 'new_service_id': -1 if not (self.service and self.service.id) else None
        }

# Service table
class Service(db.Model):
    __tablename__ = 'service'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
    time_required: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default= datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(onupdate= datetime.utcnow, nullable=True)

    users: Mapped[list[User]] = relationship('User', back_populates="service")

    requests: Mapped[list['ServiceRequest']] = relationship('ServiceRequest', back_populates='service')

    def __repr__(self):
        return f"Service(name={self.name}, price={self.price}, time_required={self.time_required}, \
        description={self.description}, created_at={self.created_at}, updated_at={self.updated_at})"
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'time_required': self.time_required,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'users': [u.to_dict() for u in self.users]
        }

# ServiceRequest table
class ServiceRequest(db.Model):
    __tablename__ = 'service_request'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    service_id: Mapped[int] = mapped_column(ForeignKey('service.id'), nullable=True)
    service: Mapped[Service] = relationship('Service', back_populates='requests')

    customer_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=True)
    customer: Mapped[User] = relationship('User', foreign_keys=[customer_id], back_populates='service_request_as_customer')

    professional_id: Mapped[Optional[int]] = mapped_column(ForeignKey('user.id'), nullable=True)
    professional: Mapped[Optional[User]] = relationship('User', foreign_keys=[professional_id], back_populates='service_request_as_professional')


    needed_at: Mapped[datetime] = mapped_column(nullable=False)
    requirement_message: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(default="requested", nullable=False)
    customer_feedback: Mapped[str] = mapped_column(nullable=True)
    professional_feedback: Mapped[str] = mapped_column(nullable=True)
    rating: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default= datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(onupdate= datetime.utcnow, nullable=True)

    def __repr__(self):
        return f"ServiceRequest(service_id={self.service_id}, customer_id={self.customer_id}, \
        professional_id={self.professional_id}, needed_at={self.needed_at}, status={self.status}, \
        created_at={self.created_at}, updated_at={self.updated_at})"
    def to_dict(self):
        return {
            'id': self.id,
            'service': self.service.to_dict(),
            'customer': self.customer.to_dict(),
            'professional': self.professional.to_dict() if self.professional else None,
            'needed_at': self.needed_at,
            'requirement_message': self.requirement_message,
            'status': self.status,
            'customer_feedback': self.customer_feedback,
            'professional_feedback': self.professional_feedback,
            'rating': self.rating,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'service': self.service.to_dict(),
        }

# initial data setup for demonstration
def setup_data():
    if Role.query.count() == 0:
        for role_name in ['Admin', 'Professional', 'Customer']:
            role = Role(name=role_name)
            db.session.add(role)
        db.session.commit()
        
        admin_user = User(
            name="Admin",
            email="admin@gmail.com",
            password = generate_password_hash("aaaaaa"),
            phone = "1234567890",
            address = "Bengaluru",
            pincode = "556677",
            is_active = True,
            roles=[Role.query.filter_by(name='Admin').first(), Role.query.filter_by(name='Customer').first()]
        )
        db.session.add(admin_user); db.session.commit()

        names = ['Charan', 'Chandan', 'Chandini']
        addresses = ['Kalkunte', 'Huskur', 'Nelamangala']
        pincodes = ['560067', '550099', '562123']
        for i in range(3):
            cusotmer_user = User(
                name=names[i],
                email=f"{names[i].lower()}@gmail.com",
                password = generate_password_hash('cccccc'),
                phone = "9999999999",
                address = addresses[i],
                pincode = pincodes[i],
                is_active = True,
                roles=[Role.query.filter_by(name='Customer').first()]
            )
            db.session.add(cusotmer_user); db.session.commit()
        service_names = ['House Cleaning', 'Plumbing', 'Appliance Repairing', 'Pest Control', 'Haircut & Styling'] 
        service_description = ['Kitchen Cleaning, Bathroom Cleaning, Living Room & Common Areas Cleaning, Bedroom Cleaning, Window Cleaning',
        "Leak Repair, Drain Cleaning, Pipe Installation, Water Heater Services, Fixture Replacement",
        "Refrigerator Repair, Washer Repair, Oven Repair, Dishwasher Repair, Microwave Repair",
        "Ant Treatment, Roach Treatment, Rodent Control, Termite Treatment, Bed Bug Treatment",
        "Women’s Cuts, Men’s Cuts, Coloring, Blowouts, Special Occasion Styling"
        ] 
        for i in range(5):
            service = Service(
                name = service_names[i],
                price = 500,
                time_required = 2,
                description = service_description[i]
            )
            db.session.add(service); db.session.commit()

        service_professionals = {
            'Praveen': {'service': service_names[0] , 'address': addresses[0], 'pincode': pincodes[0], 'phone': '1122334455'},
            'Pavan': {'service': service_names[1], 'address': addresses[1], 'pincode': pincodes[1], 'phone': '9988776655'},
            'Prashant': {'service': service_names[2], 'address': addresses[0], 'pincode': pincodes[0], 'phone': '2233114455'},
            'Priya': {'service': service_names[3], 'address': addresses[1], 'pincode': pincodes[1], 'phone': '9977886655'},
            'Pandu': {'service': service_names[4], 'address': addresses[2], 'pincode': pincodes[2], 'phone': '1133557799'},
            'Pranav': {'service': service_names[0], 'address': addresses[2], 'pincode': pincodes[2], 'phone': '5566447799'}
        }
        for name, sap in service_professionals.items():
            professional_user = User(   
                name=name,
                email=f"{name.lower()}@gmail.com",
                password = generate_password_hash("pppppp"),
                phone = sap['phone'],
                address = sap['address'],
                pincode = sap['pincode'],
                is_active = True,
                doc_loc = 'https://drive.google.com/file/d/1yaLYCJv3I9jw3FbuEgxQMJRTRkW5sna5/view?usp=sharing',
                roles = [Role.query.filter_by(name='Professional').first(), Role.query.filter_by(name='Customer').first()],
                service = Service.query.filter_by(name=sap['service']).first()
            )
            db.session.add(professional_user); db.session.commit()

#   <div class="mb-3">
#                     <strong>Account Created at</strong>
#                     <p>{{ user.created_at.date().strftime('%d-%b-%Y') }} {{ user.created_at.time().strftime('%H:%M') }}
#                         UTC</p>
#                 </div>

#                 <div class="mb-3">
#                     <strong>Account Updated at</strong>
#                     {% if user.updated_at %}
#                     <p>{{ user.updated_at.date().strftime('%d-%b-%Y') }} {{ user.updated_at.time().strftime('%H:%M') }}
#                         UTC</p>
#                     {% else %}
#                     <p>Never Updated</p>
#                     {% endif %}
#                 </div>

