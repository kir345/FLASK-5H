import uvicorn
from fastapi import FastAPI,Request, HTTPException, Form
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Annotated

app = FastAPI()
templates = Jinja2Templates

tasks = []
class TaskIn(BaseModel):
    name: str
    task_id: int

class Task(TaskIn):
    id: int

class TaskOut(BaseModel):
    task_id: int
    name: str


@app.get('/tasks', response_class=HTMLResponse)
async def get_tasks(request: Request):
    return templates.TemplateResponse('tasks.html',{'request': request, 'tasks': tasks})


@app.post('/tasks/post/', response_model=TaskOut)
async def add_task(new_task: TaskIn):
    new_task_id = tasks[-1].id + 1 if len(tasks) else 1
    new_task = Task(id = new_task_id, name= new_task)
    tasks.append(new_task)


@app.put('/tasks/put/{task_id}', response_model=TaskOut)
async def edit_task(task_id: int, task_in: TaskIn):
    for task in tasks:
        if task.id == task_id:
            task.name == task_in.name
            return TaskOut(id=task.id, name=task.name)
    raise HTTPException(status_code=404, detail='Task not found')

@app.delete('/tasks/delete/{task_id}', response_model=dict)
async def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return {'message': 'Task delet'}
    raise HTTPException(status_code=404, detail='Task not found')

@app.get('/new_task/', response_class=HTMLResponse)
async def new_task(request: Request):
    return templates.TemplateResponse('new_task.html',{'request': request})

@app.post('/new_task/', response_class=HTMLResponse)
async def create_task(request: Request, task_name: Annotated[str, Form()]):
    await add_task(TaskIn(name=task_name))
    return await get_tasks(request)

if __name__ == '__main__':
    uvicorn.run('main_01:app', host='127.0.0.1', port=8000, reload=True)


