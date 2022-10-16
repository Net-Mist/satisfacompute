from pathlib import Path
from .base import Base, Building

GRAPHVIZ_START = """
digraph G {
  fontname="Helvetica,Arial,sans-serif"
  node [fontname="Helvetica,Arial,sans-serif", shape=rect]
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

GRAPHVIZ_END ="\n}\n"

def plotter(base: Base, path: Path):
    id = "1"
    base_to_id = {base: id}
    connections = [] # list of flux between bases

    graphviz = GRAPHVIZ_START
    graphviz += base_to_graphviz(base, id, base_to_id, connections, 1)
    for (in_base, out_base) in connections:
        in_id = base_to_id[in_base]
        out_id = base_to_id[out_base]
        graphviz += f"  {in_id} -> {out_id}\n"
    graphviz += GRAPHVIZ_END
    path.write_text(graphviz)


def base_to_graphviz(base: Base, id, base_to_id, connections, level) -> str:
    indent = " " * 2*level
    indent_in = " " * 3*level
    r = f"\n{indent}subgraph cluster{id} {{\n{indent_in}label = \"{base.label}\";\n"

    for i, sub_base in enumerate(base.sub_bases):
        if type(sub_base) == Building:
            b_id = f"b{id}building{i}" 
            r += f"{indent_in}{b_id} [label=\"{sub_base.building_type}: {sub_base.label}\"]\n"
            # r += f"{b_id} [label=\"{sub_base.building_type}: {sub_base.label}\n|{{input:|output:}}|{{{{[(?, ?)]}}|{{[(?, ?)]}}}}\"];"
            base_to_id[sub_base] = b_id
            for import_base in sub_base.imports.keys():
                connections.append((import_base, sub_base))
        else:
            b_id = f"s{id}subbase{i}" 
            r += base_to_graphviz(sub_base, b_id, base_to_id, connections, level+1)


    return r + indent + "}\n"