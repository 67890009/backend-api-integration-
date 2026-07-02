from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import LeaveStatus
from app.leave_requests.model import LeaveRequest
from app.leave_requests.repository import LeaveRequestRepository
from app.leave_requests.schema import LeaveRequestCreate


class LeaveRequestService:

    def __init__(self):
        self.repository = LeaveRequestRepository()

    async def apply_leave(
        self,
        db: AsyncSession,
        data: LeaveRequestCreate,
    ) -> LeaveRequest:

        leave_request = LeaveRequest(
            employee_id=data.employee_id,
            leave_type_id=data.leave_type_id,
            start_date=data.start_date,
            end_date=data.end_date,
            number_of_days=data.number_of_days,
            reason=data.reason,
        )

        return await self.repository.create(
            db,
            leave_request,
        )

    async def get_leave_request(
        self,
        db: AsyncSession,
        leave_request_id: UUID,
    ) -> LeaveRequest:

        leave_request = await self.repository.get_by_id(
            db,
            leave_request_id,
        )

        if leave_request is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Leave request not found.",
            )

        return leave_request

    async def get_all_leave_requests(
        self,
        db: AsyncSession,
    ) -> list[LeaveRequest]:

        return await self.repository.get_all(db)

    async def get_employee_leave_requests(
        self,
        db: AsyncSession,
        employee_id: UUID,
    ) -> list[LeaveRequest]:

        return await self.repository.get_by_employee(
            db,
            employee_id,
        )

    async def cancel_leave_request(
        self,
        db: AsyncSession,
        leave_request_id: UUID,
    ) -> LeaveRequest:

        leave_request = await self.repository.get_by_id(
            db,
            leave_request_id,
        )

        if leave_request is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Leave request not found.",
            )

        leave_request.status = LeaveStatus.CANCELLED

        return await self.repository.update(
            db,
            leave_request,
        )