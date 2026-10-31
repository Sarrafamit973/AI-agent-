import os
from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class Settings:
    api_key: str | None
    base_url: str
    model: str
    request_timeout_seconds: float

    @classmethod
    def from_env(cls) -> "Settings":
        timeout = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "30"))
        if not isfinite(timeout) or timeout <= 0:
            raise ValueError("REQUEST_TIMEOUT_SECONDS must be greater than zero")

        return cls(
            api_key=os.getenv("OPENAI_API_KEY") or None,
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/"),
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            request_timeout_seconds=timeout,
        )
