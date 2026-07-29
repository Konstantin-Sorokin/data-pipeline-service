from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_helper import db_helper
from app.core.unit_of_work import UnitOfWork


async def get_uow(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UnitOfWork:
    return UnitOfWork(session)


UOW_Dep = Annotated[UnitOfWork, Depends(get_uow)]
