"""Manually drawn diagrams: no plotting library has these built in."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyArrow, Wedge


def plasmid_map(df: pd.DataFrame, plasmid_length: int = 5400) -> tuple[plt.Figure, plt.Axes]:
    """Draw a circular plasmid map from a gene table, using Wedge patches
    for each gene arc and arrow markers for strand direction.

    Parameters
    ----------
    df : DataFrame with columns ``gene``, ``start_bp``, ``end_bp``,
        ``strand``, ``color``.
    plasmid_length : total plasmid length in base pairs, used to convert
        positions to angles.
    """
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={"aspect": "equal"})
    r_outer, r_inner = 1.0, 0.85

    # backbone circle
    backbone = plt.Circle((0, 0), (r_outer + r_inner) / 2, fill=False, color="#888888", linewidth=1.5)
    ax.add_patch(backbone)

    def bp_to_angle(bp: float) -> float:
        return 90 - (bp / plasmid_length) * 360

    for _, row in df.iterrows():
        theta1 = bp_to_angle(row["end_bp"])
        theta2 = bp_to_angle(row["start_bp"])
        wedge = Wedge(
            (0, 0), r_outer, theta1, theta2, width=r_outer - r_inner,
            facecolor=row["color"], edgecolor="white", linewidth=1,
        )
        ax.add_patch(wedge)

        mid_bp = (row["start_bp"] + row["end_bp"]) / 2
        mid_angle = np.radians(bp_to_angle(mid_bp))
        label_r = r_outer + 0.18
        lx, ly = label_r * np.cos(mid_angle), label_r * np.sin(mid_angle)
        ax.text(lx, ly, row["gene"], ha="center", va="center", fontsize=9, fontweight="bold")

        arrow_r = (r_outer + r_inner) / 2
        ax_angle = np.radians(bp_to_angle(row["end_bp"] if row["strand"] == "+" else row["start_bp"]))
        tip_angle = np.radians(bp_to_angle(row["start_bp"] if row["strand"] == "+" else row["end_bp"]))
        x0, y0 = arrow_r * np.cos(ax_angle), arrow_r * np.sin(ax_angle)
        x1, y1 = arrow_r * np.cos(tip_angle), arrow_r * np.sin(tip_angle)
        dx, dy = (x1 - x0) * 0.001, (y1 - y0) * 0.001
        ax.add_patch(
            FancyArrow(x0, y0, dx, dy, width=0.0001, head_width=0.05, head_length=0.05, color="black")
        )

    ax.text(0, 0, f"{plasmid_length} bp", ha="center", va="center", fontsize=11, fontweight="bold")
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.axis("off")
    ax.set_title("Synthetic Plasmid Map", fontweight="bold")
    return fig, ax


def _build_tree_layout(edges: pd.DataFrame) -> dict:
    """Compute (x, y) positions for every node: x = cumulative branch
    length from root, y = evenly spaced leaf order for leaves, with
    internal nodes at the mean y of their children.
    """
    children = {}
    depth = {}
    for _, row in edges.iterrows():
        children.setdefault(row["parent"], []).append((row["child"], row["branch_length"]))

    all_children = set(edges["child"])
    all_parents = set(edges["parent"])
    root = next(iter(all_parents - all_children))
    depth[root] = 0.0

    def set_depth(node):
        for child, bl in children.get(node, []):
            depth[child] = depth[node] + bl
            set_depth(child)

    set_depth(root)

    leaves = sorted(all_children - all_parents)
    y_pos = {leaf: i for i, leaf in enumerate(leaves)}

    def set_y(node):
        kids = children.get(node, [])
        if not kids:
            return y_pos[node]
        ys = [set_y(child) for child, _ in kids]
        y_pos[node] = sum(ys) / len(ys)
        return y_pos[node]

    set_y(root)
    return {"depth": depth, "y": y_pos, "children": children, "root": root}


def phylo_tree(edges: pd.DataFrame) -> tuple[plt.Figure, plt.Axes]:
    """Draw a phylogenetic tree from a parent/child/branch_length edge
    table, using plain line segments (a manual rectangular dendrogram)
    rather than a library dendrogram function.

    Parameters
    ----------
    edges : DataFrame with columns ``parent``, ``child``, ``branch_length``.
    """
    layout = _build_tree_layout(edges)
    depth, y_pos, children, root = layout["depth"], layout["y"], layout["children"], layout["root"]

    fig, ax = plt.subplots(figsize=(8, 5.5))

    def draw(node):
        for child, _ in children.get(node, []):
            x0, x1 = depth[node], depth[child]
            y0, y1 = y_pos[node], y_pos[child]
            ax.plot([x0, x0], [y0, y1], color="#444444", linewidth=1.5)
            ax.plot([x0, x1], [y1, y1], color="#444444", linewidth=1.5)
            draw(child)

    draw(root)

    leaves = sorted(set(edges["child"]) - set(edges["parent"]))
    for leaf in leaves:
        ax.text(depth[leaf] + 0.01, y_pos[leaf], leaf.replace("_", " "), va="center", fontsize=10)

    ax.set_xlabel("Branch length")
    ax.set_yticks([])
    ax.set_title("Phylogenetic Tree, Drawn Manually", fontweight="bold")
    ax.set_xlim(-0.02, max(depth.values()) + 0.35)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    return fig, ax
