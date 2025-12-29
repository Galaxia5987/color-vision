from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles


def mount_frontend(app: FastAPI) -> None:
    """Mount the built Vue frontend if available."""

    backend_dir = Path(__file__).resolve().parent
    dist_dir = (backend_dir.parent / "frontend" / "dist").resolve()
    if dist_dir.exists():
        app.mount("/", StaticFiles(directory=dist_dir, html=True), name="frontend")
    else:

        @app.get("/")
        async def missing_frontend() -> JSONResponse:  # type: ignore[func-returns-value]
            return JSONResponse(
                {
                    "message": f"Frontend build not found at {dist_dir}. Run `npm run build` inside frontend."
                },
                status_code=200,
            )