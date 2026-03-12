from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import require_api_key
from app.database import get_session
from app.schemas import DashboardResponse
from app.services.metrics import get_dashboard

router = APIRouter(prefix="/dashboard", tags=["dashboard"], dependencies=[Depends(require_api_key)])


@router.get("", response_model=DashboardResponse)
async def dashboard(session: AsyncSession = Depends(get_session)):
    return await get_dashboard(session)
