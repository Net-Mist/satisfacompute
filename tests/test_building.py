from unittest import TestCase

from satisfactory import Constructeur, Fonderie, ForeuseMK2, Material, MaterialType, Recipe


class TestSingleBuilding(TestCase):
    def test_2_building(self) -> None:
        a = ForeuseMK2(Material.MINERAI_DE_FER, MaterialType.PUR)
        b = Fonderie(Recipe.LINGOT_FER)
        a.to(b)
        b.compute()
        self.assertEqual(b.get_materials()[Material.LINGOT_FER], 30)
        self.assertEqual(b.get_material(Material.LINGOT_FER), 30)
        self.assertEqual(a.get_material(Material.MINERAI_DE_FER), 240 - 30)

    def test_set_similar_building(self) -> None:
        a = ForeuseMK2(Material.MINERAI_DE_FER, MaterialType.PUR)
        b = Fonderie(Recipe.LINGOT_FER, q=8)
        a.to(b)
        b.compute()
        self.assertEqual(b.get_materials()[Material.LINGOT_FER], 240)
        self.assertEqual(b.get_material(Material.LINGOT_FER), 240)
        self.assertEqual(a.get_material(Material.MINERAI_DE_FER), 0)

    def test_set_similar_building_more_than_needed(self) -> None:
        a = ForeuseMK2(Material.MINERAI_DE_FER, MaterialType.PUR)
        b = Fonderie(Recipe.LINGOT_FER, q=10)
        a.to(b)
        b.compute()
        self.assertEqual(b.get_materials()[Material.LINGOT_FER], 240)
        self.assertEqual(b.get_material(Material.LINGOT_FER), 240)
        self.assertEqual(a.get_material(Material.MINERAI_DE_FER), 0)
        self.assertEqual(b.q, 10)
        self.assertEqual(b.computed_q, 8)

    def test_to(self) -> None:
        a = ForeuseMK2(Material.MINERAI_DE_FER, MaterialType.PUR).to(Fonderie(Recipe.LINGOT_FER, q=8))
        a.compute()
        self.assertEqual(a.get_materials()[Material.LINGOT_FER], 240)
        self.assertEqual(a.get_material(Material.LINGOT_FER), 240)

    def test_merge(self) -> None:
        a = (
            ForeuseMK2(Material.MINERAI_DE_CATERIUM, MaterialType.NORMAL)
            .to(Fonderie(Recipe.LINGOT_CATERIUM, q=2.6666))
            .merge(ForeuseMK2(Material.MINERAI_DE_CATERIUM, MaterialType.PUR).to(Fonderie(Recipe.LINGOT_CATERIUM, q=5)))
            .to(Constructeur(Recipe.FILACTIF, q=6))
        )
        a.compute()
        self.assertEqual(a.get_materials()[Material.FILACTIF], 360)
