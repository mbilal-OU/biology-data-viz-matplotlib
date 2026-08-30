"""Manually drawn diagrams: no plotting library has these built in."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyArrowPatch, Patch, Wedge


def _require_columns(df: pd.DataFrame, required: set[str]) -> None:
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    if df.empty:
        raise ValueError("Input data must contain at least one row")


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
    _require_columns(df, {"gene", "category", "start_bp", "end_bp", "strand", "color"})
    if plasmid_length <= 0:
        raise ValueError("plasmid_length must be positive")
    if not df["strand"].isin(["+", "-"]).all():
        raise ValueError("strand must contain only '+' and '-'")
    if (df["start_bp"] < 0).any() or (df["end_bp"] > plasmid_length).any():
        raise ValueError("Feature coordinates must fall within plasmid_length")
    if (df["end_bp"] <= df["start_bp"]).any():
        raise ValueError("Each end_bp must be greater than start_bp")

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={"aspect": "equal"})
    r_outer, r_inner = 1.0, 0.85

    # backbone circle
    backbone = plt.Circle((0, 0), (r_outer + r_inner) / 2, fill=False, color="#888888", linewidth=1.5)
    ax.add_patch(backbone)

    def bp_to_angle(bp: float) -> float:
        return 90 - (bp / plasmid_length) * 360

    for feature_index, (_, row) in enumerate(df.iterrows()):
        theta1 = bp_to_angle(row["end_bp"])
        theta2 = bp_to_angle(row["start_bp"])
        wedge = Wedge(
            (0, 0),
            r_outer,
            theta1,
            theta2,
            width=r_outer - r_inner,
            facecolor=row["color"],
            edgecolor="white",
            linewidth=1,
        )
        ax.add_patch(wedge)

        mid_bp = (row["start_bp"] + row["end_bp"]) / 2
        mid_angle = np.radians(bp_to_angle(mid_bp))
        feature_span = row["end_bp"] - row["start_bp"]
        short_feature_offset = 0.11 * (feature_index % 2) if feature_span < 250 else 0.0
        label_r = r_outer + 0.18 + short_feature_offset
        lx, ly = label_r * np.cos(mid_angle), label_r * np.sin(mid_angle)
        horizontal_alignment = "left" if lx > 0.15 else "right" if lx < -0.15 else "center"
        ax.text(
            lx,
            ly,
            row["gene"],
            ha=horizontal_alignment,
            va="center",
            fontsize=9,
            fontweight="bold",
        )

        arrow_r = (r_outer + r_inner) / 2
        direction = -1 if row["strand"] == "+" else 1
        start_angle = mid_angle - direction * 0.09
        end_angle = mid_angle + direction * 0.09
        start_xy = (arrow_r * np.cos(start_angle), arrow_r * np.sin(start_angle))
        end_xy = (arrow_r * np.cos(end_angle), arrow_r * np.sin(end_angle))
        ax.add_patch(
            FancyArrowPatch(
                start_xy,
                end_xy,
                arrowstyle="-|>",
                mutation_scale=12,
                linewidth=1.2,
                color="#222222",
                connectionstyle="arc3,rad=0.08",
            )
        )

    ax.text(0, 0, f"{plasmid_length} bp", ha="center", va="center", fontsize=11, fontweight="bold")
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.axis("off")
    ax.set_title("Synthetic Plasmid Map", fontweight="bold")
    legend_handles = [
        Patch(facecolor=color, edgecolor="white", label=category)
        for category, color in df.drop_duplicates("category")[["category", "color"]].itertuples(index=False)
    ]
    ax.legend(handles=legend_handles, loc="lower center", bbox_to_anchor=(0.5, -0.02), ncol=3, frameon=False)
    return fig, ax


def _build_tree_layout(edges: pd.DataFrame) -> dict:
    """Compute (x, y) positions for every node: x = cumulative branch
    length from root, y = evenly spaced leaf order for leaves, with
    internal nodes at the mean y of their children.
    """
    _require_columns(edges, {"parent", "child", "branch_length"})
    if edges[["parent", "child"]].isna().any().any():
        raise ValueError("Tree node names cannot be missing")
    if edges["child"].duplicated().any():
        duplicates = sorted(edges.loc[edges["child"].duplicated(), "child"].unique())
        raise ValueError(f"Each child must have one parent; repeated: {', '.join(duplicates)}")
    if not pd.api.types.is_numeric_dtype(edges["branch_length"]):
        raise ValueError("branch_length must be numeric")
    if (edges["branch_length"] < 0).any():
        raise ValueError("branch_length cannot be negative")

    children = {}
    depth = {}
    for _, row in edges.iterrows():
        children.setdefault(row["parent"], []).append((row["child"], row["branch_length"]))

    all_children = set(edges["child"])
    all_parents = set(edges["parent"])
    roots = all_parents - all_children
    if len(roots) != 1:
        raise ValueError(f"Tree must contain exactly one root; found {len(roots)}")
    root = next(iter(roots))
    depth[root] = 0.0

    visiting: set[str] = set()
    visited: set[str] = set()

    def set_depth(node):
        if node in visiting:
            raise ValueError("Tree contains a directed cycle")
        visiting.add(node)
        for child, bl in children.get(node, []):
            depth[child] = depth[node] + bl
            set_depth(child)
        visiting.remove(node)
        visited.add(node)

    set_depth(root)
    all_nodes = all_parents | all_children
    if visited != all_nodes:
        unreachable = sorted(all_nodes - visited)
        raise ValueError(f"Tree contains disconnected nodes: {', '.join(unreachable)}")

    leaves = []

    def collect_leaves(node):
        kids = children.get(node, [])
        if not kids:
            leaves.append(node)
        for child, _ in kids:
            collect_leaves(child)

    collect_leaves(root)
    y_pos = {leaf: i for i, leaf in enumerate(leaves)}

    def set_y(node):
        kids = children.get(node, [])
        if not kids:
            return y_pos[node]
        ys = [set_y(child) for child, _ in kids]
        y_pos[node] = sum(ys) / len(ys)
        return y_pos[node]

    set_y(root)
    return {
        "depth": depth,
        "y": y_pos,
        "children": children,
        "root": root,
        "leaves": leaves,
    }


def phylo_tree(
    edges: pd.DataFrame,
    ax: plt.Axes | None = None,
    *,
    show_tip_labels: bool = True,
) -> tuple[plt.Figure, plt.Axes]:
    """Draw a phylogenetic tree from a parent/child/branch_length edge
    table, using plain line segments (a manual rectangular dendrogram)
    rather than a library dendrogram function.

    Parameters
    ----------
    edges : DataFrame with columns ``parent``, ``child``, ``branch_length``.
    """
    layout = _build_tree_layout(edges)
    depth, y_pos, children, root = layout["depth"], layout["y"], layout["children"], layout["root"]

    fig, ax = (ax.figure, ax) if ax is not None else plt.subplots(figsize=(8, 5.5))

    def draw(node):
        for child, _ in children.get(node, []):
            x0, x1 = depth[node], depth[child]
            y0, y1 = y_pos[node], y_pos[child]
            ax.plot([x0, x0], [y0, y1], color="#444444", linewidth=1.5)
            ax.plot([x0, x1], [y1, y1], color="#444444", linewidth=1.5)
            draw(child)

    draw(root)

    leaves = layout["leaves"]
    if show_tip_labels:
        for leaf in leaves:
            ax.text(depth[leaf] + 0.01, y_pos[leaf], leaf.replace("_", " "), va="center", fontsize=10)

    ax.set_xlabel("Branch length")
    ax.set_yticks([])
    ax.set_title("Phylogenetic Tree, Drawn Manually", fontweight="bold")
    ax.set_xlim(-0.02, max(depth.values()) + 0.35)
    ax.set_ylim(-0.6, len(leaves) - 0.4)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    return fig, ax
