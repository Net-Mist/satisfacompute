import unittest
from pathlib import Path

from satisfactory.base import AllConnectedBase, Base
from satisfactory.dataclasses import Material, MaterialType, Recipe
from satisfactory.plotter import plotter
from satisfactory.specific_buildings import Assembleuse, Constructeur, Fonderie, ForeuseMK1, ForeuseMK2


class TestBase(unittest.TestCase):
    def test_add_building(self) -> None:
        base = Base()
        foreuse = ForeuseMK1(Material.MINERAI_DE_FER, MaterialType.PUR, label="mine_plaque")
        base.add_building(foreuse)
        fonderie = Fonderie(Recipe.LINGOT_FER, clock_speed=50, label="foreuse_plaque")
        base.add_building(fonderie)
        foreuse.to(fonderie, [Material.MINERAI_DE_FER])
        base.compute()
        self.assertEqual(foreuse.get_material(Material.MINERAI_DE_FER), 120 - 30 / 2)
        self.assertEqual(fonderie.get_material(Material.LINGOT_FER), 30 / 2)
        self.assertEqual(base.get_energy_produced(), -5 - 4 * 0.5**1.6)

    def test_all_connected_base(self) -> None:
        base = Base()
        all_connected = AllConnectedBase()
        foreuse = ForeuseMK1(Material.MINERAI_DE_FER, MaterialType.PUR, label="mine_plaque")
        fonderie = Fonderie(Recipe.LINGOT_FER, clock_speed=50, label="foreuse_plaque")
        all_connected.add_building(foreuse)
        all_connected.add_building(fonderie)
        base.add_sub_base(all_connected)
        base.compute()
        self.assertEqual(foreuse.get_material(Material.MINERAI_DE_FER), 120 - 30 / 2)
        self.assertEqual(fonderie.get_material(Material.LINGOT_FER), 30 / 2)
        self.assertEqual(base.get_energy_produced(), -5 - 4 * 0.5**1.6)

    def test_all_connected_base2(self) -> None:
        base = Base("plop")
        base.add_all_connected(
            "all_connected",
            [
                ForeuseMK1(Material.MINERAI_DE_FER, MaterialType.PUR, label="mine_plaque"),
                Fonderie(Recipe.LINGOT_FER, clock_speed=50, label="foreuse_plaque"),
            ],
        )
        base.compute()
        materials = base.get_materials()
        self.assertEqual(materials[Material.MINERAI_DE_FER], 120 - 30 / 2)
        self.assertEqual(materials[Material.LINGOT_FER], 30 / 2)
        self.assertEqual(base.get_energy_produced(), -5 - 4 * 0.5**1.6)

    def test_base_principale_vis(self) -> None:
        base = Base()
        sub_base = Base("Base principale")
        sub_base.add_all_connected(
            "RdC Vis",
            [
                ForeuseMK2(Material.MINERAI_DE_FER, MaterialType.PUR),
                Fonderie(Recipe.LINGOT_FER, q=8),
                Constructeur(Recipe.TIGE, q=6),  # RdC
                Constructeur(Recipe.VIS, q=6),  # RdC
                Assembleuse(Recipe.ROTOR, q=3),
            ],
        )
        base.add_sub_base(sub_base)
        base.compute()
        materials = base.get_materials()
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
                ForeuseMK1(material=Material.MINERAI_DE_FER, material_type=MaterialType.PUR),
                Fonderie(recipe=Recipe.LINGOT_FER, q=4),
                Constructeur(recipe=Recipe.PLAQUE, q=4),
                # need import vis
                fer_renforce := Assembleuse(recipe=Recipe.PLAQUE_DE_FER_RENFORCEE, q=2),
                Assembleuse(recipe=Recipe.CADRE_MODULAIRE, q=3),
            ],
        )

        sub_base.add_all_connected(
            "RdC Vis",
            [
                ForeuseMK2(material=Material.MINERAI_DE_FER, material_type=MaterialType.PUR),
                lingot_fer := Fonderie(recipe=Recipe.LINGOT_FER, q=8),
                Constructeur(recipe=Recipe.TIGE, q=6),  # RdC
                Constructeur(recipe=Recipe.VIS, q=6),  # RdC
                Assembleuse(recipe=Recipe.ROTOR, q=3, label="rotor"),
            ],
        )

        sub_base.add_all_connected(
            "1er Etage Vis",
            [
                tige_1 := Constructeur(Recipe.TIGE, q=7),
                vis_1 := Constructeur(Recipe.VIS, q=7),
                # export to first part
            ],
        )
        lingot_fer.to(tige_1, [Material.LINGOT_FER])
        vis_1.to(fer_renforce, [Material.VIS])

        base.add_sub_base(sub_base)
        base.compute()
        base.rapport()
        plotter(base, Path.cwd() / "output.txt")

    def test_internal_all_connected(self) -> None:
        base = Base()
        base.add_all_connected(
            "filactif",
            [
                AllConnectedBase(
                    [
                        ForeuseMK2(Material.MINERAI_DE_CATERIUM, MaterialType.NORMAL),
                        Fonderie(Recipe.LINGOT_CATERIUM, q=2.6666),
                    ]
                ),
                AllConnectedBase(
                    [
                        ForeuseMK2(Material.MINERAI_DE_CATERIUM, MaterialType.PUR),
                        Fonderie(Recipe.LINGOT_CATERIUM, q=5),
                    ]
                ),
                Constructeur(Recipe.FILACTIF, q=6),
            ],
        )
        base.compute()
        materials = base.get_materials()
        self.assertEqual(materials[Material.FILACTIF], 360)
