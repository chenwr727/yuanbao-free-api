import json
import time
from typing import AsyncGenerator, Dict, List, Optional

import httpx

from src.const import CHUNK_TYPE, MODEL_MAPPING
from src.schemas.chat import ChatCompletionChunk, Choice, ChoiceDelta, Message


def get_model_info(model_name: str) -> Optional[Dict]:
    return MODEL_MAPPING.get(model_name.lower(), None)


def parse_messages(messages: List[Message]) -> str:
    only_user_message = True
    for m in messages:
        if m.role == "user":
            only_user_message = False
            break
    if only_user_message:
        prompt = "\n".join([f"{m.role}: {m.content}" for m in messages])
    else:
        prompt = "\n".join([f"{m.content}" for m in messages])
    return prompt


async def process_response_stream(response: httpx.Response, model_id: str) -> AsyncGenerator[str, None]:
    def _create_chunk(content: str, finish_reason: Optional[str] = None) -> str:
        choice_delta = ChoiceDelta(content=content)
        choice = Choice(delta=choice_delta, finish_reason=finish_reason)
        chunk = ChatCompletionChunk(created=int(time.time()), model=model_id, choices=[choice])
        return chunk.model_dump_json(exclude_unset=True)

    status = ""
    start_word = "data: "
    finish_reason = "stop"
    async for line in response.aiter_lines():
        if not line or not line.startswith(start_word):
            continue
        data: str = line[len(start_word) :]

        if data == "[DONE]":
            yield _create_chunk("", finish_reason)
            yield "[DONE]"
            break
        elif not data.startswith("{"):
            continue

        chunk_data: Dict = json.loads(data)
        status = chunk_data["type"]
        if status == CHUNK_TYPE.TEXT:
            if chunk_data.get("msg"):
                yield _create_chunk(f"[{status}]" + chunk_data["msg"])
            if chunk_data.get("stopReason"):
                finish_reason = chunk_data["stopReason"]
        elif status == CHUNK_TYPE.THINK:
            yield _create_chunk(f"[{status}]" + chunk_data.get("content", ""))
        elif status == CHUNK_TYPE.SEARCH_GUIDE:
            docs = chunk_data.get("docs", [])
            yield _create_chunk(f"[{status}]" + json.dumps(docs, ensure_ascii=False))
        elif status == CHUNK_TYPE.STEP:
            yield _create_chunk(f"[{status}]" + chunk_data.get("msg", ""))
