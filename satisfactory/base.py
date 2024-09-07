from __future__ import annotations

from collections import Counter, defaultdict

from satisfactory.base_interface import BaseInterface
from satisfactory.building import GenericBuilding
from satisfactory.dataclasses import BuildingType, Material
from satisfactory.logger import get_logger

logger = get_logger(__name__)


class GenericBase(BaseInterface):
    def __init__(self, label: str = "") -> None:
        # defined at graph construction time
        self.label = label
        self.sub_bases: list[BaseInterface] = []

        # changed at resolution time
        self.computed = False

    def get_input(self) -> list[Material]:
        raise NotImplementedError()

    def get_output(self) -> list[Material]:
        raise NotImplementedError()

    def get_accessed_material(self, material: Material) -> defaultdict[BaseInterface, float]:
        m: defaultdict[BaseInterface, float] = defaultdict(lambda: 0)
        for base in self.sub_bases:
            q = base.get_material(material)
            m[base] = q
        return m

    def get_materials(self) -> defaultdict[Material, float]:
        m: defaultdict[Material, float] = defaultdict(lambda: 0)
        for base in self.sub_bases:
            for material, quantity in base.get_materials().items():
                m[material] += quantity
        return m

    def get_material(self, material: Material) -> float:
        return sum(base.get_material(material) for base in self.sub_bases)

    def consume_material(self, material: Material, q: float) -> None:
        q = q
        for base, available_quantity in self.get_accessed_material(material).items():
            if q < available_quantity:
                base.consume_material(material, q)
                return
            base.consume_material(material, available_quantity)
            q = q - available_quantity

        if q < 0.01:
            return
        logger.warning("this line shouldn't be executed, please investigate")

    def import_from(self, other_base: BaseInterface, materials: list[Material] | None = None) -> None:
        # generic import from a base is not yet defined
        raise NotImplementedError()

    def get_energy_produced(self) -> float:
        return sum(base.get_energy_produced() for base in self.sub_bases)

    def get_building_count(self) -> Counter[BuildingType]:
        c: Counter[BuildingType] = Counter()
        for base in self.sub_bases:
            c += base.get_building_count()
        return c

    def compute(self) -> None:
        if self.computed:
            return
        self.computed = True
        for sub_base in self.sub_bases:
            sub_base.compute()


class Base(GenericBase):
    def add_building(self, building: BaseInterface) -> None:
        self.add_sub_base(building)

    def add_sub_base(self, base: BaseInterface) -> None:
        self.sub_bases.append(base)

    def add_all_connected(self, label: str, building_list: list[BaseInterface]) -> None:
        sub_base = AllConnectedBase(building_list, label)
        self.add_sub_base(sub_base)

    def __str__(self) -> str:
        s = f"Energy available: {self.get_energy_produced()} MW\n"
        s += "Buildings:\n"
        for k, v in self.get_building_count().items():
            s += f"- {k}: {v}\n"
        s += "Materials:\n"

        material_quantities = self.get_materials()

        for material, quantity in material_quantities.items():
            if abs(quantity) > 0.01:
                s += f"- {material}: {quantity:0.2f}\n"
        return s

    def rapport(self) -> None:
        print(self)


class AllConnectedBase(GenericBase):
    def __init__(self, subbase_list: list[BaseInterface] | None = None, label: str = "") -> None:
        super().__init__(label)
        self.sub_bases = subbase_list if subbase_list is not None else []
        self.connect_sub_bases()

    def add_building(self, building: BaseInterface) -> None:
        self.sub_bases.append(building)
        self.connect_one_with_previous(len(self.sub_bases) - 1)

    def get_input(self) -> list[Material]:
        return self.sub_bases[0].get_input()

    def get_output(self) -> list[Material]:
        return self.sub_bases[-1].get_output()

    def connect_sub_bases(self) -> None:
        for i, _ in enumerate(self.sub_bases):
            self.connect_one_with_previous(i)

    def connect_one_with_previous(self, i: int) -> None:
        material_to_import = self.sub_bases[i].get_input()

        for material in material_to_import:
            for previous_base in self.sub_bases[:i]:
                if material in previous_base.get_output():
                    self.connect_2_sub_bases(previous_base, self.sub_bases[i], [material])

    def connect_2_sub_bases(self, from_base: BaseInterface, to_base: BaseInterface, material: list[Material]) -> None:
        # for now only building can be connected
        if isinstance(from_base, GenericBase):
            self.connect_2_sub_bases(from_base.sub_bases[-1], to_base, material)
        elif isinstance(to_base, GenericBase):
            self.connect_2_sub_bases(from_base, to_base.sub_bases[0], material)
        elif isinstance(to_base, GenericBuilding) and isinstance(from_base, GenericBuilding):
            from_base.to(to_base, material)
        else:
            raise ValueError("unknown types for from_base and to_base")
