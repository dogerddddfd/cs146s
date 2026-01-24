# app/models.py
from typing import List, Optional
from pydantic import BaseModel


class ActionItemBase(BaseModel):
    text: str


class ActionItemCreate(ActionItemBase):
    pass


class ActionItem(ActionItemBase):
    id: int
    note_id: Optional[int] = None
    done: bool
    created_at: str

    class Config:
        from_attributes = True


class NoteBase(BaseModel):
    content: str


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    id: int
    created_at: str

    class Config:
        from_attributes = True


class ExtractRequest(BaseModel):
    text: str
    save_note: bool = False


class MarkDoneRequest(BaseModel):
    done: bool = True