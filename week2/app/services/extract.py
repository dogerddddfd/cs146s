from __future__ import annotations

import os
import re
from typing import List
import json
from typing import Any
from ollama import chat
from dotenv import load_dotenv

load_dotenv()

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)



def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters


# Shared system prompt for action item extraction
ACTION_ITEM_SYSTEM_PROMPT = """
Extract action items from text. Action items are tasks/activities to perform.

Rules:
1. Extract all action items, any format
2. Each as concise sentence
3. No explanations/intro text
4. Output JSON array of strings
5. Empty array if none found
6. Match output language to input language

Examples:
Input: "We need to fix the login bug by Friday. Update docs too."
Output: ["Fix the login bug by Friday", "Update docs too"]

Input: "我们需要修复登录漏洞，还要更新文档。"
Output: ["修复登录漏洞", "更新文档"]
"""


def extract_action_items_llm(text: str) -> List[str]:
    """Extract action items from text using a local LLM (mistral-nemo:12b).
    
    Args:
        text: Input text containing action items in any format
        
    Returns:
        List of extracted action items
    """
    # Use the shared system prompt
    
    try:
        response = chat(
            model="mistral-nemo:12b",
            messages=[
                {"role": "system", "content": ACTION_ITEM_SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
            options={"temperature": 0.1, "format": "json"},
        )
        
        output_text = response.message.content.strip()
        
        # Parse the JSON response
        action_items = json.loads(output_text)
        
        # Ensure we have a list of strings
        if isinstance(action_items, list):
            # Filter out empty strings and strip whitespace
            return [item.strip() for item in action_items if isinstance(item, str) and item.strip()]
        else:
            return []
            
    except Exception as e:
        print(f"Error extracting action items with LLM: {e}")
        # Return empty list on error
        return []


def extract_action_items_api_llm(text: str) -> List[str]:
    """Extract action items from text using an external LLM API.
    
    Args:
        text: Input text containing action items in any format
        
    Returns:
        List of extracted action items
    """
    # Use the shared system prompt
    
    try:
        # Import the LLM API functions
        from my_llm import llm, get_content
        
        # Prepare messages in the format expected by the API
        messages = [
            {"role": "system", "content": ACTION_ITEM_SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ]
        
        # Call the LLM API
        response = llm(messages, enable_thinking=False)
        
        # Extract the content from the response
        output_text = get_content(response).strip()
        
        # Parse the JSON response
        action_items = json.loads(output_text)
        
        # Ensure we have a list of strings
        if isinstance(action_items, list):
            # Filter out empty strings and strip whitespace
            return [item.strip() for item in action_items if isinstance(item, str) and item.strip()]
        else:
            return []
            
    except Exception as e:
        print(f"Error extracting action items with API LLM: {e}")
        # Return empty list on error
        return []
