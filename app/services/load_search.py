from sqlalchemy import cast, Date, select
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

    pickup_date = filters.get_pickup_date()
    if pickup_date is not None:
        stmt = stmt.where(cast(Load.pickup_date, Date) == pickup_date)

    max_weight = filters.get_max_weight()
    if max_weight is not None:
        stmt = stmt.where(Load.weight <= max_weight)

    min_rate = filters.get_min_rate()
    if min_rate is not None:
        stmt = stmt.where(Load.rate >= min_rate)

    max_miles = filters.get_max_miles()
    if max_miles is not None:
        stmt = stmt.where(Load.miles <= max_miles)

    num_of_pieces = filters.get_num_of_pieces()
    if num_of_pieces is not None:
        stmt = stmt.where(Load.num_of_pieces <= num_of_pieces)

    result = await session.execute(stmt.order_by(Load.pickup_date))
    return list(result.scalars().all())
