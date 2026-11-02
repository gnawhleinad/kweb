from itertools import chain
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse

from ..config import Config

# from . import __version__ as version

router = APIRouter()
templates = Jinja2Templates(
    directory=(Path(__file__).parent.parent / "templates").resolve()
)


@router.get("/", response_class=HTMLResponse)
async def file_browser(
    request: Request,
) -> _TemplateResponse:
    dependency = router.dependencies[0].dependency
    assert dependency is not None
    settings: Config = dependency()

    files = chain(
        settings.fileslocation.glob("**/*.gds"), settings.fileslocation.glob("**/*.oas")
    )
    return templates.TemplateResponse(
        request,
        "browser.html",
        {
            "folder_files": [
                file.relative_to(settings.fileslocation) for file in files
            ],
            "page_name": f"File Browser    Root: {settings.fileslocation}",
            "root": settings.fileslocation,
        },
    )
