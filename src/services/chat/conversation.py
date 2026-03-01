"""会话管理服务模块"""

from typing import Dict

import httpx

CREATE_URL = "https://yuanbao.tencent.com/api/user/agent/conversation/create"
CLEAR_URL = "https://yuanbao.tencent.com/api/user/agent/conversation/v1/clear"

DEFAULT_TIMEOUT = 60


class ConversationCreationError(Exception):
    """会话创建异常"""

    pass


class ConversationRemoveError(Exception):
    """会话删除异常"""

    pass


async def create_conversation(agent_id: str, headers: Dict[str, str], timeout: int = DEFAULT_TIMEOUT) -> str:
    """创建会话

    Args:
        agent_id: 代理 ID
        headers: 认证请求头
        timeout: 超时时间

    Returns:
        str: 会话 ID

    Raises:
        ConversationCreationError: 会话创建失败时抛出
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(CREATE_URL, json={"agentId": agent_id}, headers=headers, timeout=timeout)

            if response.status_code != 200:
                raise Exception(f"Request failed. Status code: {response.status_code}, Response: {response.text}")

            try:
                json_data = response.json()
            except ValueError:
                raise Exception(f"Failed to parse response as JSON. Response: {response.text}")

            if "id" not in json_data:
                raise Exception(f"Failed to find 'id' in response JSON. Response: {response.text}")

            return json_data["id"]

    except Exception as e:
        raise ConversationCreationError(e)


async def remove_conversation(chat_id: str, headers: Dict[str, str], timeout: int = DEFAULT_TIMEOUT) -> None:
    """删除会话

    Args:
        chat_id: 会话 ID
        headers: 认证请求头
        timeout: 超时时间

    Raises:
        ConversationRemoveError: 会话删除失败时抛出
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                CLEAR_URL,
                json={"conversationIds": [chat_id], "uiOptions": {"noToast": True}},
                headers=headers,
                timeout=timeout,
            )

            if response.status_code != 200:
                raise Exception(f"Request failed. Status code: {response.status_code}, Response: {response.text}")

    except Exception as e:
        raise ConversationRemoveError(e)
