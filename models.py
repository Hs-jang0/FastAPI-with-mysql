from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Customer(Base):
    __tablename__ = "customers"

    cus_id = Column(String(100), primary_key=True, default=generate_uuid)
    cus_email_add = Column(String(255), unique=True, index=True)
    cus_first_name = Column(String(255), index=True)
    cus_last_name = Column(String(255), index=True)

    hashed_password = Column(String(255))

    tasks = relationship("Task", back_populates="owner")


class Task(Base):
    __tablename__ = "tasks"

    task_id= Column(String(100), primary_key=True, default=generate_uuid)
    task_title = Column(String(255), index=True)
    task_description=  Column(String(255), index=True)
    owner_id = Column(String(100), ForeignKey("customers.cus_id"))
    is_competed = Column(Boolean, default=False)

    owner = relationship("Customer", back_populates="tasks")

    