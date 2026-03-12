from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader

from app.config import settings

_header = APIKeyHeader(name="x-api-key", auto_error=False)


async def require_api_key(key: str | None = Security(_header)) -> str:
    if not key or key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return key
