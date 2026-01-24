from typing import Dict, Any, List

from ..db import db
from ..models import NoteCreate, Note
from ..exceptions import BadRequestException, NotFoundException


def create_note_service(payload: NoteCreate) -> Dict[str, Any]:
    content = str(payload.content).strip()
    if not content:
        raise BadRequestException(detail="content is required")
    note_id = db.insert_note(content)
    note = db.get_note(note_id)
    return note


def get_single_note_service(note_id: int) -> Dict[str, Any]:
    note = db.get_note(note_id)
    if note is None:
        raise NotFoundException(detail="note not found")
    return note


def list_notes_service() -> List[Dict[str, Any]]:
    rows = db.list_notes()
    return [dict(row) for row in rows]
