from typing import List, Optional
from urllib.parse import urljoin

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from fastapi.exceptions import HTTPException

from .models import Currency, Item, Province


class Scraper:
    BASE_URL = "https://comohay.com"
    PARSER = "html.parser"

    @staticmethod
    async def get_autocomplete(query: str) -> List[str]:
        async with ClientSession() as session:
            url = urljoin(Scraper.BASE_URL, "search/autocomplete")
            async with session.get(url, params={"q": query}) as response:
                print(f"Request URL: {response.url}")
                if response.status != 200:
                    raise HTTPException(
                        status_code=response.status,
                        detail=response.reason,
                    )
                json = await response.json()
                return json["results"]

    @staticmethod
    async def get_items(
        query: str,
        page: int,
        provinces: Optional[List[Province]],
        price_from: Optional[int],
        price_to: Optional[int],
        price_currency: Optional[Currency],
    ) -> List[Item]:
        async with ClientSession() as session:
            url = urljoin(Scraper.BASE_URL, "")
            params = {"q": query, "page": page}
            if provinces:
                params["provinces"] = [province.value for province in provinces]
            if price_from is not None:
                params["price_from"] = price_from
            if price_to is not None:
                params["price_to"] = price_to
            if price_currency is not None:
                params["price_currency"] = price_currency.value
            async with session.get(url, params=params) as response:
                print(f"Request URL: {response.url}")
                if response.status != 200:
                    raise HTTPException(
                        status_code=response.status,
                        detail=response.reason,
                    )
                soup = BeautifulSoup(await response.text(), Scraper.PARSER)
                items = soup.find_all("div", class_="list-item-container")
                result: List[Item] = []
                for item in items:
                    header = item.find("div", class_="list-item-header")
                    source = header.find("span", class_="list-item-badge").text.strip()
                    date = header.find_all("span")[1].text.strip()
                    url = item.find("div", class_="list-item-title").a["href"]
                    title = item.find("div", class_="list-item-title").a.text.strip()
                    location = " ".join(
                        filter(
                            lambda x: x,
                            item.find("div", class_="list-item-location")
                            .span.text.strip()
                            .replace("\n", " ")
                            .replace("\t", " ")
                            .split(" "),
                        )
                    )
                    price = item.find("div", class_="list-item-price")
                    price = price.h3.text.strip() if price else price
                    description = (
                        " ".join(
                            filter(
                                lambda x: x,
                                item.find("div", class_="list-item-description")
                                .get_text()
                                .strip()
                                .replace("\n", " ")
                                .replace("\t", " ")
                                .split(" "),
                            )
                        )
                        .replace(",", ", ")
                        .replace(",  ", ", ")
                        .replace(";", "; ")
                        .replace(";  ", "; ")
                        .replace(".", ". ")
                        .replace(".  ", ". ")
                        .replace(":", ": ")
                        .replace(":  ", ": ")
                        .replace(". . .", "...")
                    ).strip()
                    result.append(
                        Item(
                            source=source,
                            date=date,
                            url=url,
                            title=title,
                            location=location,
                            price=price,
                            description=description,
                        )
                    )
                return result

    @staticmethod
    async def get_total() -> int:
        async with ClientSession() as session:
            url = urljoin(Scraper.BASE_URL, "")
            async with session.get(url) as response:
                print(f"Request URL: {response.url}")
                if response.status != 200:
                    raise HTTPException(
                        status_code=response.status,
                        detail=response.reason,
                    )
                soup = BeautifulSoup(await response.text(), Scraper.PARSER)
                try:
                    item = soup.select_one(
                        "#search-form > div.center-content.ads-quantity > span"
                    )
                    total = int(item.get_text().strip().split(" ")[0])
                except Exception as e:
                    print(f"Exception: {e}")
                    raise HTTPException(status_code=500, detail="Error getting total")
                return total
