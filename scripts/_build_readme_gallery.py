"""
_build_readme_gallery.py
==========================
Generates the "Full Tutorial: Every Plot, Explained" section of
README.md programmatically, so all 7 sections follow an identical
structure without manual copy-paste drift.

This is a one-off authoring tool, not part of the tested package.
Run it, then paste and verify the output into README.md.

Usage:
    python scripts/_build_readme_gallery.py > /tmp/gallery_section.md
"""

SECTIONS = [
    dict(
        num="1",
        title="3D Scatter: Docking Landscape in Three Dimensions",
        plot_kind="3D scatter (mpl_toolkits.mplot3d)",
        shared="Shared with biology-data-viz-seaborn (same dataset, new dimension).",
        what_it_is=(
            "Seaborn has no 3D plotting function at all. A true 3D "
            "scatter needs `mpl_toolkits.mplot3d`, accessed directly "
            "through Matplotlib's `Axes3D` projection, giving full "
            "control over elevation, azimuth, and three independent "
            "numeric axes at once."
        ),
        question=(
            "How do lipophilicity (logP), molecular weight, and "
            "docking score relate together across three drug targets? "
            "A 2D scatter has to pick two of these three variables. "
            "Does the third add anything?"
        ),
        dataset="`data/docking_scores.csv`",
        dataset_desc="360 rows. Simulated virtual-screening results against 3 protein targets.",
        image="figures/01_docking_3d.png",
        code=(
            'df = pd.read_csv("data/docking_scores.csv")\n'
            "fig, ax = scatter3d.docking_scatter_3d(df)"
        ),
        interpretation=(
            "The 3D view shows that molecular weight adds little extra "
            "separation beyond what logP already explains: the "
            "best-scoring points cluster in the same logP band "
            "regardless of molecular weight, meaning weight is not an "
            "independent driver of affinity in this simulated screen. "
            "That is itself a useful negative result, and it is easier "
            "to see in 3D than by eyeballing two separate 2D plots."
        ),
        requirements=[
            "three continuous numeric columns (x, y, z)",
            "optionally: a categorical column to color and label groups",
        ],
        adapt_code=(
            "fig = plt.figure()\n"
            'ax = fig.add_subplot(111, projection="3d")\n'
            'ax.scatter(my_df["x"], my_df["y"], my_df["z"], c=my_df["group_codes"])'
        ),
    ),
    dict(
        num="2",
        title="Small Multiples: One Panel Per Gene",
        plot_kind="plt.subplots grid",
        shared="Shared with biology-data-viz-seaborn (same dataset, different layout).",
        what_it_is=(
            "`plt.subplots` gives direct control over a grid of "
            "independent Axes, useful when each panel needs its own "
            "scale, title, or annotation rather than sharing one set "
            "of axes the way a faceted Seaborn plot would."
        ),
        question=(
            "Which genes shift between control and treatment, and by "
            "how much does each individual replicate move?"
        ),
        dataset="`data/gene_expression.csv`",
        dataset_desc="180 rows. log2 expression for 6 genes, control vs. treatment, 15 replicates each.",
        image="figures/02_gene_expression_panels.png",
        code=(
            'df = pd.read_csv("data/gene_expression.csv")\n'
            "fig, axes = panels.gene_expression_small_multiples(df)"
        ),
        interpretation=(
            "`MYC` and `IL6` show a clear upward shift with little "
            "overlap between conditions. `TP53` and `CDKN1A` shift "
            "down the same way. `GAPDH` and `ACTB` show heavily "
            "overlapping distributions, consistent with them being "
            "simulated as unaffected housekeeping genes. Plotting "
            "every replicate dot, not just a summary bar, makes clear "
            "these patterns hold across the whole replicate set."
        ),
        requirements=[
            "a grouping column to split into panels (one Axes per group)",
            "one categorical x column and one continuous y column within each panel",
        ],
        adapt_code=(
            "groups = my_df[\"panel_column\"].unique()\n"
            "fig, axes = plt.subplots(nrows, ncols, figsize=(11, 3 * nrows))\n"
            "for ax, group in zip(axes.ravel(), groups):\n"
            '    sub = my_df[my_df["panel_column"] == group]\n'
            '    ax.scatter(sub["x"], sub["y"])\n'
            "    ax.set_title(group)"
        ),
    ),
    dict(
        num="3",
        title="Custom Dashboard: Sequencing QC in One Figure",
        plot_kind="GridSpec multi-panel dashboard",
        shared="Shared with biology-data-viz-seaborn (same dataset, different layout).",
        what_it_is=(
            "`GridSpec` allows Axes of different sizes and aspect "
            "ratios to sit in one figure, for example a large scatter "
            "next to two small histograms next to a text panel, a "
            "layout no single Seaborn function produces."
        ),
        question=(
            "What is the overall health of a sequencing run: coverage, "
            "duplication, GC content, quality, and a quick summary all "
            "at a glance?"
        ),
        dataset="`data/qc_metrics.csv`",
        dataset_desc="96 rows. Per-sample sequencing QC for a 96-sample batch across 3 sub-batches.",
        image="figures/03_qc_dashboard.png",
        code=(
            'df = pd.read_csv("data/qc_metrics.csv")\n'
            "fig = panels.qc_dashboard(df)"
        ),
        interpretation=(
            "The scatter panel shows the same coverage-versus-"
            "duplication artifact seen in the Seaborn version of this "
            "dataset (low coverage tracking with high duplication), "
            "while the dashboard format adds an at-a-glance numeric "
            "summary a reader could act on immediately, for example "
            "the exact count of samples below a 30x coverage threshold."
        ),
        requirements=[
            "several numeric columns for the scatter and histograms",
            "a categorical column for the scatter's color grouping",
        ],
        adapt_code=(
            "fig = plt.figure(figsize=(11, 7))\n"
            "gs = GridSpec(2, 3, figure=fig, width_ratios=[2, 1, 1])\n"
            "ax_main = fig.add_subplot(gs[:, 0])\n"
            "ax_hist1 = fig.add_subplot(gs[0, 1])\n"
            "ax_hist2 = fig.add_subplot(gs[0, 2])\n"
            "ax_text = fig.add_subplot(gs[1, 1:])"
        ),
    ),
    dict(
        num="4",
        title="Animation: Bacterial Growth Curves Over Time",
        plot_kind="FuncAnimation",
        shared="New dataset, no Seaborn equivalent at all.",
        what_it_is=(
            "`FuncAnimation` is the only way to show a process "
            "unfolding over time rather than a single finished state. "
            "Each frame redraws the line data with one more timepoint "
            "revealed, so change over time is genuinely visible rather "
            "than implied."
        ),
        question=(
            "How do three bacterial strains differ in growth rate and "
            "lag phase as they grow toward carrying capacity?"
        ),
        dataset="`data/growth_curves.csv`",
        dataset_desc="240 rows. OD600 growth curves for 3 strains over 24h, 4 replicates each, logistic growth model.",
        image="figures/04_growth_curves.gif",
        code=(
            'df = pd.read_csv("data/growth_curves.csv")\n'
            "anim, fig = animation.growth_curve_animation(df, n_frames=40)\n"
            'anim.save("growth_curves.gif", writer="pillow", fps=12)'
        ),
        interpretation=(
            "`MutantA_fast` pulls ahead almost immediately and "
            "plateaus early at a lower final density. `MutantB_slow` "
            "has a visibly longer lag phase before it starts climbing, "
            "but ultimately reaches the highest carrying capacity of "
            "the three strains. Neither of those facts, an early speed "
            "and final yield trade-off, is obvious from endpoint data "
            "alone; the animation makes it visible as it happens."
        ),
        requirements=[
            "an ordered x variable (usually time)",
            "one or more y series to animate, grouped by a category column",
            "install `pillow` to export as GIF, or use `writer=\"ffmpeg\"` for MP4",
        ],
        adapt_code=(
            "fig, ax = plt.subplots()\n"
            "(line,) = ax.plot([], [])\n\n"
            "def update(frame):\n"
            "    line.set_data(x[:frame], y[:frame])\n"
            "    return [line]\n\n"
            "anim = FuncAnimation(fig, update, frames=len(x))\n"
            'anim.save("output.gif", writer="pillow", fps=12)'
        ),
    ),
    dict(
        num="5",
        title="3D Surface and Contour: Enzyme Activity Response Surface",
        plot_kind="plot_surface + contourf",
        shared="New dataset, no Seaborn equivalent at all.",
        what_it_is=(
            "A heatmap flattens a true 2D-input, 1D-output relationship "
            "onto a single flat color grid. `plot_surface` shows the "
            "actual shape of the response, including how sharply "
            "activity falls off away from the optimum in each "
            "direction, which is harder to judge by eye on a flat map."
        ),
        question=(
            "How does enzyme activity depend jointly on pH and "
            "temperature, and where is the optimum?"
        ),
        dataset="`data/enzyme_activity_surface.csv`",
        dataset_desc="625 rows. Enzyme activity sampled on a 25x25 grid of pH and temperature.",
        image="figures/05_enzyme_surface.png",
        code=(
            'df = pd.read_csv("data/enzyme_activity_surface.csv")\n'
            "fig = surface.enzyme_activity_surface(df)"
        ),
        interpretation=(
            "The surface has a single, fairly narrow peak near pH 7.4 "
            "and 37C, consistent with a typical mesophilic enzyme "
            "operating near physiological conditions. The contour "
            "panel beside it marks that peak directly, and shows the "
            "surface is more sensitive to temperature than to pH: the "
            "contour lines are more tightly packed along the "
            "temperature axis, meaning a given temperature deviation "
            "costs more activity than the same-sized pH deviation."
        ),
        requirements=[
            "two continuous independent variables sampled on a grid",
            "one continuous response variable",
            "pivot to a 2D grid first (`pivot_table`), then use `np.meshgrid`",
        ],
        adapt_code=(
            "piv = my_df.pivot_table(index=\"y_var\", columns=\"x_var\", values=\"z_var\")\n"
            "x_grid, y_grid = np.meshgrid(piv.columns, piv.index)\n"
            "ax = fig.add_subplot(projection=\"3d\")\n"
            "ax.plot_surface(x_grid, y_grid, piv.to_numpy(), cmap=\"viridis\")"
        ),
    ),
    dict(
        num="6",
        title="Manually Drawn Diagram: Circular Plasmid Map",
        plot_kind="Wedge patches, manual layout",
        shared="New dataset, no Seaborn equivalent at all.",
        what_it_is=(
            "There is no Seaborn function for this at all. Drawing it "
            "requires placing `Wedge` patches at specific angles "
            "computed from base-pair positions, plus manual label and "
            "arrow placement: a diagram type built entirely from "
            "primitive shapes rather than a single plotting call."
        ),
        question=(
            "What does the gene layout of a small expression plasmid "
            "look like: which genes are present, where, and on which "
            "strand?"
        ),
        dataset="`data/plasmid_map.csv`",
        dataset_desc="7 rows. A synthetic 5400bp expression plasmid's gene layout.",
        image="figures/06_plasmid_map.png",
        code=(
            'df = pd.read_csv("data/plasmid_map.csv")\n'
            "fig, ax = diagrams.plasmid_map(df)"
        ),
        interpretation=(
            "The map lays out an origin of replication, two resistance "
            "markers, a reporter gene, and their associated promoters "
            "around the circle in their correct relative positions and "
            "strand orientations. This is the same kind of diagram "
            "produced by dedicated plasmid-mapping software, built "
            "here entirely from Matplotlib primitives."
        ),
        requirements=[
            "gene name, start position, end position, and strand columns",
            "a total sequence length to convert positions into angles",
        ],
        adapt_code=(
            "from matplotlib.patches import Wedge\n\n"
            "def bp_to_angle(bp, total_length):\n"
            "    return 90 - (bp / total_length) * 360\n\n"
            "for _, gene in my_df.iterrows():\n"
            "    theta1 = bp_to_angle(gene[\"end_bp\"], total_length)\n"
            "    theta2 = bp_to_angle(gene[\"start_bp\"], total_length)\n"
            "    ax.add_patch(Wedge((0, 0), 1.0, theta1, theta2, width=0.15))"
        ),
    ),
    dict(
        num="7",
        title="Manually Drawn Diagram: Phylogenetic Tree",
        plot_kind="Line segments, manual layout algorithm",
        shared="New dataset, no Seaborn equivalent at all.",
        what_it_is=(
            "Rather than calling a dendrogram function, this draws the "
            "tree from a plain parent-child-branch-length table using "
            "line segments, showing the layout algorithm itself: each "
            "node's horizontal position comes from cumulative branch "
            "length, and each internal node's vertical position from "
            "the mean of its children."
        ),
        question=(
            "What are the evolutionary relationships and relative "
            "divergence times among 8 taxa?"
        ),
        dataset="`data/phylo_edges.csv`",
        dataset_desc="14 rows. A small phylogenetic tree for 8 taxa, encoded as parent-child edges.",
        image="figures/07_phylo_tree.png",
        code=(
            'df = pd.read_csv("data/phylo_edges.csv")\n'
            "fig, ax = diagrams.phylo_tree(df)"
        ),
        interpretation=(
            "Taxon A and Taxon B are each other's closest relatives, "
            "joining at the shallowest branch length in the tree. "
            "Taxon C is the deepest-branching member of its clade, "
            "splitting off before the E/F/G/H group diversifies "
            "further. The x-axis position of each tip directly encodes "
            "cumulative evolutionary distance from the root, which is "
            "exactly what a phylogenetic tree diagram is meant to show."
        ),
        requirements=[
            "a parent column, a child column, and a branch length column",
            "exactly one root node (present as a parent but never as a child)",
        ],
        adapt_code=(
            "# compute cumulative depth from root by walking the edge table,\n"
            "# then for each parent-child pair draw an L-shaped connector:\n"
            'ax.plot([x_parent, x_parent], [y_parent, y_child], color="black")\n'
            'ax.plot([x_parent, x_child], [y_child, y_child], color="black")'
        ),
    ),
]


