from pathlib import Path

from satisfactory import *
from satisfactory.building import GenericBuilding as Building

# from satisfactory.base import AllConnectedBase, Base, Building
# from satisfactory.dataclasses import BuildingType, Material, MaterialType, Recipe
# from satisfactory.plotter import plotter


def base_acier() -> tuple[Base, Building]:
    base = Base("base acier")
    base.add_all_connected(
        "",
        [
            ForeuseMK2(Material.MINERAI_DE_FER, MaterialType.PUR, q=2),
            ForeuseMK2(Material.CHARBON, MaterialType.PUR, q=2),
            # poutre
            FonderieAvancee(Recipe.LINGOT_ACIER, q=6),
            Constructeur(Recipe.POUTRE_ACIER, q=4.5),
            # tuyau
            FonderieAvancee(Recipe.LINGOT_ACIER, q=4.666666),
            Constructeur(Recipe.TUYAU_ACIER, q=7),
            ForeuseMK2(Material.CALCAIRE, MaterialType.NORMAL, q=1),  # a vérifier
            Constructeur(Recipe.BETON, q=2.66666666),
            Assembleuse(Recipe.POUTRE_BETON_ARME, q=2),
            ForeuseMK2(Material.MINERAI_DE_CUIVRE, MaterialType.PUR, q=1),
            Fonderie(Recipe.LINGOT_CUIVRE, q=4),
            Constructeur(Recipe.FIL_ELECTRIQUE, q=5),
            Assembleuse(Recipe.STATOR, q=3.75),
            # base.add_import(Material.ROTOR, q=100)
            a := Assembleuse(Recipe.MOTEUR, q=1.75),
            cml := Faconneuse(Recipe.CADRE_MODULAIRE_LOURD),
        ],
    )
    base.add_all_connected(
        "vis",
        [
            ForeuseMK2(Material.MINERAI_DE_FER, material_type=MaterialType.NORMAL, q=2),
            Fonderie(Recipe.LINGOT_FER, q=8),
            Constructeur(Recipe.TIGE, q=9),
            vis := Constructeur(Recipe.VIS, q=6),
        ],
    )
    vis.to(cml)

    return base, a, cml


