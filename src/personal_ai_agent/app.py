import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

from personal_ai_agent.config import Settings
from personal_ai_agent.llm import (
    ChatConfigurationError,
    ChatProviderError,
    ChatProviderTimeout,
    get_chat_reply,
)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10_000)

    @field_validator("message")
    @classmethod
    def message_must_not_be_whitespace(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("message must not be blank")
        return value


class ChatResponse(BaseModel):
    reply: str


def create_app(
    settings: Settings | None = None,
    transport: httpx.AsyncBaseTransport | None = None,
) -> FastAPI:
    app = FastAPI(title="Personal AI Agent API", version="0.1.0")
    configured_settings = settings or Settings.from_env()

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/chat", response_model=ChatResponse)
    async def chat(request: ChatRequest) -> ChatResponse:
        try:
            reply = await get_chat_reply(request.message, configured_settings, transport)
        except ChatConfigurationError as exc:
            raise HTTPException(
                status_code=503,
                detail="Chat provider is not configured",
            ) from exc
        except ChatProviderTimeout as exc:
            raise HTTPException(
                status_code=504,
                detail="Chat provider request timed out",
            ) from exc
        except ChatProviderError as exc:
            raise HTTPException(
                status_code=502,
                detail="Chat provider request failed",
            ) from exc

        return ChatResponse(reply=reply)

    return app


app = create_app()
