from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import require_api_key
from app.database import get_session
from app.schemas import LoadResponse, LoadSearchRequest
from app.services.load_search import search_loads

router = APIRouter(prefix="/loads", tags=["loads"], dependencies=[Depends(require_api_key)])


@router.post("/search", response_model=list[LoadResponse])
async def search(filters: LoadSearchRequest, session: AsyncSession = Depends(get_session)):
    return await search_loads(session, filters)
