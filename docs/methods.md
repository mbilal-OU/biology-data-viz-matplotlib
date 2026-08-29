# Methods and Interpretation

## Phylogenomics panel

The tree root is the single node that appears as a parent but never as a child.
Cumulative branch length sets each node's horizontal position. A depth-first
traversal preserves topology when assigning tip positions. Internal nodes are
centered between their descendants, and the resulting tip order is applied to
the metadata and gene-family tables.

Validation rejects missing columns, negative or non-numeric branch lengths,
repeated children, cycles, multiple roots, disconnected nodes, mismatched taxa,
and non-binary presence values. Invariant gene families are omitted from the
displayed accessory matrix.

The rectangular layout does not imply divergence time. Time interpretation
requires a calibrated input tree, and this code does not infer phylogeny.

## Pangenome accumulation

For each genome count, the plot preserves every supplied resampling trajectory.
The strong line is the arithmetic mean across replicates and the band spans the
empirical 2.5 and 97.5 percentiles. These bands describe order sensitivity in
the simulation; they are not model-based confidence or prediction intervals.

## Synteny tracks

Gene coordinates determine arrow position and length, while strand determines
arrow direction. Each polygon connects an explicitly named feature pair in
adjacent regions. Opacity varies with supplied percent identity.

The function does not align sequences or infer orthology, homology, or synteny.
Those relationships must come from an upstream analysis.

## Plasmid and tree diagrams

The plasmid renderer validates positive circular length, coordinates, and strand
before drawing tangent arrows and a category legend. The tree renderer shares
the same validation and topology logic used by the composite panel.

## Three-dimensional graphics

3D scatter and surface views can reveal joint structure, but projection,
occlusion, and viewpoint can make precise comparisons harder. The enzyme figure
therefore includes a contour projection, and the docking example treats the 3D
view as exploratory rather than uniquely superior to 2D alternatives.

## Reproducibility

All CSV files are generated with `numpy.random.default_rng(42)`. CI reruns the
generator and fails if committed data change. Both notebooks execute from a
clean environment, figures render headlessly, and the distributable package is
built on every change.
