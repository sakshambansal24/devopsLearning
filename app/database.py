from collections.abc import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool


class Base(DeclarativeBase):
    pass


def create_database_engine(database_url: str) -> Engine:
    engine_options = {"pool_pre_ping": True}

    if database_url.startswith("sqlite"):
        engine_options["connect_args"] = {"check_same_thread": False}

        if ":memory:" in database_url:
            engine_options["poolclass"] = StaticPool

    return create_engine(database_url, **engine_options)


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)


async def get_db(
    session_factory: sessionmaker[Session],
) -> AsyncGenerator[Session, None]:
    db = session_factory()
    try:
        yield db
    finally:
        db.close()
