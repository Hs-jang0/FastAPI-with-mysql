from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/Customers/", response_model=schemas.Customer)
def create_user(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_user = crud.get_customer_email(db, email=customer.cus_email_add)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_customer(db=db, customer=customer)


@app.post("/Customers/{cus_id}/tasks/", response_model=schemas.Task)
def create_item_for_Customers(
    cus_id: str, task: schemas.TaskCreate, db: Session = Depends(get_db)
):
    return crud.create_customer_task(db=db, task=task, cus_id=cus_id)



@app.get("/Customers/{Cus_id}", response_model=schemas.Customer)
def read_user(cus_id: str, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, cus_id=cus_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_customer


@app.get("/Customers/", response_model=list[schemas.Customer])
def read_Customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = crud.get_customers(db, skip=skip, limit=limit)
    return customers



@app.get("/Task/{Cus_id}", response_model=list[schemas.TaskReturn])
def get_customer_tasks(cus_id: str,  db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db, cus_id=cus_id)
    return tasks

@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: str, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud.update_task(db=db, task_id=task_id, task_data=task_update)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.put("/tasks/{task_id}/is_complete", response_model=schemas.Task)
def update_task(task_id: str, task_update: schemas.Tasiscomplete, db: Session = Depends(get_db)):
    db_task = crud.update_task(db=db, task_id=task_id, task_data=task_update)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.patch("/tasks/{task_id}/", response_model=schemas.TaskUpdate)
def update_task(task_id: str, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud.update_task(db=db, task_id=task_id, task_data=task_update)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.delete("/customers/{cus_id}", response_model=schemas.Customer)
def delete_customer(cus_id: str, db: Session = Depends(get_db)):
    db_customer = crud.delete_customer(db=db, id=cus_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer