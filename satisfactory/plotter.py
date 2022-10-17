from math import floor
from pathlib import Path

from satisfactory.dataclasses import Material

from .base import AllConnectedBase, Base, Building, GenericBase

GRAPHVIZ_START = """
digraph G {
  fontname="Helvetica,Arial,sans-serif"
  node [fontname="Helvetica,Arial,sans-serif"]
  edge [
    arrowsize=0.5
    fontname="Helvetica,Arial,sans-serif"
    labeldistance=3
    labelfontcolor="#00000080"
    penwidth=2
    // style=dotted // dotted style symbolizes data transfer
  ]
  // layout=fdp
  concentrate=True;
  rankdir=TB;
  node [shape=record];
"""

GRAPHVIZ_END = "\n}\n"

def fstr(n: float):
    if abs(n - floor(n)) < 0.01:
        return f"{int(n)}"
    else:
        return f"{n:0.2f}"


def plotter(base: Base, path: Path) -> None:
    id = "1"
    base_to_id = {base: id}
    connections = []  # list of flux between bases

    graphviz = GRAPHVIZ_START
    graphviz += base_to_graphviz(base, id, base_to_id, connections, 1)
    for (in_base, out_base, materials) in connections:
        in_id = base_to_id[in_base]
        out_id = base_to_id[out_base]
        materials = " ".join([f"{fstr(v)} {k}" for k, v in materials.items()])
        graphviz += f'  {in_id} -> {out_id} [label="   {materials}"]\n'
    graphviz += GRAPHVIZ_END
    path.write_text(graphviz)


def base_to_graphviz(
    base: Base,
    id: str,
    base_to_id: dict[GenericBase, str],
    connections: list[tuple[GenericBase, GenericBase, Material]],
    level: int,
) -> str:
    indent = " " * 2 * level
    indent_in = " " * 3 * level
    r = f'\n{indent}subgraph cluster{id} {{\n{indent_in}label = "{base.label} : {base.energy_available:0.2f} MW";\n'

    for i, sub_base in enumerate(base.sub_bases):
        if type(sub_base) == Building:
            b_id = f"b{id}building{i}"
            r += indent_in + building_to_graphviz(sub_base, b_id)
            base_to_id[sub_base] = b_id
            for import_base, materials in sub_base.imports.items():
                connections.append((import_base, sub_base, materials))
        elif type(sub_base) in (Base, AllConnectedBase):
            b_id = f"s{id}subbase{i}"
            r += base_to_graphviz(sub_base, b_id, base_to_id, connections, level + 1)
        else:
            ValueError("unknown subbase type")

    return r + indent + "}\n"


def building_to_graphviz(building: Building, id: str) -> str:
    label_displayed = f": {building.label}" if building.label is not None else ""
    residual_materials_snippets = [f"{k}: {fstr(v)}" for k, v in building.material_quantities.items() if v > 0.01]
    color = "white"

    has_lowered_q = False
    has_residual = False

    params = ""
    if building.clock_speed == 100:
        params += f"q={fstr(building.q)}"
        if building.computed_q != building.q:
            params += f" to {fstr(building.computed_q)}"
            has_lowered_q = True

    residual_materials = ""
    if residual_materials_snippets:
        residual_materials = "|reste: " + ",".join(residual_materials_snippets)
        has_residual = True

    if has_lowered_q and has_residual:
        color = "#ff880022"
    elif has_lowered_q:
        color = "#88000022"
    elif has_residual:
        color = "#88ff0022"

    displayed_color = ""
    if color != "white":
        displayed_color = f'style=filled fillcolor="{color}"'

    return (
        f'{id} [{displayed_color} label="{building.building_type}{label_displayed}\\n{params}{residual_materials}"]\n'
    )
