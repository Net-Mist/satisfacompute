from pathlib import Path

from satisfactory.base import AllConnectedBase, Base, Building
from satisfactory.dataclasses import BuildingType, Material, MaterialType, Recipe
from satisfactory.plotter import plotter


def base_acier() -> tuple[Base, Building]:
    base = Base("base acier")
    base.add_all_connected("",[
        Building(BuildingType.FOREUSE_MK2, material=Material.MINERAI_DE_FER, material_type=MaterialType.PUR, q=2),
    
        Building(BuildingType.FOREUSE_MK2, material=Material.CHARBON, material_type=MaterialType.PUR, q=2),

        # poutre
        Building(BuildingType.FONDERIE_AVANCEE, Recipe.LINGOT_ACIER, q=6),
        Building(BuildingType.CONSTRUCTEUR, Recipe.POUTRE_ACIER, q=4.5),

        # tuyau
        Building(BuildingType.FONDERIE_AVANCEE, Recipe.LINGOT_ACIER, q=4.666666),
        Building(BuildingType.CONSTRUCTEUR, Recipe.TUYAU_ACIER, q=7),

        Building(
        BuildingType.FOREUSE_MK2, material=Material.CALCAIRE, material_type=MaterialType.NORMAL, q=1
    ),  # a vérifier
        Building(BuildingType.CONSTRUCTEUR, Recipe.BETON, q=2.66666666),
        Building(BuildingType.ASSEMBLEUSE, Recipe.POUTRE_BETON_ARME, q=2),

        Building(
        BuildingType.FOREUSE_MK2, material=Material.MINERAI_DE_CUIVRE, material_type=MaterialType.PUR, q=1
    ),
        Building(BuildingType.FONDERIE, Recipe.LINGOT_CUIVRE, q=4),
        Building(BuildingType.CONSTRUCTEUR, Recipe.FIL_ELECTRIQUE, q=5),
        Building(BuildingType.ASSEMBLEUSE, Recipe.STATOR, q=3.75),
        # base.add_import(Material.ROTOR, q=100)
        a :=     Building(BuildingType.ASSEMBLEUSE, Recipe.MOTEUR, q=1.75),
        cml := Building(BuildingType.FACONNEUSE, Recipe.CADRE_MODULAIRE_LOURD)
    ])
    base.add_all_connected("vis", [
        Building(BuildingType.FOREUSE_MK2, material=Material.MINERAI_DE_FER, material_type=MaterialType.NORMAL, q=2),
        Building(BuildingType.FONDERIE, Recipe.LINGOT_FER, q=8),
        Building(BuildingType.CONSTRUCTEUR, Recipe.TIGE, q=9),
        vis := Building(BuildingType.CONSTRUCTEUR, Recipe.VIS, q=6),

    ])
    vis.export_to(cml)

    return base, a, cml


def base_principale() -> tuple[Base, Building]:
    base = Base("Base principale")
    base.add_all_connected(
        "plaque",
        [
            Building(BuildingType.FOREUSE_MK1, material=Material.MINERAI_DE_FER, material_type=MaterialType.PUR),
            Building(BuildingType.FONDERIE, recipe=Recipe.LINGOT_FER, q=4),
            Building(BuildingType.CONSTRUCTEUR, recipe=Recipe.PLAQUE, q=4),
            # need import vis
            fer_renforce := Building(BuildingType.ASSEMBLEUSE, recipe=Recipe.PLAQUE_DE_FER_RENFORCEE, q=2),
            # import vis 2
            cadre := Building(BuildingType.ASSEMBLEUSE, recipe=Recipe.CADRE_MODULAIRE, q=3),
        ],
    )

    base.add_all_connected(
        "RdC Vis",
        [
            Building(BuildingType.FOREUSE_MK2, material=Material.MINERAI_DE_FER, material_type=MaterialType.PUR),
            lingot_fer := Building(BuildingType.FONDERIE, recipe=Recipe.LINGOT_FER, q=8),
            Building(BuildingType.CONSTRUCTEUR, recipe=Recipe.TIGE, q=6),  # RdC
            vis1 := Building(BuildingType.CONSTRUCTEUR, recipe=Recipe.VIS, q=6),  # RdC
            vis2 := Building(BuildingType.CONSTRUCTEUR, recipe=Recipe.VIS, q=3),  # RdC
        ],
    )
    base.add_building(rotor := Building(BuildingType.ASSEMBLEUSE, recipe=Recipe.ROTOR, q=3, label="rotor"))
    vis1.export_to(rotor)
    vis2.export_to(fer_renforce)

    base.add_all_connected(
        "1er Etage Vis",
        [
            tige_1 := Building(BuildingType.CONSTRUCTEUR, Recipe.TIGE, q=7),
            vis_1 := Building(BuildingType.CONSTRUCTEUR, Recipe.VIS, q=7),
            # export to first part
        ],
    )
    lingot_fer.export_to(tige_1, [Material.LINGOT_FER])
    vis_1.export_to(rotor)
    vis_1.export_to(cadre)
    tige_1.export_to(rotor)

    base.add_all_connected("quartz", [
        Building(BuildingType.FOREUSE_MK1, material=Material.QUARTZ_BRUT, material_type=MaterialType.PUR),
        Building(BuildingType.CONSTRUCTEUR, Recipe.CRISTAL_DE_QUARTZ, q=3),
        Building(BuildingType.CONSTRUCTEUR, Recipe.SILICE, q=2),

        Building(BuildingType.FOREUSE_MK2, material=Material.MINERAI_DE_CUIVRE, material_type=MaterialType.PUR),
        Building(BuildingType.FONDERIE, Recipe.LINGOT_CUIVRE, q=4),
        Building(BuildingType.CONSTRUCTEUR, Recipe.TOLE_CUIVRE, q=3),
        Building(BuildingType.ASSEMBLEUSE, Recipe.CIRCUIT_IMPRIME_EN_SILICIUM, q=1)
    ])

    return base, rotor, cadre


def base_centrale_charbon() -> Base:
    base = Base("Centrales charbon")
    base.add_all_connected(
        "grande plage",
        [
            f1 := Building(BuildingType.FOREUSE_MK2, material=Material.CHARBON, material_type=MaterialType.PUR),
            Building(BuildingType.POMPE_EAU, q=4),
            Building(BuildingType.GENERATEUR_CHARBON, recipe=Recipe.BRULE_CHARBON, q=10),
        ],
    )
    base.add_all_connected(
        "etage",
        [
            f2 := Building(BuildingType.FOREUSE_MK2, material=Material.CHARBON, material_type=MaterialType.NORMAL),
            Building(BuildingType.POMPE_EAU, q=3),
            Building(BuildingType.GENERATEUR_CHARBON, recipe=Recipe.BRULE_CHARBON, q=6),
        ],
    )
    base.add_all_connected(
        "petite plage",
        [
            Building(BuildingType.POMPE_EAU, q=4),
            g3 := Building(BuildingType.GENERATEUR_CHARBON, recipe=Recipe.BRULE_CHARBON, q=8),
        ],
    )
    f1.export_to(g3)
    f2.export_to(g3)
    return base


base = Base("Everything")
base_a, a, cml = base_acier()
base_p, b, cadre = base_principale()
base_e = base_centrale_charbon()
b.export_to(a, [Material.ROTOR])
cadre.export_to(cml)
base.add_sub_base(base_a)
base.add_sub_base(base_p)
base.add_sub_base(base_e)
base.resolve()
base.rapport()
plotter(base, Path.cwd() / "output.txt")
