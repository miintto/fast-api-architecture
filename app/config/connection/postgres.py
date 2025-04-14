from asyncio import TimeoutError, current_task, open_connection, wait_for
import logging

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from app.config.settings import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()


class PostgresConnection:
    def __init__(self) -> None:
        self.engine = self.create_session()
        self._session = async_scoped_session(
            session_factory=async_sessionmaker(
                bind=self.engine,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False,
            ),
            scopefunc=current_task,
        )

    def create_session(self) -> AsyncEngine:
        return create_async_engine(
            url="postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}".format(
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                name=settings.DB_NAME,
            ),
            pool_size=settings.SQLALCHEMY_POOL_SIZE,
        )

    async def check_connection(self):
        try:
            await wait_for(
                open_connection(self.engine.url.host, self.engine.url.port, limit=1),
                timeout=1,
            )
        except TimeoutError:
            raise TimeoutError("Cannot connect to PostgreSQL.")

    async def dispose_connection(self):
        await self.engine.dispose()

    async def get_session(self) -> AsyncSession:
        async with self._session() as session:
            try:
                yield session
                await self._session.commit()
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()
        await self._session.remove()

    @property
    def session(self):
        return self.get_session


db = PostgresConnection()
