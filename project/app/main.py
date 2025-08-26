import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import APIRouter, FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from tortoise import Tortoise

from app.api.app import user_router, workspace_router, board_router, column_router, task_router
from app.app_config import app_settings
from app.modules.database_module.settings import module_settings
from app.schemas.base_schema import BaseException

logger = logging.getLogger(__name__)


def application_service_handler(_: Request, exception: Exception) -> JSONResponse:
    if isinstance(exception, BaseException):
        return JSONResponse(
            status_code=exception.status_code,
            content=jsonable_encoder(
                obj=exception.detail,
                exclude_none=True,
            ),
        )

    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(
            obj=exception,
            exclude_none=True,
        ),
    )


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Init Tortoise
    await Tortoise.init(
        db_url=module_settings.database_url,
        modules={"default": ["app.modules.database_module.models.default"]},
    )

    yield
    await Tortoise.close_connections()


def create_app() -> FastAPI:
    application = FastAPI(
        title="kanban Antonio",
        description="Copy trello basic api",
        version=app_settings.api_version,
        lifespan=lifespan,
    )

    # Middlewares
    # Add CORS origins
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Handlers
    application.add_exception_handler(BaseException, application_service_handler)

    # Routes
    api_version_router = APIRouter()

    api_version_router.include_router(user_router, prefix="/users", tags=["User"])
    api_version_router.include_router(workspace_router, prefix="/workspaces", tags=["Workspace"])
    api_version_router.include_router(board_router, prefix="/boards", tags=["Board"])
    api_version_router.include_router(column_router, prefix="/columns", tags=["Column"])
    api_version_router.include_router(task_router, prefix="/tasks", tags=["Task"])

    application.include_router(
        api_version_router, prefix=f"/api/v{app_settings.api_version}"
    )
    return application


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
