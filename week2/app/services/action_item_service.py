# app/services/action_item_service.py
from typing import List, Optional
from ..db import db
from ..models import ActionItem
from ..exceptions import NotFoundException


class ActionItemService:
    def extract_and_save_llm(
        self, text: str, save_note: bool = False
    ) -> dict:
        note_id: Optional[int] = None
        if save_note:
            note_id = db.insert_note(text)

        from .extract import extract_action_items_api_llm
        items = extract_action_items_api_llm(text)

        ids = db.insert_action_items(items, note_id=note_id)
        return {"note_id": note_id, "items": [{"id": i, "text": t} for i, t in zip(ids, items)]}

    def extract_and_save_heuristic(
        self, text: str, save_note: bool = False
    ) -> dict:
        note_id: Optional[int] = None
        if save_note:
            note_id = db.insert_note(text)

        from .extract import extract_action_items
        items = extract_action_items(text)

        ids = db.insert_action_items(items, note_id=note_id)
        return {"note_id": note_id, "items": [{"id": i, "text": t} for i, t in zip(ids, items)]}

    def list_all(self, note_id: Optional[int] = None) -> List[ActionItem]:
        rows = db.list_action_items(note_id=note_id)
        return [ActionItem.model_validate(dict(row)) for row in rows]

    def mark_done(self, action_item_id: int, done: bool) -> ActionItem:
        db.mark_action_item_done(action_item_id, done)
        # 验证操作是否成功
        row = db.get_action_item(action_item_id)
        if row:
            return ActionItem.model_validate(dict(row))
        raise NotFoundException(f"Action item with id {action_item_id} not found")


action_item_service = ActionItemService()