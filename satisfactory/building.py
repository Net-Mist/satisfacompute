from __future__ import annotations

from collections import Counter, defaultdict
from math import ceil, floor

from satisfactory.base_interface import BaseInterface
from satisfactory.data_loader import BUILDING_SPEC, RecipeModel
from satisfactory.dataclasses import BuildingType, Material, MaterialType, Recipe
from satisfactory.logger import get_logger

logger = get_logger(__name__)


class Merged:
    def __init__(self, connected_bases: list[GenericBuilding]) -> None:
        self.connected_bases = connected_bases

    def to(self, other_base: GenericBuilding) -> GenericBuilding:
        for base in self.connected_bases:
            base.to(other_base)
        return other_base


class GenericBuilding(BaseInterface):
    def __init__(
        self,
        building_type: BuildingType,
        label: str = "",
        clock_speed: float = 100,
        q: float = 1,
    ) -> None:
        """
        if clock_speed is 100, then assume there is `floor(q)` building at 100% efficiency and 1 at `q-floor(q)`
        efficiency else assume all q buildings have this clock speed (q need to be an integer)
        """
        if clock_speed != 100:
            assert q == floor(q)
        self.building_spec = BUILDING_SPEC[building_type]
        # see https://satisfactory.fandom.com/wiki/Clock_speed for formula
        self.energy: float = -self.building_spec.energy_cost * (
            floor(q) * (clock_speed / 100) ** 1.6 + ceil(q - floor(q)) * (q - floor(q)) ** 1.6
        )
        self.building_type = building_type
        self.label = label
        self.clock_speed = clock_speed
        self.q = q
        self.computed_q = self.q * self.clock_speed / 100

        # structure that keep track of imported materials
        # TODO move to BuildingRecipe
        self.imports: dict[BaseInterface, dict[Material, float]] = defaultdict(dict)
        # map material to exported base. These base need to be processed first at resolution time
        self.imported_resources_origin: dict[Material, list[BaseInterface]] = defaultdict(list)

        # structure useful for computation
        self.computed = False
        self.material_produced: defaultdict[Material, float] = defaultdict(lambda: 0)
        self.material_consumed: defaultdict[Material, float] = defaultdict(lambda: 0)

    def get_energy_produced(self) -> float:
        return self.energy

    def get_materials(self) -> defaultdict[Material, float]:
        d: defaultdict[Material, float] = defaultdict(lambda: 0)
        for k in self.material_produced:
            d[k] = self.material_produced[k] - self.material_consumed[k]
        return d

    def get_material(self, material: Material) -> float:
        return self.material_produced[material] - self.material_consumed[material]

    def get_building_count(self) -> Counter[BuildingType]:
        return Counter({self.building_type: ceil(self.q)})

    def consume_material(self, material: Material, q: float) -> None:
        self.material_consumed[material] += q
        if self.material_consumed[material] > self.material_produced[material]:
            raise ValueError("consume more than produced ressources")

    def import_from(self, other_base: BaseInterface, materials: list[Material] | None = None) -> None:
        if materials is None:
            materials = self.get_input()
        for material in materials:
            self.imports[other_base][material] = 0
        for material in materials:
            self.imported_resources_origin[material].append(other_base)

    def merge(self, other_building: GenericBuilding) -> Merged:
        return Merged([self, other_building])

    def to(self, other_base: GenericBuilding, materials: list[Material] | None = None) -> GenericBuilding:
        """exports other_base output to self input and returns other_base"""
        other_base.import_from(self, materials)
        return other_base


class BuildingRecipe(GenericBuilding):
    """a class that model a building with Recipe"""

    def __init__(
        self,
        building_type: BuildingType,
        recipe: Recipe,
        label: str = "",
        clock_speed: float = 100,
        q: float = 1,
    ) -> None:
        """
        if clock_speed is 100, then assume there is `floor(q)` building at 100% efficiency and 1 at `q-floor(q)`
        efficiency else assume all q buildings have this clock speed (q need to be an integer)
        """
        super().__init__(building_type, label, clock_speed, q)

        if self.building_spec.recipes is None:
            raise ValueError("This building doesn't have recipes")
        self.recipe = self.building_spec.recipes[recipe]

    def compute(self) -> None:
        if self.computed:
            return
        self.computed = True
        self.computed_q = self._check_efficiency(self.computed_q, self.recipe, self.building_type)
        for material, quantity in self.recipe.inputs.items():
            self._update_available_resources(material, self.computed_q * quantity)
        for material, quantity in self.recipe.outputs.items():
            self.material_produced[material] = self.computed_q * quantity

    def get_accessed_material(self, material: Material) -> defaultdict[BaseInterface, float]:
        bases = self.imported_resources_origin[material]
        r: defaultdict[BaseInterface, float] = defaultdict(lambda: 0)
        for base in bases:
            base.compute()
            r[base] = base.get_materials()[material]
        return r

    def _check_efficiency(self, q: float, recipe: RecipeModel, building_name: BuildingType) -> float:
        best_q = q
        for material, quantity in recipe.inputs.items():
            material_origins = self.get_accessed_material(material)
            av_resources = sum(material_origins.values())
            quantity_diff = av_resources - q * quantity
            if quantity_diff < -0.01:
                better_q = av_resources / quantity
                logger.warning(
                    f'don\'t have enough "{material}", miss {-quantity_diff}. '
                    f"You should have {better_q:.2f} {building_name}"
                )
                if better_q < best_q:
                    best_q = better_q
        return best_q

    def _update_available_resources(self, material: Material, quantity: float) -> None:
        material_origins = self.get_accessed_material(material)
        for origin, q_available in material_origins.items():
            if q_available >= quantity:
                origin.consume_material(material, quantity)
                self.imports[origin][material] += quantity
                return
            else:
                origin.consume_material(material, q_available)
                self.imports[origin][material] += q_available
                quantity -= q_available

    def get_input(self) -> list[Material]:
        return list(self.recipe.inputs.keys())

    def get_output(self) -> list[Material]:
        return list(self.recipe.outputs.keys())


class BuildingRessourceExtractor(GenericBuilding):
    """ressource extractor are special because they don't need recipe, but we need to indicate the material"""

    def __init__(
        self,
        building_type: BuildingType,
        material: Material,
        material_type: MaterialType,
        label: str = "",
        clock_speed: float = 100,
        q: float = 1,
    ) -> None:
        """
        if clock_speed is 100, then assume there is `floor(q)` building at 100% efficiency and 1 at `q-floor(q)`
        efficiency else assume all q buildings have this clock speed (q need to be an integer)
        """
        super().__init__(building_type, label, clock_speed, q)

        self.material = material
        self.material_type = material_type

    def get_input(self) -> list[Material]:
        return []

    def get_output(self) -> list[Material]:
        return [self.material]
