from pydantic import BaseModel
import uuid 

class ClassResponse(BaseModel):
    id: int
    class_number: int
    class_desc: str
    student_number: int

class ClassCreate(BaseModel):
    class_number: int
    class_desc: str
    student_number: int
    
