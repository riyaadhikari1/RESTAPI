from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

from app.server.database import (
    add_student,
    delete_student,
    retrieve_student,
    retrieve_students,
    update_student,
)
from app.server.models.student import (
    ErrorResponseModel,
    ResponseModel,
    StudentSchema,
    UpdateStudentModel,
)

router = APIRouter()

@router.post("/", response_description="Add new student")
async def add_student_data(student: StudentSchema = Body(...)):
    student = jsonable_encoder(student)
    new_student = await add_student(student)
    return ResponseModel(new_student, "Student added successfully.")

@router.get("/", response_description="List all students")
async def get_students():
    students = await retrieve_students()
    if students:
        return ResponseModel(students, "Students data retrieved successfully")
    return ResponseModel([], "No students found.")

@router.get("/{id}", response_description="Get a student by ID")
async def get_student_data(id: str):
    try:
        student = await retrieve_student(id)
        if student:
            return ResponseModel(student, "Student data retrieved successfully")
        raise HTTPException(status_code=404, detail="Student not found")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid student ID format")

@router.put("/{id}", response_description="Update a student")
async def update_student_data(id: str, req: UpdateStudentModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated = await update_student(id, req)
    if updated:
        return ResponseModel(f"Student with ID {id} updated.", "Update successful.")
    raise HTTPException(status_code=404, detail="Student not found")

@router.delete("/{id}", response_description="Delete a student")
async def delete_student_data(id: str):
    deleted = await delete_student(id)
    if deleted:
        return ResponseModel(f"Student with ID {id} deleted.", "Deletion successful.")
    raise HTTPException(status_code=404, detail="Student not found")
