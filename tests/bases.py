import unittest

from satisfactory import AllConnectedBase, Base, Building
from satisfactory.dataclasses import BuildingType, Material, MaterialType, Recipe
from pathlib import Path 
from satisfactory.plotter import plotter

class TestBase(unittest.TestCase):
    def test_create_building(self) -> None:
        base = Base()
        foreuse = base.create_building(
            BuildingType.FOREUSE_MK1,
            material=Material.MINERAI_DE_FER,
            material_type=MaterialType.PUR,
            label="mine_plaque",
        )
        fonderie = base.create_building(
            BuildingType.FONDERIE,
            Recipe.LINGOT_FER,
            clock_speed=50,
            label="foreuse_plaque",
        )
        foreuse.export_to(fonderie, [Material.MINERAI_DE_FER])
        base.resolve()

        self.assertEqual(foreuse.material_quantities[Material.MINERAI_DE_FER], 120 - 30 / 2)
        self.assertEqual(fonderie.material_quantities[Material.LINGOT_FER], 30 / 2)

    def test_add_building(self) -> None:
        base = Base()
        foreuse = Building(
            BuildingType.FOREUSE_MK1,
            material=Material.MINERAI_DE_FER,
            material_type=MaterialType.PUR,
            label="mine_plaque",
        )
        base.add_building(foreuse)
        fonderie = Building(BuildingType.FONDERIE, recipe=Recipe.LINGOT_FER, clock_speed=50, label="foreuse_plaque")
        base.add_building(fonderie)
        foreuse.export_to(fonderie, [Material.MINERAI_DE_FER])
        base.resolve()
        self.assertEqual(foreuse.material_quantities[Material.MINERAI_DE_FER], 120 - 30 / 2)
        self.assertEqual(fonderie.material_quantities[Material.LINGOT_FER], 30 / 2)

    def test_all_connected_base(self) -> None:
        base = Base()
        all_connected = AllConnectedBase()
        foreuse = all_connected.create_building(
            BuildingType.FOREUSE_MK1,
            material=Material.MINERAI_DE_FER,
            material_type=MaterialType.PUR,
            label="mine_plaque",
        )
        fonderie = all_connected.create_building(
            BuildingType.FONDERIE,
            Recipe.LINGOT_FER,
            clock_speed=50,
            label="foreuse_plaque",
        )
        base.add_sub_base(all_connected)
        base.resolve()
        self.assertEqual(foreuse.material_quantities[Material.MINERAI_DE_FER], 120 - 30 / 2)
        self.assertEqual(fonderie.material_quantities[Material.LINGOT_FER], 30 / 2)

    def test_all_connected_base2(self) -> None:
        base = Base("plop")
        base.add_all_connected("all_connected",
            [
                Building(
                    BuildingType.FOREUSE_MK1,
                    material=Material.MINERAI_DE_FER,
                    material_type=MaterialType.PUR,
                    label="mineur"
                ),
                Building(
                    BuildingType.FONDERIE,
                    Recipe.LINGOT_FER,
                    clock_speed=50,
                    label="fonderie v1"
                ),
            ]
        )
        base.resolve()
        base.rapport()
        materials = base.get_material_quantities_rec()
        self.assertEqual(materials[Material.MINERAI_DE_FER], 120 - 30 / 2)
        self.assertEqual(materials[Material.LINGOT_FER], 30 / 2)
        plotter(base, Path.cwd() / "output.txt")
