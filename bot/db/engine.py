from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import config

engine = create_async_engine(
    config.DB_URL,
    echo=config.DB_ECHO,
    # pool_size=5,
    # max_overflow=10,
)

session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
