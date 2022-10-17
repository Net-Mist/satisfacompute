from __future__ import annotations

from collections import Counter, defaultdict
from math import floor

from .data_loader import BUILDING_SPEC, RecipeModel
from .dataclasses import BuildingType, Material, MaterialType, Recipe
from .logger import get_logger

logger = get_logger(__name__)


class GenericBase:
    def __init__(self, label: str = "") -> None:
        # defined at graph construction time
        self.label = label
        self.sub_bases: list[GenericBase] = []
        self.parent_base: GenericBase | None = None
        self.imports: dict[GenericBase, dict[Material, float]] = defaultdict(dict)
        self.imported_resources_origin: dict[Material, list[GenericBase]] = defaultdict(list)

        # changed at resolution time
        self.computed = False
        self.building_count: Counter[Building] = Counter()  # counter of all building in base and sub-bases
        self.energy_available: float = 0
        self.material_quantities: defaultdict[Material, float] = defaultdict(
            lambda: 0
        )  # counter for the number of non-consumed materials

    def export_to(self, other_base: GenericBase, materials: list[Material] | None = None) -> None:
        if materials is None:
            if type(self) == Building:
                materials = self.outputs
            else:
                raise ValueError("materials need to be define if not a building")
        materials = [Material(i) for i in materials]
        for material in materials:
            other_base.imports[self][material] = 0
        for material in materials:
            other_base.imported_resources_origin[material].append(self)

    def import_from(self, other_base: GenericBase, materials: list[Material] | None) -> None:
        other_base.export_to(self, materials)

    def _building_count_rec_add(self, building: BuildingType, q: int) -> None:
        self.building_count[building] += q
        if self.parent_base:
            self.parent_base._building_count_rec_add(building, q)

    def _energy_available_rec_update(self, q: float) -> None:
        self.energy_available += q
        if self.parent_base:
            self.parent_base._energy_available_rec_update(q)

    def _get_available_resources(self, material: Material) -> float:
        r = self.material_quantities[material]
        # check all imports
        for base in self.imported_resources_origin[material]:
            r += base._get_available_resources(material)
        return r

    def _update_available_resources(self, material: Material, q: float) -> None:
        # first consume local resources
        diff = self.material_quantities[material] - q
        if diff >= 0:
            self.material_quantities[material] = diff
            return
        else:
            self.material_quantities[material] = 0
            q = -diff
            # update importing bases
            for base in self.imported_resources_origin[material]:
                av_resources = base._get_available_resources(material)
                if av_resources >= q:
                    base._update_available_resources(material, q)
                    self.imports[base][material] += q
                    return
                base._update_available_resources(material, av_resources)
                self.imports[base][material] += av_resources
                q -= av_resources
        if q < 0.01:
            return
        logger.warning("this line shouldn't be executed, please investigate")

    def resolve(self) -> None:
        self._pre_compute_hook()
        self._compute()

    def _compute(self) -> None:
        if self.computed:
            return
        self.computed = True
        # first resolve imports
        for k in self.imports.keys():
            if not k.computed:
                k._compute()
        # then compute all sub_bases
        for i, sub_base in enumerate(self.sub_bases):
            if not sub_base.computed:
                self._pre_sub_base_hook(sub_base, i)
                sub_base._compute()

    def _pre_compute_hook(self) -> None:
        for base in self.sub_bases:
            base._pre_compute_hook()

    def _pre_sub_base_hook(self, sub_base: GenericBase, i: int) -> None:
        pass

    def get_material_quantities_rec(self) -> Counter:
        material_quantities = self.material_quantities
        for base in self.sub_bases:
            material_quantities += base.get_material_quantities_rec()
        return material_quantities


