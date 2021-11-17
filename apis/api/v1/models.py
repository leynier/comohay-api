from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Currency(str, Enum):
    CUP = "CUP"
    CUC = "CUC"


class Province(str, Enum):
    PinardelRío = "Pinar del Río"
    Artemisa = "Artemisa"
    LaHabana = "La Habana"
    Mayabeque = "Mayabeque"
    Matanzas = "Matanzas"
    VillaClara = "Villa Clara"
    Cienfuegos = "Cienfuegos"
    SanctiSpíritus = "Sancti Spíritus"
    CiegodeÁvila = "Ciego de Ávila"
    Camagüey = "Camagüey"
    LasTunas = "Las Tunas"
    Holguín = "Holguín"
    Granma = "Granma"
    SantiagodeCuba = "Santiago de Cuba"
    Guantánamo = "Guantánamo"


class Item(BaseModel):
    source: str
    date: str
    url: str
    title: str
    location: str
    price: Optional[str]
    description: str
