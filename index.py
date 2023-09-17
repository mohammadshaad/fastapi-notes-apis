from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.note import note

app = FastAPI() 

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(note)