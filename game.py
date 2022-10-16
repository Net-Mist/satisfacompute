from satisfactory import AllConnectedBase, Base, Building
from satisfactory.dataclasses import BuildingType, Material, MaterialType, Recipe
from pathlib import Path 
from satisfactory.plotter import plotter


def base_acier() -> None:
    base = AllConnectedBase("base acier")
    base.create_building(BuildingType.FOREUSE_MK2, material=Material.MINERAI_DE_FER, material_type=MaterialType.PUR, q=2)
    base.create_building(BuildingType.FOREUSE_MK2, material=Material.CHARBON, material_type=MaterialType.PUR, q=2)

    # poutre
    base.create_building(BuildingType.FONDERIE_AVANCEE, Recipe.LINGOT_ACIER, q=6)
    base.create_building(BuildingType.CONSTRUCTEUR, Recipe.POUTRE_ACIER, q=4)
    base.create_building(BuildingType.CONSTRUCTEUR, Recipe.POUTRE_ACIER, q=1, clock_speed=50)

    # tuyau
    base.create_building(BuildingType.FONDERIE_AVANCEE, Recipe.LINGOT_ACIER, q=4)
    base.create_building(BuildingType.FONDERIE_AVANCEE, Recipe.LINGOT_ACIER, q=1, clock_speed=66.6667)
    base.create_building(BuildingType.CONSTRUCTEUR, Recipe.TUYAU_ACIER, q=7)

    base.create_building(
        BuildingType.FOREUSE_MK2, material=Material.CALCAIRE, material_type=MaterialType.NORMAL, q=1
    )  # a vérifier
    base.create_building(BuildingType.CONSTRUCTEUR, Recipe.BETON, q=3)
    base.create_building(BuildingType.ASSEMBLEUSE, Recipe.POUTRE_BETON_ARME, q=2)

    base.create_building(BuildingType.FOREUSE_MK2, material=Material.MINERAI_DE_CUIVRE, material_type=MaterialType.PUR, q=1)
    base.create_building(BuildingType.FONDERIE, Recipe.LINGOT_CUIVRE, q=4)
    base.create_building(BuildingType.CONSTRUCTEUR, Recipe.FIL_ELECTRIQUE, q=5)
    base.create_building(BuildingType.ASSEMBLEUSE, Recipe.STATOR, q=3)
    base.create_building(BuildingType.ASSEMBLEUSE, Recipe.STATOR, q=1, clock_speed=75)
    # base.add_import(Material.ROTOR, q=100)
    a = base.create_building(BuildingType.ASSEMBLEUSE, Recipe.MOTEUR, q=1)
    base.create_building(BuildingType.ASSEMBLEUSE, Recipe.MOTEUR, q=1, clock_speed=75)
    return base, a


def base_principale() -> None:
    base = Base("Base principale")
    base.add_all_connected("plaque", [
        Building(BuildingType.FOREUSE_MK1, material=Material.MINERAI_DE_FER, material_type=MaterialType.PUR, q=1),
        Building(BuildingType.FONDERIE, recipe=Recipe.LINGOT_FER, q=4),
        Building(BuildingType.CONSTRUCTEUR, recipe=Recipe.PLAQUE, q=4),
        # need import vis
        fer_renforce := Building(BuildingType.ASSEMBLEUSE, recipe=Recipe.PLAQUE_DE_FER_RENFORCEE, q=2),
        Building(BuildingType.ASSEMBLEUSE, recipe=Recipe.CADRE_MODULAIRE, q=3)
    ])

    base.add_all_connected("RdC Vis", [
        Building(BuildingType.FOREUSE_MK2, material=Material.MINERAI_DE_FER, material_type=MaterialType.PUR, q=1),
        lingot_fer := Building(BuildingType.FONDERIE, recipe=Recipe.LINGOT_FER, q=8),
        Building(BuildingType.CONSTRUCTEUR, recipe=Recipe.TIGE, q=6), #RdC
        Building(BuildingType.CONSTRUCTEUR, recipe=Recipe.VIS, q=6), # RdC
        b := Building(BuildingType.ASSEMBLEUSE, recipe=Recipe.ROTOR, q=3)
    ])

    base.add_all_connected("1er Etage Vis", [
        tige_1 := Building(BuildingType.CONSTRUCTEUR, Recipe.TIGE, q=7),
        vis_1 := Building(BuildingType.CONSTRUCTEUR, Recipe.VIS, q=7),
        # export to first part
    ])
    lingot_fer.export_to(tige_1, Material.LINGOT_FER)
    vis_1.export_to(fer_renforce, Material.VIS)
    return base, b


base = Base()
base_a, a = base_acier()
base_p, b = base_principale()
b.export_to(a, Material.ROTOR)
base.add_sub_base(base_a)
base.add_sub_base(base_p)
base.resolve()
base.rapport()
plotter(base, Path.cwd()/ "output.txt")