class Building(GenericBase):
    def __init__(
        self,
        building_type: BuildingType | str,
        recipe: Recipe | str = None,
        material: Material | str = None,
        material_type: MaterialType | str = None,
        label: str = None,
        clock_speed: float = 100,
        q: float = 1,
    ) -> None:
        """
        if clock_speed is 100, then assume there is `floor(q)` building at 100% efficiency and 1 at `q-floor(q)`
        efficiency
        else, then assume all q buildings have this clock speed (q need to be an integer)
        """
        super().__init__(label)
        self.building_type = BuildingType(building_type)
        self.building_spec = BUILDING_SPEC[self.building_type]
        self.clock_speed = clock_speed
        self.q = q

        # material and material_type are for foreuse only
        self.material = Material(material) if material else None
        self.material_type = MaterialType(material_type) if material_type else None

        # special case for water
        if building_type == BuildingType.POMPE_EAU:
            self.material = Material.EAU

        # for other buildings
        self.recipe = self.building_spec.recipes[Recipe(recipe)] if recipe else None

        self.outputs = [self.material] if self.material else self.recipe.outputs

    def _compute(self) -> None:
        super()._compute()
        # update number of buildings
        self._building_count_rec_add(self.building_type, self.q)

        if self.clock_speed != 100:
            # see https://satisfactory.fandom.com/wiki/Clock_speed for formula
            assert self.q == floor(self.q)
            self._energy_available_rec_update(
                -self.building_spec.energy_cost * self.q * (self.clock_speed / 100) ** 1.6
            )
        else:
            self._energy_available_rec_update(-self.building_spec.energy_cost * floor(self.q))
            self._energy_available_rec_update(
                -self.building_spec.energy_cost * (self.q - floor(self.q)) * (self.clock_speed / 100) ** 1.6
            )

        q = self.q * self.clock_speed / 100

        self.computed_q = q
        if self.building_type == BuildingType.POMPE_EAU:
            self.material_quantities[Material.EAU] += 120 * q
        elif self.building_type == BuildingType.FOREUSE_MK2:
            self.material_quantities[self.material] += self.material_type * 2 * q
        elif self.building_type == BuildingType.FOREUSE_MK1:
            self.material_quantities[self.material] += self.material_type * 1 * q
        else:
            self.computed_q = self._check_efficiency(q, self.recipe, self.building_type)
            for material, quantity in self.recipe.inputs.items():
                self._update_available_resources(material, self.computed_q * quantity)
            for material, quantity in self.recipe.outputs.items():
                self.material_quantities[material] += self.computed_q * quantity

    def _check_efficiency(self, q: int, recipe: RecipeModel, building_name: BuildingType) -> float:
        best_q = q
        for material, quantity in recipe.inputs.items():
            av_resources = self._get_available_resources(material)
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


class Base(GenericBase):
    def create_building(
        self,
        building_type: BuildingType | str,
        recipe: Recipe | str | None = None,
        material: Material | str | None = None,
        material_type: MaterialType | str | None = None,
        label: str | None = None,
        clock_speed: float = 100,
        q: int = 1,
    ) -> Building:
        building = Building(building_type, recipe, material, material_type, label, clock_speed, q)
        self.add_building(building)
        return building

    def add_building(self, building: Building) -> None:
        self.sub_bases.append(building)
        building.parent_base = self

    def add_sub_base(self, base: GenericBase) -> None:
        self.sub_bases.append(base)
        base.parent_base = self

    def add_all_connected(self, label: str, building_list: list[Building]) -> None:
        sub_base = AllConnectedBase(label)
        for building in building_list:
            sub_base.add_building(building)
        self.add_sub_base(sub_base)

    def __str__(self) -> str:
        s = f"Energy available: {self.energy_available} MW\n"
        s += "Buildings:\n"
        for k, v in self.building_count.items():
            s += f"- {k}: {v}\n"
        s += "Materials:\n"

        material_quantities = self.get_material_quantities_rec()

        for k, v in material_quantities.items():
            if abs(v) > 0.01:
                s += f"- {k}: {v:0.2f}\n"
        return s

    def get_material_quantities_rec(self) -> Counter:
        material_quantities = Counter()
        for base in self.sub_bases:
            material_quantities += base.get_material_quantities_rec()
        return material_quantities

    def _compute(self) -> None:
        super()._compute()

    def rapport(self) -> None:
        print(self)


class AllConnectedBase(Base):
    def _pre_compute_hook(self) -> None:
        super()._pre_compute_hook()

        # connect the buildings
        for i, sub_base in enumerate(self.sub_bases):
            if sub_base.recipe is None:
                continue
            material_to_import = sub_base.recipe.inputs.keys()

            for previous_building in self.sub_bases[:i]:
                for material in material_to_import:
                    if material in previous_building.outputs:
                        previous_building.export_to(sub_base, [material])
