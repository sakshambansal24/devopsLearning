from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import Base, create_database_engine, create_session_factory, get_db
from app.models import User
from app.schemas import HealthRead, UserCreate, UserRead


def create_app(database_url: str | None = None) -> FastAPI:
    settings = get_settings()
    engine = create_database_engine(database_url or settings.database_url)
    session_factory = create_session_factory(engine)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        Base.metadata.create_all(bind=engine)
        yield
        engine.dispose()

    app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)

    async def db_dependency() -> AsyncGenerator[Session, None]:
        async for db in get_db(session_factory):
            yield db

    @app.get("/health", response_model=HealthRead)
    async def health() -> HealthRead:
        return HealthRead(status="ok")

    @app.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
    async def create_user(
        payload: UserCreate,
        db: Session = Depends(db_dependency),
    ) -> User:
        user = User(name=payload.name, email=str(payload.email))
        db.add(user)

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email already exists.",
            ) from None

        db.refresh(user)
        return user

    @app.get("/users", response_model=list[UserRead])
    async def list_users(db: Session = Depends(db_dependency)) -> list[User]:
        return list(db.scalars(select(User).order_by(User.id)).all())

    return app


app = create_app()
