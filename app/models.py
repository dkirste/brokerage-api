import datetime
import uuid

from sqlalchemy import Date, DateTime, Float, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Load(Base):
    __tablename__ = "loads"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    origin: Mapped[str] = mapped_column(String(255))
    destination: Mapped[str] = mapped_column(String(255))
    equipment_type: Mapped[str] = mapped_column(String(100))
    weight: Mapped[float] = mapped_column(Float)
    rate: Mapped[float] = mapped_column(Float)
    miles: Mapped[int] = mapped_column(Integer)
    pickup_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    delivery_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    commodity_type: Mapped[str] = mapped_column(String(255))
    num_of_pieces: Mapped[int] = mapped_column(Integer)
    dimensions: Mapped[str | None] = mapped_column(String(255), nullable=True)
    special_instructions: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="available")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class CallLog(Base):
    __tablename__ = "call_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mc_number: Mapped[str] = mapped_column(String(20))
    carrier_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    load_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    origin: Mapped[str | None] = mapped_column(String(255), nullable=True)
    destination: Mapped[str | None] = mapped_column(String(255), nullable=True)
    agreed_rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    counter_offer_count: Mapped[int] = mapped_column(Integer, default=0)
    call_outcome: Mapped[str] = mapped_column(String(50))  # booked, declined, callback, no_answer
    sentiment: Mapped[str | None] = mapped_column(String(50), nullable=True)  # positive, neutral, negative
    transcript: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
