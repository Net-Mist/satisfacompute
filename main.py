from src.base import Base
from src.dataclasses import Building, Material, MaterialType, Recipe
from src.logger import get_logger

logger = get_logger(__name__)


def base_acier() -> None:
    base = Base()
    base.add_building(Building.FOREUSE_MK2, material=Material.MINERAI_DE_FER, material_type=MaterialType.PUR, q=2)
    base.add_building(Building.FOREUSE_MK2, material=Material.CHARBON, material_type=MaterialType.PUR, q=2)

    # poutre
    base.add_building(Building.FONDERIE_AVANCEE, recipe=Recipe.LINGOT_ACIER, q=6)
    base.add_building(Building.CONSTRUCTEUR, recipe=Recipe.POUTRE_ACIER, q=4)
    base.add_building(Building.CONSTRUCTEUR, recipe=Recipe.POUTRE_ACIER, q=1, clock_speed=50)

    # tuyau
    base.add_building(Building.FONDERIE_AVANCEE, recipe=Recipe.LINGOT_ACIER, q=4)
    base.add_building(Building.FONDERIE_AVANCEE, recipe=Recipe.LINGOT_ACIER, q=1, clock_speed=66.6667)
    base.add_building(Building.CONSTRUCTEUR, recipe=Recipe.TUYAU_ACIER, q=7)

    base.add_building(
        Building.FOREUSE_MK2, material=Material.CALCAIRE, material_type=MaterialType.NORMAL, q=1
    )  # a vérifier
    base.add_building(Building.CONSTRUCTEUR, recipe=Recipe.BETON, q=3)
    base.add_building(Building.ASSEMBLEUSE, recipe=Recipe.POUTRE_BETON_ARME, q=2)

    base.add_building(Building.FOREUSE_MK2, material=Material.MINERAI_DE_CUIVRE, material_type=MaterialType.PUR, q=1)
    base.add_building(Building.FONDERIE, recipe=Recipe.LINGOT_CUIVRE, q=4)
    base.add_building(Building.CONSTRUCTEUR, recipe=Recipe.FIL_ELECTRIQUE, q=5)
    base.add_building(Building.ASSEMBLEUSE, recipe=Recipe.STATOR, q=3)
    base.add_building(Building.ASSEMBLEUSE, recipe=Recipe.STATOR, q=1, clock_speed=75)
    base.add_import(Material.ROTOR, q=100)
    base.add_building(Building.ASSEMBLEUSE, recipe=Recipe.MOTEUR, q=1)
    base.add_building(Building.ASSEMBLEUSE, recipe=Recipe.MOTEUR, q=1, clock_speed=75)
    print(base)


def base_centrale_charbon() -> None:
    base = Base()
    # proche de l'eau
    base.add_building(Building.FOREUSE_MK2, material=Material.CHARBON, material_type=MaterialType.PUR, q=1)
    base.add_building(Building.POMPE_EAU, q=4)
    base.add_building(Building.GENERATEUR_CHARBON, recipe=Recipe.BRULE_CHARBON, q=10)

    # etage
    base.add_building(Building.FOREUSE_MK2, material=Material.CHARBON, material_type=MaterialType.NORMAL, q=1)
    base.add_building(Building.POMPE_EAU, q=3)
    base.add_building(Building.GENERATEUR_CHARBON, recipe=Recipe.BRULE_CHARBON, q=6)

    # autre coté de la rive
    base.add_building(Building.POMPE_EAU, q=4)
    base.add_building(Building.GENERATEUR_CHARBON, recipe=Recipe.BRULE_CHARBON, q=8)
    print(base)


def base_principale() -> None:
    base = Base()

    base.add_building(Building.FOREUSE_MK1, material=Material.MINERAI_DE_FER, material_type=MaterialType.PUR, q=1)
    base.add_building(Building.FONDERIE, recipe=Recipe.LINGOT_FER, q=4)
    base.add_building(Building.CONSTRUCTEUR, recipe=Recipe.PLAQUE, q=4)
    base.add_import(Material.VIS, q=1000)
    base.add_building(Building.ASSEMBLEUSE, recipe=Recipe.PLAQUE_DE_FER_RENFORCEE, q=2)
    base.add_building(Building.ASSEMBLEUSE, recipe=Recipe.CADRE_MODULAIRE, q=3)

    base.add_building(Building.FOREUSE_MK2, material=Material.MINERAI_DE_FER, material_type=MaterialType.PUR, q=1)
    base.add_building(Building.FONDERIE, recipe=Recipe.LINGOT_FER, q=8)
    base.add_building(Building.CONSTRUCTEUR, recipe=Recipe.TIGE, q=6)  # RdC
    base.add_building(Building.CONSTRUCTEUR, recipe=Recipe.VIS, q=6)  # RdC

    base.add_building(Building.CONSTRUCTEUR, recipe=Recipe.TIGE, q=7)  # 1er etage
    base.add_building(Building.CONSTRUCTEUR, recipe=Recipe.VIS, q=7)  # 1er etage
    # base.export_to(first_part)
    base.add_building(Building.ASSEMBLEUSE, recipe=Recipe.ROTOR, q=3)


def main() -> None:
    base_acier()
    base_centrale_charbon()


if __name__ == "__main__":
    main()
