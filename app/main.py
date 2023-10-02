from typing import Union
from fastapi import FastAPI, HTTPException, status, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from uuid import UUID, uuid1
from app.models.Student import Student, CreateStudent
from datetime import datetime
from asyncio import sleep
app = FastAPI()

students = {}

def log_new_students(name:str, course: str):
    print('log criada')
    with open ("students.txt", mode="a") as request_file:
        content = f'{name} - {course}\n'

        request_file.write(content)
    
@app.middleware('http')
async def log_requests(request: Request, call_next):
    started_at = datetime.now()

    headers = request.headers
    url = request.url
    method_name = request.method
    path_params = request.path_params
    query_params = request.query_params
    
    with open ("logs.txt", mode="a") as request_file:
        content = f'------------ LOG ({datetime.now()}) ------------\nURL: {url}\nMethod: {method_name}\nQueryParams: {query_params}\nPathParams: {path_params}\nHeaders: {headers}\n-----------------------------------------------------------\n'

        request_file.write(content)
    
    response = await call_next(request)
    process_time = datetime.now() - started_at
    response.headers["X-Time-Elapsed"] = str(process_time)
    
    
    return response

@app.get("/students")
async def list_all_students():
    await sleep(5)
    
    return JSONResponse(jsonable_encoder(students.items()), status_code=status.HTTP_200_OK)

@app.get("/students/{student_name}")
def list_student(student_name: str):
    if students.get(student_name):
        return JSONResponse(jsonable_encoder(students.get(student_name)), status_code=status.HTTP_200_OK)
    
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'details': 'Not found'})

@app.post("/students/")
def create_student(student: Student, bg_task: BackgroundTasks):
    if student:
        new_id = uuid1()
        new_student = CreateStudent(id=new_id, name=student.name, email=student.email, course=student.course, period=student.period,age=student.age)
        students[student.name] = new_student

        bg_task.add_task(log_new_students, name=student.name, course=student.course)

        return JSONResponse(jsonable_encoder(new_student), status_code=status.HTTP_201_CREATED)
    
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'details': 'Body cannot be empty'})

@app.put("/students/{student_name}")
def update_student(student_name: str, data: Student):
    if student_name and data:
        updated_student = CreateStudent(id=uuid1(), name=data.name, email=data.email, course=data.course, period=data.period, age=data.age)
        students[student_name] = updated_student
        
        return JSONResponse(jsonable_encoder(updated_student), status_code=status.HTTP_201_CREATED)
    
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'details': 'Body cannot be empty'})

@app.delete("/students/{student_id}")
def remove_student(student_id: str):
    if student_id in students:
        del students[student_id]

        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'details': 'Not found'})