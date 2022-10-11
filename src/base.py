from collections import Counter

from src.data_loader import BUILDING_SPEC, RecipeModel
from src.dataclasses import Building, Material, MaterialType, Recipe
from src.logger import get_logger

logger = get_logger(__name__)


class Base:
    def __init__(self) -> None:
        self.building_count = Counter()
        self.total_energy_cost = 0
        self.material_quantities = Counter()

    def check_efficiency(self, q: int, recipe: RecipeModel, building_name: Building) -> float:
        for material, quantity in recipe.inputs.items():
            quantity_diff = self.material_quantities[material] - q * quantity
            best_q = q
            if quantity_diff < -0.01:
                better_q = self.material_quantities[material] / quantity
                logger.warning(
                    f'don\'t have enough "{material}", miss {-quantity_diff}. '
                    f"You should have {better_q:.2f} {building_name}"
                )
                if better_q < best_q:
                    best_q = better_q
        return best_q

    def add_building(
        self,
        name: Building,
        material: Material = None,
        material_type: MaterialType = None,
        recipe: Recipe = None,
        q: int = 1,
        clock_speed: float = 100,
    ) -> None:
        name = Building(name)

        self.building_count[name] += q
        building_spec = BUILDING_SPEC[name]
        # see https://satisfactory.fandom.com/wiki/Clock_speed for formula
        self.total_energy_cost += building_spec.energy_cost * q * (clock_speed / 100) ** 1.6
        q = q * (clock_speed / 100)

        if name == Building.POMPE_EAU:
            self.material_quantities[Material.EAU] += 120 * q
        elif name in (Building.FOREUSE_MK2):
            material = Material(material)
            material_type = MaterialType(material_type)
            self.material_quantities[material] += material_type * 2 * q
        else:
            recipe: RecipeModel = building_spec.recipes[Recipe(recipe)]
            q = self.check_efficiency(q, recipe, name)
            for material, quantity in recipe.inputs.items():
                self.material_quantities[material] -= q * quantity
            for material, quantity in recipe.outputs.items():
                self.material_quantities[material] += q * quantity

    def add_import(self, material: Material, q: int) -> None:
        self.material_quantities[material] += q

    def __str__(self) -> str:
        s = f"Energy consumption: {self.total_energy_cost} MW\n"
        s += "Buildings:\n"
        for k, v in self.building_count.items():
            s += f"- {k}: {v}\n"
        s += "Materials:\n"
        for k, v in self.material_quantities.items():
            if abs(v) > 0.01:
                s += f"- {k}: {v:0.2f}\n"
        return s
