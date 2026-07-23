from pydantic import BaseModel, ConfigDict

# Shared based fields 
class NoteBase(BaseModel):
    title: str 
    content: str 

# For creation
class NoteCreate(NoteBase):
    pass 

# For full update (PUT)
class NoteUpdate(NoteBase):
    pass

# For partial update (PATCH)
class NotePatch(BaseModel):
    title: str | None = None 
    content: str | None = None 

class NoteOut(NoteBase):
    id: int
    model_config = ConfigDict(from_attributes=True)