from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException

from ..db import db
# from ..services.extract import extract_action_items
from ..services.extract import extract_action_items_api_llm
from ..models import ExtractRequest, ActionItem, MarkDoneRequest
from ..exceptions import BadRequestException
from ..services.action_item_service import action_item_service

router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.post("/extract")
def extract(payload: ExtractRequest, method: str = "llm") -> Dict[str, Any]:
    if method == "heuristic":
        return action_item_service.extract_and_save_heuristic(payload.text, payload.save_note)
    else:
        return action_item_service.extract_and_save_llm(payload.text, payload.save_note)


@router.get("")
def list_all(note_id: Optional[int] = None) -> List[ActionItem]:
    return action_item_service.list_all(note_id=note_id)


@router.post("/{action_item_id}/done")
def mark_done(action_item_id: int, payload: MarkDoneRequest) -> ActionItem:
    return action_item_service.mark_done(action_item_id, payload.done)


