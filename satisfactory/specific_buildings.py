from satisfactory.building import BuildingRecipe, BuildingRessourceExtractor
from satisfactory.dataclasses import BuildingType, Material, MaterialType, Recipe


class ForeuseMK1(BuildingRessourceExtractor):
    def __init__(
        self,
        material: Material | str,
        material_type: MaterialType | str,
        label: str = "",
        clock_speed: float = 100,
        q: float = 1,
    ) -> None:
        super().__init__(
            BuildingType.FOREUSE_MK1, Material(material), MaterialType(material_type), label, clock_speed, q
        )

    def compute(self) -> None:
        self.material_produced[self.material] = self.material_type * 1 * self.computed_q


class ForeuseMK2(BuildingRessourceExtractor):
    def __init__(
        self,
        material: Material | str,
        material_type: MaterialType | str,
        label: str = "",
        clock_speed: float = 100,
        q: float = 1,
    ) -> None:
        super().__init__(
            BuildingType.FOREUSE_MK2, Material(material), MaterialType(material_type), label, clock_speed, q
        )

    def compute(self) -> None:
        self.material_produced[self.material] = self.material_type * 2 * self.computed_q


class PompeEau(BuildingRessourceExtractor):
    def __init__(self, label: str = "", clock_speed: float = 100, q: float = 1) -> None:
        super().__init__(BuildingType.POMPE_EAU, Material.EAU, MaterialType.PUR, label, clock_speed, q)

    def compute(self) -> None:
        self.material_produced[Material.EAU] = self.material_type * self.computed_q


class PompePetrole(BuildingRessourceExtractor):
    def __init__(
        self, material_type: MaterialType | str, label: str = "", clock_speed: float = 100, q: float = 1
    ) -> None:
        super().__init__(
            BuildingType.POMPE_A_PETROLE,
            Material.PETROLE_BRUT,
            MaterialType(material_type),
            label,
            clock_speed,
            q,
        )

    def compute(self) -> None:
        self.material_produced[Material.PETROLE_BRUT] = self.material_type * 2 * self.computed_q


class FonderieAvancee(BuildingRecipe):
    def __init__(
        self,
        recipe: Recipe | str,
        label: str = "",
        clock_speed: float = 100,
        q: float = 1,
    ) -> None:
        super().__init__(BuildingType.FONDERIE_AVANCEE, Recipe(recipe), label, clock_speed, q)


class Constructeur(BuildingRecipe):
    def __init__(
        self,
        recipe: Recipe | str,
        label: str = "",
        clock_speed: float = 100,
        q: float = 1,
    ) -> None:
        super().__init__(BuildingType.CONSTRUCTEUR, Recipe(recipe), label, clock_speed, q)


class Assembleuse(BuildingRecipe):
    def __init__(
        self,
        recipe: Recipe | str,
        label: str = "",
        clock_speed: float = 100,
        q: float = 1,
    ) -> None:
        super().__init__(BuildingType.ASSEMBLEUSE, Recipe(recipe), label, clock_speed, q)


class Fonderie(BuildingRecipe):
    def __init__(
        self,
        recipe: Recipe | str,
        label: str = "",
        clock_speed: float = 100,
        q: float = 1,
    ) -> None:
        super().__init__(BuildingType.FONDERIE, Recipe(recipe), label, clock_speed, q)


class GenerateurCharbon(BuildingRecipe):
    def __init__(
        self,
        recipe: Recipe | str,
        label: str = "",
        clock_speed: float = 100,
        q: float = 1,
    ) -> None:
        super().__init__(BuildingType.GENERATEUR_CHARBON, Recipe(recipe), label, clock_speed, q)


class GenerateurCarburant(BuildingRecipe):
    def __init__(
        self,
        recipe: Recipe | str,
        label: str = "",
        clock_speed: float = 100,
        q: float = 1,
    ) -> None:
        super().__init__(BuildingType.GENERATEUR_CARBURANT, Recipe(recipe), label, clock_speed, q)


class Faconneuse(BuildingRecipe):
    def __init__(
        self,
        recipe: Recipe | str,
        label: str = "",
        clock_speed: float = 100,
        q: float = 1,
    ) -> None:
        super().__init__(BuildingType.FACONNEUSE, Recipe(recipe), label, clock_speed, q)


class Raffinerie(BuildingRecipe):
    def __init__(
        self,
        recipe: Recipe | str,
        label: str = "",
        clock_speed: float = 100,
        q: float = 1,
    ) -> None:
        super().__init__(BuildingType.RAFFINERIE, Recipe(recipe), label, clock_speed, q)


class Packageur(BuildingRecipe):
    def __init__(
        self,
        recipe: Recipe | str,
        label: str = "",
        clock_speed: float = 100,
        q: float = 1,
    ) -> None:
        super().__init__(BuildingType.PACKAGEUR, Recipe(recipe), label, clock_speed, q)
