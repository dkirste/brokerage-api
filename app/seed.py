import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Load

_TODAY = datetime.date.today

SEED_LOADS = [
    {"origin": "Dallas, TX", "destination": "Chicago, IL", "equipment_type": "Dry Van", "weight": 42000, "rate": 2200, "miles": 920, "pickup_offset": 1, "pickup_hour": 8, "delivery_offset": 3, "delivery_hour": 14, "commodity_type": "Electronics", "num_of_pieces": 24, "dimensions": "48x40x48 in", "special_instructions": "No double stack"},
    {"origin": "Los Angeles, CA", "destination": "Phoenix, AZ", "equipment_type": "Reefer", "weight": 38000, "rate": 1450, "miles": 370, "pickup_offset": 2, "pickup_hour": 6, "delivery_offset": 3, "delivery_hour": 10, "commodity_type": "Frozen Foods", "num_of_pieces": 18, "dimensions": "48x40x40 in", "special_instructions": "Temp set to -10F"},
    {"origin": "Atlanta, GA", "destination": "Miami, FL", "equipment_type": "Flatbed", "weight": 44000, "rate": 1800, "miles": 660, "pickup_offset": 1, "pickup_hour": 7, "delivery_offset": 2, "delivery_hour": 16, "commodity_type": "Steel Coils", "num_of_pieces": 6, "dimensions": "72x48x48 in", "special_instructions": "Tarping required"},
    {"origin": "Houston, TX", "destination": "Memphis, TN", "equipment_type": "Dry Van", "weight": 30000, "rate": 1600, "miles": 580, "pickup_offset": 3, "pickup_hour": 9, "delivery_offset": 5, "delivery_hour": 12, "commodity_type": "Consumer Goods", "num_of_pieces": 32, "dimensions": "48x40x48 in", "special_instructions": None},
    {"origin": "Seattle, WA", "destination": "Portland, OR", "equipment_type": "Reefer", "weight": 35000, "rate": 750, "miles": 175, "pickup_offset": 1, "pickup_hour": 5, "delivery_offset": 1, "delivery_hour": 14, "commodity_type": "Produce", "num_of_pieces": 40, "dimensions": "40x40x36 in", "special_instructions": "Temp set to 34F"},
    {"origin": "Denver, CO", "destination": "Kansas City, MO", "equipment_type": "Step Deck", "weight": 46000, "rate": 1900, "miles": 600, "pickup_offset": 2, "pickup_hour": 10, "delivery_offset": 4, "delivery_hour": 15, "commodity_type": "Heavy Machinery", "num_of_pieces": 2, "dimensions": "120x96x84 in", "special_instructions": "Oversized load permit required"},
    {"origin": "Nashville, TN", "destination": "Charlotte, NC", "equipment_type": "Dry Van", "weight": 28000, "rate": 1200, "miles": 410, "pickup_offset": 4, "pickup_hour": 7, "delivery_offset": 5, "delivery_hour": 11, "commodity_type": "Pharmaceuticals", "num_of_pieces": 50, "dimensions": "24x20x24 in", "special_instructions": "Climate controlled, no stops"},
    {"origin": "Chicago, IL", "destination": "Detroit, MI", "equipment_type": "Flatbed", "weight": 40000, "rate": 950, "miles": 280, "pickup_offset": 1, "pickup_hour": 6, "delivery_offset": 2, "delivery_hour": 10, "commodity_type": "Lumber", "num_of_pieces": 12, "dimensions": "192x12x12 in", "special_instructions": "Tarping required"},
    {"origin": "San Antonio, TX", "destination": "El Paso, TX", "equipment_type": "Dry Van", "weight": 25000, "rate": 1100, "miles": 550, "pickup_offset": 3, "pickup_hour": 8, "delivery_offset": 4, "delivery_hour": 17, "commodity_type": "Retail Goods", "num_of_pieces": 28, "dimensions": "48x40x48 in", "special_instructions": None},
    {"origin": "Jacksonville, FL", "destination": "Savannah, GA", "equipment_type": "Power Only", "weight": 0, "rate": 450, "miles": 140, "pickup_offset": 1, "pickup_hour": 12, "delivery_offset": 1, "delivery_hour": 18, "commodity_type": "Pre-loaded Trailer", "num_of_pieces": 1, "dimensions": None, "special_instructions": "Trailer number TRL-4892"},
    {"origin": "Minneapolis, MN", "destination": "Milwaukee, WI", "equipment_type": "Reefer", "weight": 36000, "rate": 850, "miles": 340, "pickup_offset": 2, "pickup_hour": 5, "delivery_offset": 3, "delivery_hour": 9, "commodity_type": "Dairy Products", "num_of_pieces": 22, "dimensions": "48x40x40 in", "special_instructions": "Temp set to 38F"},
    {"origin": "Phoenix, AZ", "destination": "Las Vegas, NV", "equipment_type": "Dry Van", "weight": 32000, "rate": 900, "miles": 300, "pickup_offset": 5, "pickup_hour": 9, "delivery_offset": 6, "delivery_hour": 13, "commodity_type": "Building Materials", "num_of_pieces": 15, "dimensions": "48x48x48 in", "special_instructions": None},
    {"origin": "Columbus, OH", "destination": "Pittsburgh, PA", "equipment_type": "Flatbed", "weight": 43000, "rate": 1050, "miles": 185, "pickup_offset": 1, "pickup_hour": 7, "delivery_offset": 2, "delivery_hour": 11, "commodity_type": "Steel Beams", "num_of_pieces": 8, "dimensions": "240x12x12 in", "special_instructions": "Escort vehicle required"},
    {"origin": "Dallas, TX", "destination": "Atlanta, GA", "equipment_type": "Dry Van", "weight": 39000, "rate": 2100, "miles": 780, "pickup_offset": 2, "pickup_hour": 8, "delivery_offset": 4, "delivery_hour": 16, "commodity_type": "Auto Parts", "num_of_pieces": 35, "dimensions": "36x24x24 in", "special_instructions": "Dock-high delivery"},
    {"origin": "Los Angeles, CA", "destination": "San Francisco, CA", "equipment_type": "Step Deck", "weight": 45000, "rate": 1350, "miles": 380, "pickup_offset": 3, "pickup_hour": 10, "delivery_offset": 4, "delivery_hour": 14, "commodity_type": "Industrial Equipment", "num_of_pieces": 3, "dimensions": "96x72x60 in", "special_instructions": "Forklift required at delivery"},
    {"origin": "Miami, FL", "destination": "Orlando, FL", "equipment_type": "Reefer", "weight": 34000, "rate": 650, "miles": 235, "pickup_offset": 1, "pickup_hour": 4, "delivery_offset": 1, "delivery_hour": 12, "commodity_type": "Seafood", "num_of_pieces": 30, "dimensions": "48x40x36 in", "special_instructions": "Temp set to 28F"},
    {"origin": "Boston, MA", "destination": "New York, NY", "equipment_type": "Dry Van", "weight": 27000, "rate": 750, "miles": 215, "pickup_offset": 4, "pickup_hour": 11, "delivery_offset": 5, "delivery_hour": 15, "commodity_type": "Textiles", "num_of_pieces": 45, "dimensions": "48x40x48 in", "special_instructions": "Liftgate required"},
    {"origin": "St. Louis, MO", "destination": "Indianapolis, IN", "equipment_type": "Power Only", "weight": 0, "rate": 500, "miles": 240, "pickup_offset": 2, "pickup_hour": 13, "delivery_offset": 2, "delivery_hour": 20, "commodity_type": "Pre-loaded Trailer", "num_of_pieces": 1, "dimensions": None, "special_instructions": "Trailer number TRL-7231"},
    {"origin": "Salt Lake City, UT", "destination": "Boise, ID", "equipment_type": "Flatbed", "weight": 41000, "rate": 1250, "miles": 340, "pickup_offset": 5, "pickup_hour": 6, "delivery_offset": 7, "delivery_hour": 10, "commodity_type": "Concrete Products", "num_of_pieces": 10, "dimensions": "48x48x12 in", "special_instructions": "Tarping required"},
    {"origin": "New Orleans, LA", "destination": "Houston, TX", "equipment_type": "Dry Van", "weight": 33000, "rate": 850, "miles": 350, "pickup_offset": 3, "pickup_hour": 9, "delivery_offset": 4, "delivery_hour": 13, "commodity_type": "Food & Beverage", "num_of_pieces": 20, "dimensions": "48x40x48 in", "special_instructions": None},
]


async def seed_loads(session: AsyncSession) -> None:
    result = await session.execute(select(Load.id).limit(1))
    if result.scalar() is not None:
        return  # already seeded

    today = _TODAY()
    for data in SEED_LOADS:
        pickup_dt = datetime.datetime.combine(
            today + datetime.timedelta(days=data["pickup_offset"]),
            datetime.time(hour=data["pickup_hour"]),
            tzinfo=datetime.timezone.utc,
        )
        delivery_dt = datetime.datetime.combine(
            today + datetime.timedelta(days=data["delivery_offset"]),
            datetime.time(hour=data["delivery_hour"]),
            tzinfo=datetime.timezone.utc,
        )
        load = Load(
            origin=data["origin"],
            destination=data["destination"],
            equipment_type=data["equipment_type"],
            weight=data["weight"],
            rate=data["rate"],
            miles=data["miles"],
            pickup_date=pickup_dt,
            delivery_date=delivery_dt,
            commodity_type=data["commodity_type"],
            num_of_pieces=data["num_of_pieces"],
            dimensions=data["dimensions"],
            special_instructions=data["special_instructions"],
        )
        session.add(load)

    await session.commit()
