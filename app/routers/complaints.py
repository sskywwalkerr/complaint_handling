from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import ComplaintResponse, ComplaintCreate, OpenComplaint
from app.services import complaint_service

router = APIRouter()


@router.post("/", response_model=ComplaintResponse)
async def create_complaint(
    complaint: ComplaintCreate,
    db: AsyncSession = Depends(get_db)
):
    return await complaint_service.create_complaint(db, {"text": complaint.text})


@router.get("/open/", response_model=list[OpenComplaint])
async def get_open_complaints(
    hours: int = 1,
    db: AsyncSession = Depends(get_db)
):
    return await complaint_service.get_open_complaints(db, hours)


@router.patch("/{complaint_id}/close/")
async def close_complaint(
    complaint_id: int,
    db: AsyncSession = Depends(get_db)
):
    await complaint_service.close_complaint(db, complaint_id)
    return {"status": "closed"}
