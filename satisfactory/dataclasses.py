from enum import Enum


class Material(str, Enum):
    MINERAI_DE_FER = "minerai de fer"
    MINERAI_DE_CUIVRE = "minerai de cuivre"
    CHARBON = "charbon"
    LINGOT_ACIER = "lingot d'acier"
    LINGOT_CUIVRE = "lingot de cuivre"
    LINGOT_FER = "lingot de fer"
    POUTRE_ACIER = "poutre en acier"
    TUYAU_ACIER = "tuyau en acier"
    CALCAIRE = "calcaire"
    BETON = "beton"
    POUTRE_BETON_ARME = "poutre en beton armé"
    FIL_ELECTRIQUE = "fil electrique"
    STATOR = "stator"
    MOTEUR = "moteur"
    ROTOR = "rotor"
    EAU = "eau"
    PLAQUE = "plaque"
    PLAQUE_DE_FER_RENFORCEE = "plaque de fer renforcée"
    CADRE_MODULAIRE = "cadre modulaire"
    TIGE = "tige"
    VIS = "vis"


class BuildingType(str, Enum):
    FOREUSE_MK2 = "Foreuse MK2"
    FOREUSE_MK1 = "Foreuse MK1"
    FONDERIE_AVANCEE = "Fonderie avancée"
    CONSTRUCTEUR = "Constructeur"
    ASSEMBLEUSE = "Assembleuse"
    FONDERIE = "Fonderie"
    POMPE_EAU = "Pompe à eau"
    GENERATEUR_CHARBON = "Générateur à charbon"


class Recipe(str, Enum):
    LINGOT_ACIER = "lingot d'acier"
    POUTRE_ACIER = "poutre en acier"
    TUYAU_ACIER = "tuyau en acier"
    BETON = "beton"
    POUTRE_BETON_ARME = "poutre en beton armé"
    LINGOT_CUIVRE = "lingot de cuivre"
    LINGOT_FER = "lingot de fer"
    PLAQUE = "plaque"
    FIL_ELECTRIQUE = "fil electrique"
    STATOR = "stator"
    MOTEUR = "moteur"
    BRULE_CHARBON = "brule charbon"
    PLAQUE_DE_FER_RENFORCEE = "plaque de fer renforcée"
    CADRE_MODULAIRE = "cadre modulaire"
    TIGE = "tige"
    ROTOR = "rotor"
    VIS = "vis"


class MaterialType(int, Enum):
    PUR = 120
    NORMAL = 60
    IMPUR = 30