def base_principale(plastique, plastique2) -> tuple[Base, Building]:
    base = Base("Base principale")

    base.add_all_connected(
        "vis_pour_plaque",
        [
            ForeuseMK2(material=Material.MINERAI_DE_FER, material_type=MaterialType.PUR),
            Fonderie(recipe=Recipe.LINGOT_FER, q=8),
            Constructeur(recipe=Recipe.TIGE, q=16),
            vis_plaque := Constructeur(recipe=Recipe.VIS, q=20),
        ],
    )

    base.add_all_connected(
        "plaque",
        [
            ForeuseMK2(material=Material.MINERAI_DE_FER, material_type=MaterialType.PUR),
            Fonderie(recipe=Recipe.LINGOT_FER, q=8),
            Constructeur(recipe=Recipe.PLAQUE, q=8),
            # need import vis
            fer_renforce := Assembleuse(recipe=Recipe.PLAQUE_DE_FER_RENFORCEE, q=5),
            # import vis 2
            cadre := Assembleuse(recipe=Recipe.CADRE_MODULAIRE, q=3),
        ],
    )
    vis_plaque.to(cadre)
    vis_plaque.to(fer_renforce)

    base.add_all_connected(
        "cuivre",
        [
            ForeuseMK1(material=Material.MINERAI_DE_CUIVRE, material_type=MaterialType.PUR),
            Fonderie(recipe=Recipe.LINGOT_CUIVRE, q=4),
            Constructeur(recipe=Recipe.FIL_ELECTRIQUE, q=4),
            Constructeur(recipe=Recipe.TOLE_CUIVRE, q=3),
            cable := Constructeur(recipe=Recipe.CABLE, q=2),
        ],
    )

    base.add_all_connected(
        "Vis 0 et 1",
        [
            ForeuseMK2(material=Material.MINERAI_DE_FER, material_type=MaterialType.PUR),
            lingot_fer := Fonderie(recipe=Recipe.LINGOT_FER, q=8),
            tige_1 := Constructeur(recipe=Recipe.TIGE, q=6 + 7),
            vis1 := Constructeur(recipe=Recipe.VIS, q=6),
            vis2 := Constructeur(recipe=Recipe.VIS, q=6),
            vis2b := Constructeur(recipe=Recipe.VIS, q=1),
        ],
    )
    base.add_all_connected(
        "2eme Etage Vis",
        [
            t_2 := Constructeur(Recipe.TIGE, q=3),
            vis_2 := Constructeur(Recipe.VIS, q=4.5),
        ],
    )
    base.add_building(rotor := Assembleuse(recipe=Recipe.ROTOR, q=3, label="rotor"))

    base.add_building(ordi := Faconneuse(Recipe.ORDINATEUR, q=2))

    lingot_fer.to(t_2)

    tige_1.to(rotor)
    # vis1.to(cadre)
    # vis1.to(fer_renforce)
    vis2.to(rotor)

    vis_2.to(ordi)
    vis2b.to(ordi)
    cable.to(ordi)
    plastique.to(ordi, [Material.PLASTIQUE])
    plastique2.to(ordi, [Material.PLASTIQUE])

    base.add_all_connected(
        "quartz",
        [
            ForeuseMK1(material=Material.QUARTZ_BRUT, material_type=MaterialType.PUR),
            Constructeur(Recipe.CRISTAL_DE_QUARTZ, q=3),
            Constructeur(Recipe.SILICE, q=2),
            ForeuseMK2(material=Material.MINERAI_DE_CUIVRE, material_type=MaterialType.PUR),
            Fonderie(Recipe.LINGOT_CUIVRE, q=8),
            Constructeur(Recipe.TOLE_CUIVRE, q=12),
            circuit := Assembleuse(Recipe.CIRCUIT_IMPRIME_EN_SILICIUM, q=4),
        ],
    )
    circuit.to(ordi)

    return base, rotor, cadre, circuit


def base_centrale_charbon() -> Base:
    base = Base("Centrales charbon")
    base.add_all_connected(
        "grande plage",
        [
            f1 := ForeuseMK2(material=Material.CHARBON, material_type=MaterialType.PUR),
            PompeEau(q=4),
            GenerateurCharbon(recipe=Recipe.BRULE_CHARBON, q=10),
        ],
    )
    base.add_all_connected(
        "etage",
        [
            f2 := ForeuseMK2(material=Material.CHARBON, material_type=MaterialType.NORMAL),
            PompeEau(q=3),
            GenerateurCharbon(recipe=Recipe.BRULE_CHARBON, q=6),
        ],
    )
    base.add_all_connected(
        "petite plage",
        [
            PompeEau(q=4),
            g3 := GenerateurCharbon(recipe=Recipe.BRULE_CHARBON, q=8),
        ],
    )
    f1.to(g3)
    f2.to(g3)
    return base


def base_petrole() -> Base:
    base = Base("Petrole")
    base.add_all_connected(
        "plage",
        [
            pompe := PompePetrole(material_type=MaterialType.PUR),
            PompeEau(q=3),
            plastique := Raffinerie(recipe=Recipe.PLASTIQUE, q=2),
            Raffinerie(recipe=Recipe.CAOUTCHOUC, q=2),
            Raffinerie(recipe=Recipe.COKE_DE_PETROLE, q=2),
            GenerateurCharbon(recipe=Recipe.BRULE_COKE_PETROLE, q=6),
        ],
    )

    base.add_all_connected(
        "carburant",
        [
            p2 := Raffinerie(Recipe.PLASTIQUE, q=4),
            Raffinerie(Recipe.CARBURANT_RESIDUEL, q=0.666666),
            Constructeur(Recipe.BIDON_VIDE, q=0.24),
            GenerateurCarburant(Recipe.BRULE_CARBURANT, q=1),
            Packageur(Recipe.CARBURANT_CONDITIONNE, q=0.37),
        ],
    )
    pompe.to(p2)

    return base, plastique, p2


