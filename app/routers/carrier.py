from fastapi import APIRouter, Depends

from app.auth import require_api_key
from app.schemas import CarrierVerifyResponse
from app.services.fmcsa import verify_carrier

router = APIRouter(prefix="/carrier", tags=["carrier"], dependencies=[Depends(require_api_key)])


@router.get("/verify/{mc_number}", response_model=CarrierVerifyResponse)
async def verify(mc_number: str):
    return await verify_carrier(mc_number)
