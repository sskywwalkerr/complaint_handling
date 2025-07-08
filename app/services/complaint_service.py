import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime, timedelta

from app.models import Complaint
from app.schemas import ComplaintResponse, OpenComplaint
from app.services.external_api import analyze_sentiment, categorize_complaint, get_location_by_ip


async def create_complaint(db: AsyncSession, complaint_data: dict) -> ComplaintResponse:
    ip = complaint_data.get("ip", "")  # Получаем IP из данных
    sentiment_task = analyze_sentiment(complaint_data["text"])
    category_task = categorize_complaint(complaint_data["text"])
    location_task = get_location_by_ip(ip)

    sentiment, category, location = await asyncio.gather(
        sentiment_task,
        category_task,
        location_task
    )

    db_complaint = Complaint(
        text=complaint_data["text"],
        sentiment=sentiment,
        category=category,
        location=location or {}  # Сохраняем полный JSON-ответ от IP API
    )
    db.add(db_complaint)
    await db.commit()
    await db.refresh(db_complaint)

    return ComplaintResponse(
        id=db_complaint.id,
        status=db_complaint.status,
        sentiment=db_complaint.sentiment,
        category=db_complaint.category,
        location=db_complaint.location
    )


async def get_open_complaints(db: AsyncSession, hours: int = 1) -> list[OpenComplaint]:
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    result = await db.execute(
        select(Complaint)
        .where(Complaint.status == "open")
        .where(Complaint.timestamp >= time_threshold)
    )
    complaints = result.scalars().all()

    return [
        OpenComplaint(
            id=c.id,
            text=c.text,
            category=c.category,
            sentiment=c.sentiment,
            timestamp=c.timestamp
        )
        for c in complaints
    ]


async def close_complaint(db: AsyncSession, complaint_id: int):
    await db.execute(
        update(Complaint)
        .where(Complaint.id == complaint_id)
        .values(status="closed")
    )
    await db.commit()