def base_caterium(circuit_imprime) -> Base:
    base = Base("Caterium")

    # allow with(base):
    # define a global context to put every bulding and base in a base
    filactif = (
        ForeuseMK2(Material.MINERAI_DE_CATERIUM, MaterialType.NORMAL)
        .to(Fonderie(Recipe.LINGOT_CATERIUM, q=2.6666))
        .merge(ForeuseMK2(Material.MINERAI_DE_CATERIUM, MaterialType.PUR).to(Fonderie(Recipe.LINGOT_CATERIUM, q=5)))
        .to(Constructeur(Recipe.FILACTIF, q=3))
    )

    cuivre = ForeuseMK2(material=Material.MINERAI_DE_CUIVRE, material_type=MaterialType.PUR).to(
        Fonderie(Recipe.LINGOT_CUIVRE, q=6)
    )

    ia = cuivre.to(Constructeur(Recipe.TOLE_CUIVRE, q=1)).merge(filactif).to(Assembleuse(Recipe.CONTROLEUR_IA, q=1))
    chv = (
        cuivre.to(Constructeur(Recipe.FIL_ELECTRIQUE, q=4))
        .to(Constructeur(Recipe.CABLE, q=2))
        .merge(filactif)
        .to(Faconneuse(Recipe.CONNECTEUR_HAUTE_VITESSE, q=1))
    )
    # base.add_all_connected(
    #     "filactif",
    #     [
    #         AllConnectedBase(
    #             [
    #                 ForeuseMK2(Material.MINERAI_DE_CATERIUM, MaterialType.NORMAL),
    #                 Fonderie(Recipe.LINGOT_CATERIUM, q=2.6666),
    #             ]
    #         ),
    #         AllConnectedBase(
    #             [
    #                 ForeuseMK2(Material.MINERAI_DE_CATERIUM, MaterialType.PUR),
    #                 Fonderie(Recipe.LINGOT_CATERIUM, q=5),
    #             ]
    #         ),
    #         filactif := Constructeur(Recipe.FILACTIF, q=3),
    #     ],
    # )
    # base.add_all_connected(
    #     "cuivre",
    #     [
    #         ForeuseMK2(material=Material.MINERAI_DE_CUIVRE, material_type=MaterialType.PUR),
    #         cuivre := Fonderie(Recipe.LINGOT_CUIVRE, q=6),
    #     ],
    # )

    # base.add_all_connected(
    #     "contoleur IA",
    #     [
    #         tole := Constructeur(Recipe.TOLE_CUIVRE, q=1),
    #         ia := Assembleuse(Recipe.CONTROLEUR_IA, q=1),
    #     ],
    # )
    # cuivre.to(tole)
    # filactif.to(ia)
    # base.add_all_connected(
    #     "connecterur haute vitesse",
    #     [
    #         fil := Constructeur(Recipe.FIL_ELECTRIQUE, q=4),
    #         Constructeur(Recipe.CABLE, q=2),
    #         chv := Faconneuse(Recipe.CONNECTEUR_HAUTE_VITESSE, q=1),
    #     ],
    # )
    # cuivre.to(fil)
    # filactif.to(chv)
    circuit_imprime.to(chv)
    return base


base = Base("Everything")
base_pet, plastique, plastique2 = base_petrole()
base_a, a, cml = base_acier()
base_p, b, cadre, circuit = base_principale(plastique, plastique2)
base_e = base_centrale_charbon()
base_c = base_caterium(circuit)
b.to(a, [Material.ROTOR])
cadre.to(cml)
base.add_sub_base(base_a)
base.add_sub_base(base_p)
base.add_sub_base(base_e)
base.add_sub_base(base_pet)
base.add_sub_base(base_c)
base.compute()
base.rapport()
plotter(base, Path.cwd() / "output.txt")
