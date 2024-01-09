from pydantic import BaseModel

class TaskBase(BaseModel):
    task_title:str
    task_description: str | None = None


class TaskCreate(TaskBase):
    pass

class Tasiscomplete(BaseModel):
    is_competed: bool

class Task(TaskBase):
    task_id: int
    owner_id : int
    is_competed: bool
    

    class Config:
        orm_mode = True

class TaskUpdate(TaskBase):
    pass

class TaskReturn(BaseModel):
    task_id: int
    task_title:str
    task_description: str | None = None
    is_competed: bool



class CusBase(BaseModel):
    cus_email_add: str


class CustomerCreate(CusBase):
    cus_password:str
    cus_first_name: str
    cus_last_name: str


class CustomerUpdate(CusBase):
    pass

class Customer(CusBase):
    cus_id: int
    tasks: list[Task] = []
    
    class Config:
        orm_mode = True

