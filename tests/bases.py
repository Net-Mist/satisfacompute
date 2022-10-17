import unittest
from pathlib import Path

from satisfactory import AllConnectedBase, Base, Building
from satisfactory.dataclasses import BuildingType, Material, MaterialType, Recipe
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
        self.assertEqual(base.energy_available, -5 - 4 * 0.5**1.6)

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
        self.assertEqual(base.energy_available, -5 - 4 * 0.5**1.6)


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
        self.assertEqual(base.energy_available, -5 - 4 * 0.5**1.6)


    def test_all_connected_base2(self) -> None:
        base = Base("plop")
        base.add_all_connected(
            "all_connected",
            [
                Building(
                    BuildingType.FOREUSE_MK1,
                    material=Material.MINERAI_DE_FER,
                    material_type=MaterialType.PUR,
                    label="mineur",
                ),
                Building(BuildingType.FONDERIE, Recipe.LINGOT_FER, clock_speed=50, label="fonderie v1"),
            ],
        )
        base.resolve()
        materials = base.get_material_quantities_rec()
        self.assertEqual(materials[Material.MINERAI_DE_FER], 120 - 30 / 2)
        self.assertEqual(materials[Material.LINGOT_FER], 30 / 2)
        self.assertEqual(base.energy_available, -5 - 4 * 0.5**1.6)

    def test_base_principale_vis(self) -> None:
        base = Base()
        sub_base = Base("Base principale")
        sub_base.add_all_connected(
            "RdC Vis",
            [
                Building(
                    BuildingType.FOREUSE_MK2, material=Material.MINERAI_DE_FER, material_type=MaterialType.PUR, q=1
                ),
                Building(BuildingType.FONDERIE, recipe=Recipe.LINGOT_FER, q=8),
                Building(BuildingType.CONSTRUCTEUR, recipe=Recipe.TIGE, q=6),  # RdC
                Building(BuildingType.CONSTRUCTEUR, recipe=Recipe.VIS, q=6),  # RdC
                Building(BuildingType.ASSEMBLEUSE, recipe=Recipe.ROTOR, q=3),
            ],
        )
        base.add_sub_base(sub_base)
        base.resolve()
        materials = base.get_material_quantities_rec()
        self.assertEqual(materials[Material.MINERAI_DE_FER], 0)
        self.assertEqual(materials[Material.LINGOT_FER], 150)
        self.assertEqual(materials[Material.TIGE], 0)
        self.assertEqual(materials[Material.VIS], 90)
        self.assertEqual(materials[Material.ROTOR], 6)

    def test_base_principale(self) -> None:
        base = Base()
        sub_base = Base("Base principale")
        sub_base.add_all_connected(
            "plaque",
            [
                Building(BuildingType.FOREUSE_MK1, material=Material.MINERAI_DE_FER, material_type=MaterialType.PUR, q=1),
                Building(BuildingType.FONDERIE, recipe=Recipe.LINGOT_FER, q=4),
                Building(BuildingType.CONSTRUCTEUR, recipe=Recipe.PLAQUE, q=4),
                # need import vis
                fer_renforce := Building(BuildingType.ASSEMBLEUSE, recipe=Recipe.PLAQUE_DE_FER_RENFORCEE, q=2),
                Building(BuildingType.ASSEMBLEUSE, recipe=Recipe.CADRE_MODULAIRE, q=3),
            ],
        )

        sub_base.add_all_connected(
            "RdC Vis",
            [
                Building(BuildingType.FOREUSE_MK2, material=Material.MINERAI_DE_FER, material_type=MaterialType.PUR, q=1),
                lingot_fer := Building(BuildingType.FONDERIE, recipe=Recipe.LINGOT_FER, q=8),
                Building(BuildingType.CONSTRUCTEUR, recipe=Recipe.TIGE, q=6),  # RdC
                Building(BuildingType.CONSTRUCTEUR, recipe=Recipe.VIS, q=6),  # RdC
                b := Building(BuildingType.ASSEMBLEUSE, recipe=Recipe.ROTOR, q=3, label="rotor"),
            ],
        )

        sub_base.add_all_connected(
            "1er Etage Vis",
            [
                tige_1 := Building(BuildingType.CONSTRUCTEUR, Recipe.TIGE, q=7),
                vis_1 := Building(BuildingType.CONSTRUCTEUR, Recipe.VIS, q=7),
                # export to first part
            ],
        )
        lingot_fer.export_to(tige_1, [Material.LINGOT_FER])
        vis_1.export_to(fer_renforce, [Material.VIS])
        
        base.add_sub_base(sub_base)
        base.resolve()
        base.rapport()
        plotter(base, Path.cwd() / "output.txt")