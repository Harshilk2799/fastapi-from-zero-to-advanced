from fastapi import FastAPI
from app.notes import services as notes_services
from app.notes.schemas import NoteCreate, NoteUpdate, NotePatch, NoteOut
from app.db.config import SessionDep
from typing import List

app = FastAPI()

# Way 1
# @app.post("/notes")
# async def note_create(new_note: dict):
#     note = await notes_services.create_note(new_note["title"], new_note["content"])
#     return note

# Way 2
@app.post("/notes", response_model=NoteOut)
async def note_create(session: SessionDep, new_note: NoteCreate):
    note = await notes_services.create_note(session, new_note)
    return note

@app.get("/notes/{note_id}", response_model=NoteOut)
async def note_get(session: SessionDep, note_id: int):
    note = await notes_services.get_note(session, note_id)
    return note 

@app.get("/notes", response_model=List[NoteOut])
async def note_get_all(session: SessionDep):
    notes = await notes_services.get_all_notes(session)
    return notes 

# Way 1
# @app.put("/notes/{note_id}")
# async def note_update(note_id: int, new_note: dict):
#     new_title = new_note.get("title")
#     new_content = new_note.get("content")

#     note = await notes_services.update_note(note_id, new_title, new_content)
#     return note

# Way 2
@app.put("/notes/{note_id}", response_model=NoteOut)
async def note_update(session: SessionDep, note_id: int, new_note: NoteUpdate):
    note = await notes_services.update_note(session, note_id, new_note)
    return note

# Way 1
# @app.patch("/notes/{note_id}")
# async def note_patch(note_id: int, new_note: dict):
#     new_title = new_note.get("title")
#     new_content = new_note.get("content")

#     note = await notes_services.patch_note(note_id, new_title, new_content)
#     return note

# Way 2
@app.patch("/notes/{note_id}", response_model=NoteOut)
async def note_patch(session: SessionDep, note_id: int, new_note: NotePatch):
    note = await notes_services.patch_note(session, note_id, new_note)
    return note

@app.delete("/notes/{note_id}")
async def note_delete(session: SessionDep, note_id: int):
    response = await notes_services.delete_note(session, note_id)
    return response