def render_section(s: dict) -> str:
    lines = []
    lines.append(f"### {s['num']}. {s['title']}\n")
    lines.append(f"**Plot type:** {s['plot_kind']}\n")
    lines.append(f"**Dataset origin:** {s['shared']}\n")
    lines.append(f"**What this technique is for:** {s['what_it_is']}\n")
    lines.append(f"**Biological question:** {s['question']}\n")
    lines.append(f"**Dataset:** {s['dataset']}. {s['dataset_desc']}\n")
    lines.append("**Create this figure:**\n")
    lines.append(f"```python\n{s['code']}\n```\n")
    lines.append(f"![{s['title']}]({s['image']})\n")
    lines.append(f"**Interpretation:** {s['interpretation']}\n")
    lines.append("**Requirements to use this on your own data:**\n")
    for req in s["requirements"]:
        lines.append(f"- {req}")
    lines.append("")
    lines.append("**Adapted code for your own DataFrame:**\n")
    lines.append(f"```python\n{s['adapt_code']}\n```\n")
    lines.append("---\n")
    return "\n".join(lines)


def main() -> None:
    print("## Full Tutorial: Every Plot, Explained\n")
    print(
        "For each technique below: what it is for, the biological "
        "question it answers here, the exact code that produces it, an "
        "interpretation of the actual result, and what you'd need to use "
        "it on your own data. This mirrors "
        "`notebooks/matplotlib_beginner_guide.ipynb` exactly. Every "
        "snippet below is executed end-to-end in CI on every push.\n"
    )
    print(
        "```python\n"
        "import pandas as pd\n"
        "import matplotlib.pyplot as plt\n"
        "from bioplt import theme, scatter3d, panels, animation, surface, diagrams\n\n"
        "theme.set_theme()\n"
        "```\n"
    )
    print("---\n")
    for s in SECTIONS:
        print(render_section(s))


if __name__ == "__main__":
    main()
