from dataclasses import asdict
from typing import TypeVar, overload

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapter.outbound.persistence.entity.base import Base
from app.config.connection import db

T = TypeVar("T", bound=Base)


class BaseRepository:
    def __init__(self, session: AsyncSession = Depends(db.session)):
        self._session = session

    @overload
    async def _save(self, domain, entity: type[T]) -> T:
        ...

    async def _save(self, domain, entity: type[Base]) -> Base:
        if not domain.id:
            model = entity.from_domain(domain)
            self._session.add(model)
        else:
            model = await self._session.get(entity, domain.id)
            for field, value in asdict(domain).items():
                if isinstance(value, list):
                    continue
                setattr(model, field, value)
        await self._session.commit()
        return model

    @overload
    async def _find_by_id_or_none(self, id_: int, entity: type[T]) -> T | None:
        ...

    async def _find_by_id_or_none(
        self, id_: int, entity: type[Base]
    ) -> Base | None:
        result = await self._session.execute(
            select(entity).where(entity.id == id_)
        )
        return result.scalar_one_or_none()
