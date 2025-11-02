from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class StudentSchema(BaseModel):
    fullname: str = Field(..., min_length=1)
    email: EmailStr = Field(...)
    course_of_study: str = Field(..., min_length=1)
    year: int = Field(..., gt=0, lt=9)
    gpa: float = Field(..., ge=0.0, le=4.0)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "course_of_study": "Water Resources Engineering",
                "year": 2,
                "gpa": 3.0,
            }
        }


class UpdateStudentModel(BaseModel):
    fullname: Optional[str] = Field(None, min_length=1)
    email: Optional[EmailStr] = None
    course_of_study: Optional[str] = Field(None, min_length=1)
    year: Optional[int] = Field(None, gt=0, lt=9)
    gpa: Optional[float] = Field(None, ge=0.0, le=4.0)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "course_of_study": "Water Resources & Environmental Engineering",
                "year": 4,
                "gpa": 4.0,
            }
        }


def ResponseModel(data, message):
    
    return {
        "data": data,
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
   
    return {
        "error": error,
        "code": code,
        "message": message
    }
