from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.database import student_collection
from app.models import StudentModel, UpdateStudentModel

router = APIRouter(prefix="/students", tags=["Student"])

@router.post("/", response_model=StudentModel, status_code=status.HTTP_201_CREATED)
async def create_student(student: StudentModel):
    student_dict = student.model_dump(by_alias=True, exclude=["id"])
    new_student = await student_collection.insert_one(student_dict)
    created_student = await student_collection.find_one({"_id": new_student.inserted_id})
    return created_student

@router.get("/", response_model=list[StudentModel])
async def list_students():
    students = await student_collection.find().to_list(1000)
    return students 

@router.get("/{student_id}", response_model=StudentModel)
async def get_student(student_id: str):
    if not ObjectId.is_valid(student_id):
        raise HTTPException(status_code=400, detail="Invalid student ID")
    
    student = await student_collection.find_one({"_id": ObjectId(student_id)})
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found!")
    return student 


@router.patch("/{student_id}", response_model=StudentModel)
async def update_student(student_id: str, student: UpdateStudentModel):
    if not ObjectId.is_valid(student_id):
        raise HTTPException(status_code=400, detail="Invalid student ID")

    update_data = {k: v for k, v in student.model_dump(exclude_unset=True).items()}

    if len(update_data) >= 1:
        result = await student_collection.update_one(
            {"_id": ObjectId(student_id)}, {"$set": update_data}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")

    updated_student = await student_collection.find_one({"_id": ObjectId(student_id)})
    return updated_student

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: str):
    if not ObjectId.is_valid(student_id):
        raise HTTPException(status_code=400, detail="Invalid student ID")

    result = await student_collection.delete_one({"_id": ObjectId(student_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return None