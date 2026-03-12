from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CallLog
from app.schemas import DashboardResponse


async def get_dashboard(session: AsyncSession) -> DashboardResponse:
    # Total calls
    total = (await session.execute(select(func.count(CallLog.id)))).scalar() or 0

    # Outcome distribution
    outcome_rows = (
        await session.execute(
            select(CallLog.call_outcome, func.count()).group_by(CallLog.call_outcome)
        )
    ).all()
    outcome_distribution = {row[0]: row[1] for row in outcome_rows}

    # Sentiment breakdown
    sentiment_rows = (
        await session.execute(
            select(CallLog.sentiment, func.count())
            .where(CallLog.sentiment.is_not(None))
            .group_by(CallLog.sentiment)
        )
    ).all()
    sentiment_breakdown = {row[0]: row[1] for row in sentiment_rows}

    # Success rate
    booked = outcome_distribution.get("booked", 0)
    success_rate = round((booked / total * 100) if total > 0 else 0, 1)

    # Average negotiation rounds
    avg_rounds_result = (
        await session.execute(select(func.avg(CallLog.counter_offer_count)))
    ).scalar()
    avg_rounds = round(float(avg_rounds_result), 1) if avg_rounds_result else 0.0

    # Total booked value
    booked_value_result = (
        await session.execute(
            select(func.coalesce(func.sum(CallLog.agreed_rate), 0))
            .where(CallLog.call_outcome == "booked")
        )
    ).scalar()
    total_booked_value = float(booked_value_result) if booked_value_result else 0.0

    return DashboardResponse(
        total_calls=total,
        success_rate=success_rate,
        outcome_distribution=outcome_distribution,
        sentiment_breakdown=sentiment_breakdown,
        average_negotiation_rounds=avg_rounds,
        total_booked_value=total_booked_value,
    )
