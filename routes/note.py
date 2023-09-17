from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models.note import Note
from config.db import client
from schemas.note import noteEntity, notesEntity

note = APIRouter()

# Mount templates
templates = Jinja2Templates(directory="templates")

@note.get("/", response_class=HTMLResponse)
async def index(request: Request):
    docs = client.notes.notes.find({})
    newDocs = []
    for doc in docs:
        newDocs.append({
            "id": doc["_id"],
            "title": doc["title"],
            "description": doc["description"],
        })
    print(newDocs)
    return templates.TemplateResponse("index.html", {"request": request, "newDocs": newDocs})

@note.post('/note')
async def create_notes(request: Request):
    form = await request.form()

    formDict = dict(form)

    created_note = client.notes.notes.insert_one(formDict)
    return {"message": "Note created successfully"}