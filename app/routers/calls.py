from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import require_api_key
from app.database import get_session
from app.models import CallLog
from app.schemas import CallLogRequest, CallLogResponse

router = APIRouter(prefix="/calls", tags=["calls"], dependencies=[Depends(require_api_key)])


@router.post("/log", response_model=CallLogResponse)
async def log_call(payload: CallLogRequest, session: AsyncSession = Depends(get_session)):
    call = CallLog(**payload.model_dump())
    session.add(call)
    await session.commit()
    await session.refresh(call)
    return call
