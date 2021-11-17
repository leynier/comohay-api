from os.path import join
from typing import List, Optional

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


@api.get("/items", response_model=List[Item], tags=["General"])
async def get_items(
    query: str,
    page: int = 1,
    provinces: Optional[List[Province]] = Query(None),
    price_from: Optional[int] = None,
    price_to: Optional[int] = None,
    price_currency: Optional[Currency] = None,
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


@api.get("/autocomplete", response_model=List[str], tags=["General"])
async def get_autocomplete(query: str):
    items = await Scraper.get_autocomplete(query=query)
    return items


@api.get("/currencies", response_model=List[Currency], tags=["General"])
def get_currencies():
    currencies = [currency for currency in Currency]
    return currencies


@api.get("/provinces", response_model=List[Province], tags=["General"])
def get_provinces():
    provinces = [province for province in Province]
    return provinces


@api.get("/total", response_model=int, tags=["General"])
async def get_total():
    return await Scraper.get_total()
