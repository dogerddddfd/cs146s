from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from ..models import NoteCreate, Note
from ..services.note_service import create_note_service, get_single_note_service, list_notes_service



router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("", response_model=List[Note])
def list_notes() -> List[Note]:
    notes = list_notes_service()
    return [Note(id=note["id"], content=note["content"], created_at=note["created_at"]) for note in notes]


@router.post("")
def create_note(payload: NoteCreate) -> Note:
    note = create_note_service(payload)
    return Note(
        id=note["id"],
        content=note["content"],
        created_at=note["created_at"],
    )


@router.get("/{note_id}")
def get_single_note(note_id: int) -> Note:
    note = get_single_note_service(note_id)
    return Note(
        id=note["id"],
        content=note["content"],
        created_at=note["created_at"],
    )


