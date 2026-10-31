import logging

import httpx

from personal_ai_agent.config import Settings

logger = logging.getLogger(__name__)


class ChatConfigurationError(Exception):
    """The provider is not configured for chat requests."""


class ChatProviderTimeout(Exception):
    """The provider did not respond before the configured timeout."""


class ChatProviderError(Exception):
    """The provider request failed or returned an invalid response."""


async def get_chat_reply(
    message: str,
    settings: Settings,
    transport: httpx.AsyncBaseTransport | None = None,
) -> str:
    if not settings.api_key:
        raise ChatConfigurationError

    try:
        async with httpx.AsyncClient(
            timeout=settings.request_timeout_seconds,
            transport=transport,
        ) as client:
            response = await client.post(
                f"{settings.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {settings.api_key}"},
                json={
                    "model": settings.model,
                    "messages": [{"role": "user", "content": message}],
                },
            )
    except httpx.TimeoutException as exc:
        raise ChatProviderTimeout from exc
    except httpx.RequestError as exc:
        logger.warning("Chat provider request failed: %s", type(exc).__name__)
        raise ChatProviderError from exc

    if response.is_error:
        logger.warning("Chat provider returned HTTP %s", response.status_code)
        raise ChatProviderError

    try:
        content = response.json()["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError) as exc:
        logger.warning("Chat provider returned an invalid response payload")
        raise ChatProviderError from exc

    if not isinstance(content, str):
        logger.warning("Chat provider returned a non-text response")
        raise ChatProviderError

    return content
