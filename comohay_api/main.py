from os.path import join

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

from .api.v1.main import api as api_v1

app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/api/v1", api_v1)


@app.get("/", include_in_schema=False)
def index(request: Request):
    return RedirectResponse(join(request.url.path, "api", "v1", "docs"))
