import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Load

_TODAY = datetime.date.today

SEED_LOADS = [
    {"origin": "Dallas, TX", "destination": "Chicago, IL", "equipment_type": "Dry Van", "weight": 42000, "rate": 2200, "miles": 920, "pickup_offset": 1, "delivery_offset": 3, "commodity_type": "Electronics", "num_of_pieces": 24, "special_instructions": "No double stack"},
    {"origin": "Los Angeles, CA", "destination": "Phoenix, AZ", "equipment_type": "Reefer", "weight": 38000, "rate": 1450, "miles": 370, "pickup_offset": 2, "delivery_offset": 3, "commodity_type": "Frozen Foods", "num_of_pieces": 18, "special_instructions": "Temp set to -10F"},
    {"origin": "Atlanta, GA", "destination": "Miami, FL", "equipment_type": "Flatbed", "weight": 44000, "rate": 1800, "miles": 660, "pickup_offset": 1, "delivery_offset": 2, "commodity_type": "Steel Coils", "num_of_pieces": 6, "special_instructions": "Tarping required"},
    {"origin": "Houston, TX", "destination": "Memphis, TN", "equipment_type": "Dry Van", "weight": 30000, "rate": 1600, "miles": 580, "pickup_offset": 3, "delivery_offset": 5, "commodity_type": "Consumer Goods", "num_of_pieces": 32, "special_instructions": None},
    {"origin": "Seattle, WA", "destination": "Portland, OR", "equipment_type": "Reefer", "weight": 35000, "rate": 750, "miles": 175, "pickup_offset": 1, "delivery_offset": 1, "commodity_type": "Produce", "num_of_pieces": 40, "special_instructions": "Temp set to 34F"},
    {"origin": "Denver, CO", "destination": "Kansas City, MO", "equipment_type": "Step Deck", "weight": 46000, "rate": 1900, "miles": 600, "pickup_offset": 2, "delivery_offset": 4, "commodity_type": "Heavy Machinery", "num_of_pieces": 2, "special_instructions": "Oversized load permit required"},
    {"origin": "Nashville, TN", "destination": "Charlotte, NC", "equipment_type": "Dry Van", "weight": 28000, "rate": 1200, "miles": 410, "pickup_offset": 4, "delivery_offset": 5, "commodity_type": "Pharmaceuticals", "num_of_pieces": 50, "special_instructions": "Climate controlled, no stops"},
    {"origin": "Chicago, IL", "destination": "Detroit, MI", "equipment_type": "Flatbed", "weight": 40000, "rate": 950, "miles": 280, "pickup_offset": 1, "delivery_offset": 2, "commodity_type": "Lumber", "num_of_pieces": 12, "special_instructions": "Tarping required"},
    {"origin": "San Antonio, TX", "destination": "El Paso, TX", "equipment_type": "Dry Van", "weight": 25000, "rate": 1100, "miles": 550, "pickup_offset": 3, "delivery_offset": 4, "commodity_type": "Retail Goods", "num_of_pieces": 28, "special_instructions": None},
    {"origin": "Jacksonville, FL", "destination": "Savannah, GA", "equipment_type": "Power Only", "weight": 0, "rate": 450, "miles": 140, "pickup_offset": 1, "delivery_offset": 1, "commodity_type": "Pre-loaded Trailer", "num_of_pieces": 1, "special_instructions": "Trailer number TRL-4892"},
    {"origin": "Minneapolis, MN", "destination": "Milwaukee, WI", "equipment_type": "Reefer", "weight": 36000, "rate": 850, "miles": 340, "pickup_offset": 2, "delivery_offset": 3, "commodity_type": "Dairy Products", "num_of_pieces": 22, "special_instructions": "Temp set to 38F"},
    {"origin": "Phoenix, AZ", "destination": "Las Vegas, NV", "equipment_type": "Dry Van", "weight": 32000, "rate": 900, "miles": 300, "pickup_offset": 5, "delivery_offset": 6, "commodity_type": "Building Materials", "num_of_pieces": 15, "special_instructions": None},
    {"origin": "Columbus, OH", "destination": "Pittsburgh, PA", "equipment_type": "Flatbed", "weight": 43000, "rate": 1050, "miles": 185, "pickup_offset": 1, "delivery_offset": 2, "commodity_type": "Steel Beams", "num_of_pieces": 8, "special_instructions": "Escort vehicle required"},
    {"origin": "Dallas, TX", "destination": "Atlanta, GA", "equipment_type": "Dry Van", "weight": 39000, "rate": 2100, "miles": 780, "pickup_offset": 2, "delivery_offset": 4, "commodity_type": "Auto Parts", "num_of_pieces": 35, "special_instructions": "Dock-high delivery"},
    {"origin": "Los Angeles, CA", "destination": "San Francisco, CA", "equipment_type": "Step Deck", "weight": 45000, "rate": 1350, "miles": 380, "pickup_offset": 3, "delivery_offset": 4, "commodity_type": "Industrial Equipment", "num_of_pieces": 3, "special_instructions": "Forklift required at delivery"},
    {"origin": "Miami, FL", "destination": "Orlando, FL", "equipment_type": "Reefer", "weight": 34000, "rate": 650, "miles": 235, "pickup_offset": 1, "delivery_offset": 1, "commodity_type": "Seafood", "num_of_pieces": 30, "special_instructions": "Temp set to 28F"},
    {"origin": "Boston, MA", "destination": "New York, NY", "equipment_type": "Dry Van", "weight": 27000, "rate": 750, "miles": 215, "pickup_offset": 4, "delivery_offset": 5, "commodity_type": "Textiles", "num_of_pieces": 45, "special_instructions": "Liftgate required"},
    {"origin": "St. Louis, MO", "destination": "Indianapolis, IN", "equipment_type": "Power Only", "weight": 0, "rate": 500, "miles": 240, "pickup_offset": 2, "delivery_offset": 2, "commodity_type": "Pre-loaded Trailer", "num_of_pieces": 1, "special_instructions": "Trailer number TRL-7231"},
    {"origin": "Salt Lake City, UT", "destination": "Boise, ID", "equipment_type": "Flatbed", "weight": 41000, "rate": 1250, "miles": 340, "pickup_offset": 5, "delivery_offset": 7, "commodity_type": "Concrete Products", "num_of_pieces": 10, "special_instructions": "Tarping required"},
    {"origin": "New Orleans, LA", "destination": "Houston, TX", "equipment_type": "Dry Van", "weight": 33000, "rate": 850, "miles": 350, "pickup_offset": 3, "delivery_offset": 4, "commodity_type": "Food & Beverage", "num_of_pieces": 20, "special_instructions": None},
]


async def seed_loads(session: AsyncSession) -> None:
    result = await session.execute(select(Load.id).limit(1))
    if result.scalar() is not None:
        return  # already seeded

    today = _TODAY()
    for data in SEED_LOADS:
        load = Load(
            origin=data["origin"],
            destination=data["destination"],
            equipment_type=data["equipment_type"],
            weight=data["weight"],
            rate=data["rate"],
            miles=data["miles"],
            pickup_date=today + datetime.timedelta(days=data["pickup_offset"]),
            delivery_date=today + datetime.timedelta(days=data["delivery_offset"]),
            commodity_type=data["commodity_type"],
            num_of_pieces=data["num_of_pieces"],
            special_instructions=data["special_instructions"],
        )
        session.add(load)

    await session.commit()
