from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Annotated
from bson import ObjectId
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]

class StudentModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str 
    email: str 
    course: str 
    age: int 

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

class UpdateStudentModel(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    course: Optional[str] = None
    age: Optional[int] = None