from sqlalchemy.orm import Session

from . import models, schemas
import pdb
    
def create_customer(db: Session, customer: schemas.CustomerCreate):
    fake_hashed_password = customer.cus_password + "notreallyhashed"
    db_customer = models.Customer(
        cus_first_name = customer.cus_first_name,
        cus_last_name = customer.cus_last_name,
        cus_email_add=customer.cus_email_add,
        hashed_password=fake_hashed_password
        )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def create_customer_task(db: Session, task: schemas.TaskCreate, cus_id: int):
    db_task = models.Task(**task.model_dump(), owner_id=cus_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_customer_email(db: Session, email: str):
    return db.query(models.Customer).filter(models.Customer.cus_email_add == email).first()

def get_customer(db: Session, cus_id: str):
    return db.query(models.Customer).filter(models.Customer.cus_id == cus_id).first()

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()

def get_tasks(db: Session, cus_id: str):
    return db.query(models.Task).filter(models.Task.owner_id == cus_id)


def update_task(db: Session, task_id: int, task_data: schemas.TaskUpdate):
    db_task = db.query(models.Task).filter(models.Task.task_id == task_id).first()
    if db_task:
        for key, value in task_data.model_dump(exclude_none=True).items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task


def update_iscomplete(db: Session, task_id: int, task_data: schemas.Tasiscomplete):
    db_task = db.query(models.Task).filter(models.Task.task_id == task_id).first()
    if db_task:
        for key, value in task_data.model_dump(exclude_none=True).items():
            setattr(db_task, key, value)
            pdb.set_trace()
        db.commit()
        db.refresh(db_task)
    return db_task


def delete_customer(db: Session, id: int):
    # Retrieve the customer from the database based on the customer_id
    db_customer = db.query(models.Customer).filter(models.Customer.cus_id == id).first()
    db_task = db.query(models.Task).filter(models.Task.owner_id == id).all()
    # Check if the customer exists    
    if db_customer:
        if db_task:
            for i in db_task:
                db.delete(i)
        # Delete the customer from the database
        db.delete(db_customer)
        # Commit the deletion to the database
        db.commit()
    # Return the deleted customer
    return db_customer