#!/usr/bin/env python3
"""
svg_to_d2.py - Parse SVG flowchart and convert to D2 lang diagram.
Usage: python svg_to_d2.py input.svg [output.d2]
"""

import os
import sys
import xml.etree.ElementTree as ET


# Shapes supported by D2
D2_SHAPE_MAP = {
    "diamond":   "diamond",
    "rectangle": "rectangle",
    "oval":      "oval",
    "circle":    "circle",
    "hexagon":   "hexagon",
    "cylinder":  "cylinder",
    "parallelogram": "parallelogram",
}

# Style per shape
SHAPE_STYLE = {
    "rectangle": {"fill": "#FEE2E2", "stroke": "#F97316"},
    "diamond":   {"fill": "#E0F2FE", "stroke": "#0284C7"},
}

EDGE_COLOR = "#475569"

# Layout: use 'right' when node count exceeds this threshold (more compact)
COMPACT_THRESHOLD = 6


def sanitize_id(label: str) -> str:
    """Create a safe D2 node ID from a label string."""
    result = label.strip()
    # Replace characters that are not alphanumeric or underscore
    safe = ""
    for ch in result:
        if ch.isalnum() or ch == "_":
            safe += ch
        else:
            safe += "_"
    # Remove leading digits
    if safe and safe[0].isdigit():
        safe = "_" + safe
    return safe or "node"


def parse_svg(svg_path: str) -> tuple[list[dict], list[dict]]:
    """Parse SVG file and extract nodes and edges."""
    tree = ET.parse(svg_path)
    root = tree.getroot()

    # Handle SVG namespace
    ns = ""
    if root.tag.startswith("{"):
        ns = root.tag.split("}")[0] + "}"

    nodes = []
    edges = []

    # Walk all elements
    for elem in root.iter():
        tag = elem.tag.replace(ns, "")

        # --- NODE: <g class="node"> ---
        if tag == "g" and elem.get("class") == "node":
            node_id    = elem.get("data-id", "").strip()
            node_label = elem.get("data-label", "").strip()
            node_shape = elem.get("data-shape", "rectangle").strip().lower()

            # Extract position from child <rect> or <polygon>
            x, y = None, None
            for child in list(elem):
                child_tag = child.tag.replace(ns, "")
                if child_tag == "rect":
                    try:
                        x = float(child.get("x", 0))
                        y = float(child.get("y", 0))
                    except (ValueError, TypeError):
                        pass
                    break
                elif child_tag == "polygon":
                    pts_str = child.get("points", "")
                    pts = []
                    for pt_str in pts_str.split():
                        try:
                            px, py_val = pt_str.split(",")
                            pts.append((float(px), float(py_val)))
                        except ValueError:
                            pass
                    if pts:
                        x = min(p[0] for p in pts)
                        y = min(p[1] for p in pts)
                    break

            if node_id:
                nodes.append({
                    "id":    node_id,
                    "label": node_label,
                    "shape": node_shape,
                    "x":     x,
                    "y":     y,
                })

        # --- EDGE: <polyline class="edge"> ---
        elif tag == "polyline" and elem.get("class") == "edge":
            from_id = elem.get("data-from", "").strip()
            to_id   = elem.get("data-to",   "").strip()
            label   = elem.get("data-label", "").strip()
            if from_id and to_id:
                edges.append({
                    "from":  from_id,
                    "to":    to_id,
                    "label": label,
                })

    return nodes, edges


def build_d2(nodes: list[dict], edges: list[dict]) -> str:
    """Generate D2 source code from nodes and edges."""
    # Determine if all nodes have explicit positions extracted from the SVG
    has_positions = (
        len(nodes) > 0
        and all(n.get("x") is not None and n.get("y") is not None for n in nodes)
    )

    direction = "right" if len(nodes) > COMPACT_THRESHOLD else "down"

    if has_positions:
        # Absolute positions from SVG — use tala which honours top/left
        lines = [
            "vars: {",
            "  d2-config: {",
            "    layout-engine: tala",
            "  }",
            "}",
            "",
        ]
    else:
        lines = [
            "vars: {",
            "  d2-config: {",
            "    layout-engine: dagre",
            "  }",
            "}",
            "",
            f"direction: {direction}",
            "",
        ]

    # Node definitions
    for node in nodes:
        node_id    = node["id"]
        node_label = node["label"]
        shape      = D2_SHAPE_MAP.get(node["shape"], "rectangle")
        style      = SHAPE_STYLE.get(shape, SHAPE_STYLE["rectangle"])

        lines.append(f'{node_id}: "{node_label}" {{')
        if shape != "rectangle":
            lines.append(f'  shape: {shape}')
        lines.append(f'  style: {{')
        lines.append(f'    fill: "{style["fill"]}"')
        lines.append(f'    stroke: "{style["stroke"]}"')
        lines.append(f'    stroke-width: 2')
        lines.append(f'    font-size: 20')
        lines.append(f'  }}')
        if has_positions:
            lines.append(f'  top: {int(node["y"])}')
            lines.append(f'  left: {int(node["x"])}')
        lines.append("}")

    lines.append("")

    # Edge definitions
    for edge in edges:
        from_id = edge["from"]
        to_id   = edge["to"]
        label   = edge["label"]

        if label:
            lines.append(f'{from_id} -> {to_id}: "{label}" {{')
        else:
            lines.append(f'{from_id} -> {to_id}: {{')
        lines.append(f'  style: {{')
        lines.append(f'    stroke: "{EDGE_COLOR}"')
        lines.append(f'    stroke-width: 2')
        lines.append(f'    font-size: 25')
        lines.append(f'  }}')
        lines.append("}")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python svg_to_d2.py <input.svg> [output.d2]")
        sys.exit(1)

    svg_path = sys.argv[1]

    # Default output: same directory as input, with .d2 extension
    input_dir = os.path.dirname(os.path.abspath(svg_path))
    stem = os.path.splitext(os.path.basename(svg_path))[0]
    out_path = sys.argv[2] if len(sys.argv) >= 3 else os.path.join(input_dir, f"{stem}.d2")

    nodes, edges = parse_svg(svg_path)

    if not nodes and not edges:
        print("ERROR: No nodes or edges found. Make sure the SVG uses data-id/data-from/data-to attributes.")
        sys.exit(1)

    d2_code = build_d2(nodes, edges)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(d2_code)
    print(f"Written to: {out_path}")


if __name__ == "__main__":
    main()
