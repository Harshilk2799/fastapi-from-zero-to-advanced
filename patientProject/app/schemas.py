from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class PatientCreate(BaseModel):
    name: str 
    age: int 
    gender: str 
    contact_number: str 
    diagnosis: str 
    doctor_assigned: str 

class PatientUpdate(BaseModel):
    name: str | None = None 
    age: int | None = None 
    gender: str | None = None 
    contact_number: str | None = None 
    diagnosis: str | None = None 
    doctor_assigned: str | None = None

class PatientOut(BaseModel):
    id: int 
    name: str 
    age: int 
    gender: str 
    contact_number: str 
    diagnosis: str 
    doctor_assigned: str 
    admitted_at: datetime 

    model_config = ConfigDict(from_attributes=True)

class StaffCreate(BaseModel):
    email: str 
    password: str = Field(min_length=8, max_length=72)

class Token(BaseModel):
    access_token: str 
    token_type: str = "bearer"
