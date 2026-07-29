import uvicorn

from app.core.config import BASE_DIR, settings
from app.core.logging import configure_logging
from app.create_app import create_app

configure_logging()

app = create_app()


# app.mount(
#     "/static",
#     StaticFiles(
#         directory=BASE_DIR / "src" / "app" / "static",
#     ),
#     name="static",
# )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
    )
