from fastapi import APIRouter, Request, Response, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models.note import Note
from config.db import client
from schemas.note import noteEntity, notesEntity
from bson import ObjectId

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
    return RedirectResponse(url="/", status_code=303)  # Redirect to the / route

@note.get("/{id}", response_description="Get a single note", response_model=Note)
async def show_student(id: str):
    if (to_show_note := client.notes.notes.find_one({"_id": ObjectId(id)})) is not None:
        print(to_show_note)
        return to_show_note

    raise HTTPException(status_code=404, detail=f"Note {id} not found")

@note.post("/edit/{id}")
async def update_notes(id: str, request: Request):
    try:
        form = await request.form()
        formDict = dict(form)

        updated_note = client.notes.notes.update_one({"_id": ObjectId(id)}, {"$set": formDict})
        if updated_note.modified_count > 0:
            return RedirectResponse(url="/", status_code=303)  # Redirect to the / route
        else:
            raise HTTPException(status_code=404, detail=f"Note {id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@note.post("/delete/{id}")
async def delete_notes(id: str):
    try:
        delete_note = client.notes.notes.delete_one({"_id": ObjectId(id)})
        if delete_note.deleted_count > 0:
            return RedirectResponse(url="/", status_code=303)  # Redirect to the / route
        else:
            raise HTTPException(status_code=404, detail=f"Note {id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))