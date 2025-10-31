import motor.motor_asyncio
from bson.objectid import ObjectId

from decouple import config

MONGO_DETAILS = config("MONGO_DETAILS")  # read from .env
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.students
student_collection = database.get_collection("students_collection")


# Helper
def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "fullname": student["fullname"],
        "email": student["email"],
        "course_of_study": student["course_of_study"],
        "year": student["year"],
        "gpa": student["gpa"],
    }

# CRUD Operations
async def retrieve_students():
    students = []
    async for student in student_collection.find():
        students.append(student_helper(student))
    return students

async def add_student(student_data: dict) -> dict:
    student = await student_collection.insert_one(student_data)
    new_student = await student_collection.find_one({"_id": student.inserted_id})
    return student_helper(new_student)

async def retrieve_student(id: str) -> dict:
    try:
        student = await student_collection.find_one({"_id": ObjectId(id)})
        if student:
            return student_helper(student)
    except Exception:
        return None

async def update_student(id: str, data: dict):
    if not data:
        return False
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        updated_student = await student_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        return updated_student.modified_count > 0
    return False

async def delete_student(id: str):
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        await student_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False
