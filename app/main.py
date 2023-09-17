from typing import Union
from fastapi import FastAPI
from uuid import UUID, uuid1
from app.models.Student import Student, CreateStudent

app = FastAPI()

students = {}

@app.get("/students")
def list_all_students():
    return students.items()

@app.get("/students/{student_name}")
def list_student(student_name: str):
    if students.get(student_name):
        return students.get(student_name)
    
    return {'message': 'Não encontrado'}

@app.post("/students/")
def create_student(student: Student):
    if student:
        new_id = uuid1()
        new_student = CreateStudent(id=new_id, name=student.name, email=student.email, course=student.course, period=student.period,age=student.age)
        students[student.name] = new_student
        return {'message': 'Estudante criado com sucesso!', 'student': new_student}
    
    return {}

@app.put("/students/{student_name}")
def update_student(student_name: str, data: Student):
    if student_name and data:
        updated_student = CreateStudent(id=uuid1(), name=data.name, email=data.email, course=data.course, period=data.period, age=data.age)
        students[student_name] = updated_student
        return {'message': 'Estudante atualizado com sucesso!','student': updated_student}
    
    return {}

@app.delete("/students/{student_id}")
def remove_student(student_id: str):
    print(student_id, students, students[student_id])
    if student_id in students:
        del students[student_id]

        return {'message': 'Estudante removido com sucesso!'}
    return {}