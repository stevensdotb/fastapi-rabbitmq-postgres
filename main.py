from contextlib import asynccontextmanager
from doctest import debug

from fastapi import FastAPI

from api.router import router
from api.database import db, Base
from core.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with db.engine.begin() as conn:
            if settings.debug:
                await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        yield
    finally:
        pass


app = FastAPI(
    title="Orders API",
    description="API to manage orders",
    version="1.0",
    docs_url="/api/v1/docs",
    lifespan=lifespan
)


app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=settings.debug)