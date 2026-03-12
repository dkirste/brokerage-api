from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Load
from app.schemas import LoadSearchRequest


async def search_loads(session: AsyncSession, filters: LoadSearchRequest) -> list[Load]:
    stmt = select(Load).where(Load.status == "available")

    if filters.origin:
        stmt = stmt.where(Load.origin.ilike(f"%{filters.origin}%"))
    if filters.destination:
        stmt = stmt.where(Load.destination.ilike(f"%{filters.destination}%"))
    if filters.equipment_type:
        stmt = stmt.where(Load.equipment_type.ilike(f"%{filters.equipment_type}%"))
    if filters.commodity_type:
        stmt = stmt.where(Load.commodity_type.ilike(f"%{filters.commodity_type}%"))
    if filters.pickup_date:
        stmt = stmt.where(Load.pickup_date == filters.pickup_date)
    if filters.max_weight is not None:
        stmt = stmt.where(Load.weight <= filters.max_weight)
    if filters.min_rate is not None:
        stmt = stmt.where(Load.rate >= filters.min_rate)
    if filters.max_miles is not None:
        stmt = stmt.where(Load.miles <= filters.max_miles)
    if filters.num_of_pieces is not None:
        stmt = stmt.where(Load.num_of_pieces <= filters.num_of_pieces)

    result = await session.execute(stmt.order_by(Load.pickup_date))
    return list(result.scalars().all())
