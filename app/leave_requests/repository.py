from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.leave_requests.model import LeaveRequest


class LeaveRequestRepository:

    async def create(
        self,
        db: AsyncSession,
        leave_request: LeaveRequest,
    ) -> LeaveRequest:

        db.add(leave_request)
        await db.commit()
        await db.refresh(leave_request)

        return leave_request

    async def get_by_id(
        self,
        db: AsyncSession,
        leave_request_id: UUID,
    ) -> LeaveRequest | None:

        result = await db.execute(
            select(LeaveRequest).where(
                LeaveRequest.id == leave_request_id
            )
        )

        return result.scalar_one_or_none()

    async def get_all(
        self,
        db: AsyncSession,
    ) -> list[LeaveRequest]:

        result = await db.execute(
            select(LeaveRequest).order_by(
                LeaveRequest.created_at.desc()
            )
        )

        return list(result.scalars().all())

    async def get_by_employee(
        self,
        db: AsyncSession,
        employee_id: UUID,
    ) -> list[LeaveRequest]:

        result = await db.execute(
            select(LeaveRequest)
            .where(
                LeaveRequest.employee_id == employee_id
            )
            .order_by(
                LeaveRequest.created_at.desc()
            )
        )

        return list(result.scalars().all())

    async def update(
        self,
        db: AsyncSession,
        leave_request: LeaveRequest,
    ) -> LeaveRequest:

        await db.commit()
        await db.refresh(leave_request)

        return leave_request