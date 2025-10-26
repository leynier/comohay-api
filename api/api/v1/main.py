from os.path import join

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.param_functions import Query
from fastapi.responses import RedirectResponse

from .core import Scraper
from .models import Currency, Item, Province

api = FastAPI(title="ComoHay API", version="1.0.0")
api.add_middleware(CORSMiddleware, allow_origins=["*"])


@api.get("/", include_in_schema=False, tags=["General"])
def index(request: Request):
    return RedirectResponse(join(request.url.path, "docs"))


@api.get("/items", response_model=list[Item], tags=["General"])
async def get_items(
    query: str,
    page: int = 1,
    provinces: list[Province] | None = Query(None),
    price_from: int | None = None,
    price_to: int | None = None,
    price_currency: Currency | None = None,
):
    items = await Scraper.get_items(
        query=query,
        page=page,
        provinces=provinces,
        price_from=price_from,
        price_to=price_to,
        price_currency=price_currency,
    )
    return items


@api.get("/autocomplete", response_model=list[str], tags=["General"])
async def get_autocomplete(query: str):
    items = await Scraper.get_autocomplete(query=query)
    return items


@api.get("/currencies", response_model=list[Currency], tags=["General"])
def get_currencies():
    currencies = list(Currency)
    return currencies


@api.get("/provinces", response_model=list[Province], tags=["General"])
def get_provinces():
    provinces = list(Province)
    return provinces


@api.get("/total", response_model=int, tags=["General"])
async def get_total():
    return await Scraper.get_total()
