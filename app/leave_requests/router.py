from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.leave_requests.schema import (
    LeaveRequestCreate,
    LeaveRequestResponse,
)
from app.leave_requests.service import LeaveRequestService

router = APIRouter(
    prefix="/leave-requests",
    tags=["Leave Requests"],
)

service = LeaveRequestService()


@router.post(
    "/",
    response_model=LeaveRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
async def apply_leave(
    data: LeaveRequestCreate,
    db: AsyncSession = Depends(get_db),
):
    return await service.apply_leave(
        db,
        data,
    )


@router.get(
    "/",
    response_model=list[LeaveRequestResponse],
)
async def get_all_leave_requests(
    db: AsyncSession = Depends(get_db),
):
    return await service.get_all_leave_requests(
        db,
    )


@router.get(
    "/employee/{employee_id}",
    response_model=list[LeaveRequestResponse],
)
async def get_employee_leave_requests(
    employee_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    return await service.get_employee_leave_requests(
        db,
        employee_id,
    )


@router.get(
    "/{leave_request_id}",
    response_model=LeaveRequestResponse,
)
async def get_leave_request(
    leave_request_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    return await service.get_leave_request(
        db,
        leave_request_id,
    )


@router.patch(
    "/{leave_request_id}/cancel",
    response_model=LeaveRequestResponse,
)
async def cancel_leave_request(
    leave_request_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    return await service.cancel_leave_request(
        db,
        leave_request_id,
    )