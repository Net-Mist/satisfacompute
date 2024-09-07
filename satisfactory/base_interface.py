from __future__ import annotations

from collections import Counter, defaultdict

from satisfactory.dataclasses import BuildingType, Material


class BaseInterface:
    def compute(self) -> None:
        raise NotImplementedError()

    def get_energy_produced(self) -> float:
        raise NotImplementedError()

    def get_materials(self) -> defaultdict[Material, float]:
        """return the material quantities that the base has in stock
        note that the imported material are not considered here. To get them
        use get_accessed_material
        """
        raise NotImplementedError()

    def get_material(self, material: Material) -> float:
        """return the stock quantity for a specific material
        note that the imported material are not considered here. To get them
        use get_accessed_material
        """
        raise NotImplementedError()

    def get_building_count(self) -> Counter[BuildingType]:
        raise NotImplementedError()

    def get_input(self) -> list[Material]:
        raise NotImplementedError()

    def get_output(self) -> list[Material]:
        raise NotImplementedError()

    def get_accessed_material(self, material: Material) -> defaultdict[BaseInterface, float]:
        """return material that base can consume, but doesn't directly have"""
        raise NotImplementedError()

    def consume_material(self, material: Material, q: float) -> None:
        raise NotImplementedError()

    def import_from(self, other_base: BaseInterface, materials: list[Material] | None = None) -> None:
        raise NotImplementedError()
