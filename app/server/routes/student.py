from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

from app.server.models.student import (
    StudentSchema,
    UpdateStudentModel,
    ResponseModel,
    ErrorResponseModel,
)
from app.server.database import (
    add_student,
    retrieve_students,
    retrieve_student,
    update_student,
    delete_student,
)

router = APIRouter()


@router.post("/", response_description="Add new student")
async def add_student_data(student: StudentSchema = Body(...)):
    student_data = jsonable_encoder(student)
    new_student = await add_student(student_data)
    return ResponseModel(new_student, "Student added successfully.")


@router.get("/", response_description="List all students")
async def get_students():
    students = await retrieve_students()
    return ResponseModel(students, "Students data retrieved successfully")


@router.get("/{id}", response_description="Get a student by ID")
async def get_student_data(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid student ID format")
    student = await retrieve_student(id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return ResponseModel(student, "Student data retrieved successfully")


@router.put("/{id}", response_description="Update a student")
async def update_student_data(id: str, req: UpdateStudentModel = Body(...)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid student ID format")
    update_data = {k: v for k, v in req.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No update fields provided")
    updated = await update_student(id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Student not found")
    return ResponseModel(f"Student with ID {id} updated.", "Update successful.")


@router.delete("/{id}", response_description="Delete a student")
async def delete_student_data(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid student ID format")
    deleted = await delete_student(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
    return ResponseModel(f"Student with ID {id} deleted.", "Deletion successful.")
