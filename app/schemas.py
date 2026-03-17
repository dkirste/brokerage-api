import datetime
import uuid

from pydantic import BaseModel, field_validator


# --- Carrier ---

class CarrierVerifyResponse(BaseModel):
    mc_number: str
    legal_name: str | None = None
    dot_number: str | None = None
    entity_type: str | None = None
    operating_status: str | None = None
    out_of_service: bool = False
    insurance_on_file: bool = False
    eligible: bool = False
    eligibility_reasons: list[str] = []


# --- Loads ---

class LoadSearchRequest(BaseModel):
    origin: str | None = None
    destination: str | None = None
    equipment_type: str | None = None
    pickup_date: str | None = None
    max_weight: str | None = None
    min_rate: str | None = None
    max_miles: str | None = None
    commodity_type: str | None = None
    num_of_pieces: str | None = None

    @field_validator("pickup_date", mode="before")
    @classmethod
    def parse_pickup_date(cls, v: object) -> str | None:
        if v is None or v == "":
            return None
        return str(v)

    def get_pickup_date(self) -> datetime.date | None:
        if not self.pickup_date:
            return None
        try:
            return datetime.date.fromisoformat(self.pickup_date)
        except (ValueError, TypeError):
            return None

    def get_max_weight(self) -> float | None:
        if not self.max_weight:
            return None
        try:
            return float(self.max_weight)
        except (ValueError, TypeError):
            return None

    def get_min_rate(self) -> float | None:
        if not self.min_rate:
            return None
        try:
            return float(self.min_rate)
        except (ValueError, TypeError):
            return None

    def get_max_miles(self) -> int | None:
        if not self.max_miles:
            return None
        try:
            return int(self.max_miles)
        except (ValueError, TypeError):
            return None

    def get_num_of_pieces(self) -> int | None:
        if not self.num_of_pieces:
            return None
        try:
            return int(self.num_of_pieces)
        except (ValueError, TypeError):
            return None


class LoadResponse(BaseModel):
    id: uuid.UUID
    origin: str
    destination: str
    equipment_type: str
    weight: float
    rate: float
    miles: int
    pickup_date: datetime.datetime
    delivery_date: datetime.datetime
    commodity_type: str
    num_of_pieces: int
    dimensions: str | None = None
    special_instructions: str | None = None
    status: str

    model_config = {"from_attributes": True}


# --- Calls ---

class CallLogRequest(BaseModel):
    mc_number: str
    carrier_name: str | None = None
    load_id: str | None = None
    origin: str | None = None
    destination: str | None = None
    agreed_rate: float | None = None
    counter_offer_count: int = 0
    call_outcome: str  # booked, declined, callback, no_answer
    sentiment: str | None = None  # positive, neutral, negative
    transcript: str | None = None


class CallLogResponse(BaseModel):
    id: uuid.UUID
    mc_number: str
    carrier_name: str | None = None
    load_id: str | None = None
    origin: str | None = None
    destination: str | None = None
    agreed_rate: float | None = None
    counter_offer_count: int
    call_outcome: str
    sentiment: str | None = None
    transcript: str | None = None
    created_at: datetime.datetime

    model_config = {"from_attributes": True}


# --- Dashboard ---

class DashboardResponse(BaseModel):
    total_calls: int
    success_rate: float
    outcome_distribution: dict[str, int]
    sentiment_breakdown: dict[str, int]
    average_negotiation_rounds: float
    total_booked_value: float
