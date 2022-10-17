from pathlib import Path

import pydantic
import yaml

from .dataclasses import BuildingType, Material, Recipe

DATA_FILE = Path(__file__).parent / "data.yaml"


class RecipeModel(pydantic.BaseModel):
    """
    inputs and outputs are dictionary mapping the material to the quantity per hour
    """

    inputs: dict[Material, float]
    outputs: dict[Material, float] = {}  # for electricity producer, output is not mandatory


class BuildingModel(pydantic.BaseModel):
    energy_cost: int  # in MW
    recipes: dict[Recipe, RecipeModel] | None  # recipes are optional because some buildings (foreuse) don't have


class ConfModel(pydantic.BaseModel):
    buildings: dict[BuildingType, BuildingModel]


BUILDING_SPEC = ConfModel(**yaml.safe_load(DATA_FILE.read_text())).buildings
