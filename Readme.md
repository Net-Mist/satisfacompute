# Satisfactory calculator

## Modelisation

a _base_ is a building or a set of building importing and exporting resources and consuming energy.

More specifically, a base can be recursively defined as:

1. a single building
2. a set of similar building with a common conveyer belt as input and as output
3. a list of bases. We will call these bases _sub-bases_. In this case we consider that the *N*th sub-base in the list have access to the ressources of the _N-1_ previous ones.
4. a set of bases. In this case the base is marly a container for organization. internal bases probably imports and export resources between themselves.

The Calculator works in 2 steps : first we define the list of bases and the connections between them, then the calculator tries to compute the number of resources generated. This will be done doing a graph exploration starting from the Miners.

## Definition of base

### Single building

A single building is represented by a class that inherit from `Building`

```python
from satisfactory import ForeuseMK2, Fonderie, Material, MaterialType, Recipe
a = ForeuseMK2(Material.MINERAI_DE_FER, MaterialType.PUR)
b = Fonderie(Recipe.LINGOT_FER)
```

If you wish to change the efficiency of the building, you can set the parameter `clock_speed` to a value between 0 and 100 (default value is 100).

### a set of similar building

You can use the same syntax as for single building, and specify the number of building using the `q` parameter.

If `q` has a no-null decimal part, then The calculator will assume there will be `floor(q)` building with every building at efficiency 1, except the last one at efficiency `q - floor(q)`. In this case, clock_speed need to be set at 100.

If `q` doesn't have a decimal part, then all building will have the same clock speed defined by `clock_speed`

### A list of base

The simplest way to define that the output of a base is the input of another is to use a `AllConnectedBase` structure.

with this code:

```python
base.add_all_connected("filactif", [
    AllConnectedBase([
        ForeuseMK2(Material.MINERAI_DE_CATERIUM, MaterialType.NORMAL),
        Fonderie(Recipe.LINGOT_CATERIUM, q=2.6666),
    ]),
    AllConnectedBase([
        ForeuseMK2(Material.MINERAI_DE_CATERIUM, MaterialType.PUR),
        Fonderie(Recipe.LINGOT_CATERIUM, q=5),
    ]),
    Constructeur(Recipe.FILACTIF, q=3)
])
```

a MK2 Foreuse mining normal material is connected to a Fonderie, another one mining Pur material is connected to another fonderie. Then the 2 fonderie are connected a constructeur.

### Import and export ressources

```python
ForeuseMK2(Material.MINERAI_DE_CATERIUM, MaterialType.NORMAL).to(
    Fonderie(Recipe.LINGOT_CATERIUM, q=2.6666)
).merge(
    ForeuseMK2(Material.MINERAI_DE_CATERIUM, MaterialType.PUR).to(
        Fonderie(Recipe.LINGOT_CATERIUM, q=5)
    )
).to(
    Constructeur(Recipe.FILACTIF, q=3)
)
```
