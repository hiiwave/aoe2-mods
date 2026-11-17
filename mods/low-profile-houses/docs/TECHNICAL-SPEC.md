# Technical specification / lightweight architecture

## Current release boundary

The current standard is **0.6x Beta**, with a **120 px upper bound**, starting from original graphics and leaving shorter houses unchanged. The name estimates above-ground height; it is not a uniform image-space scale. The equations below explain the method, while the numerical profile table and checked-in source files below are **historical v0.2 / 110 px examples**, not the current release configuration. The general seam/roof/wall equations also appear in the inspected 120 px builder; some Western assets dispatch to specialized protection rules.

A full current configuration and package manifest are not yet checked in. Do not infer current lifecycle coverage or byte reproducibility from this historical implementation.

## Data flow
Lawful local game SLD files -> bounded decoder -> selected original frame -> age-specific 2D inverse warp -> aligned main / shadow / damage / player layers -> regenerated outline mask -> native SLD writer -> readback validation -> isolated local-mod folder -> ZIP.

No service, backend or database is required. The architecture is an offline asset build pipeline. Current profiles are hand-traced, not automatically generalizable to arbitrary architecture.

Full derivations, historical screenshot examples and the historical 110 px implementation are in [MATHEMATICS.md](MATHEMATICS.md).

## Height and coordinates
Height means the decoded main RGBA layer's nontransparent bounding-box height, excluding the separate shadow layer. Chimneys and visible ground details in the main image count. It is neither a world-space 3D height nor a uniform scale factor.

Image y increases downward. Variants in documents are 1-based; source frame index is variant minus one. Keep this conversion explicit.

For each horizontal coordinate $x$, $t(x)$ is a traced roof/wall seam and $b(x)$ a traced ground/foot line. These are piecewise-linear estimates, not reconstructed 3D geometry.

## Method names
**Rigid Roof-Shift:** translate the roof downward without flattening it; compress the wall band to meet the fixed ground. It fails aesthetically/geometrically when the translated roof consumes the wall or crosses the foot line.

**Roof-Shift Hybrid:** vertically compress the roof around anchor $a$ by scale $k\gt 0$, then translate it downward by $d$. Let $y$ denote an output-image coordinate and $y_s$ the corresponding source coordinate. The transformed seam is:

```math
n(x)=a+k\bigl(t(x)-a\bigr)+d.
```

Provided $n(x)\lt b(x)$, the inverse map has three branches in the active warped region.

Roof branch, for $y\lt n(x)$:

```math
y_s=a+\frac{y-a-d}{k}.
```

Wall branch, for $n(x)\le y\lt b(x)$:

```math
y_s=t(x)+\frac{(y-n(x))(b(x)-t(x))}{b(x)-n(x)}.
```

Ground branch, for $y\ge b(x)$:

```math
y_s=y.
```

The roof formula inverts the scale and translation. The wall formula maps the new seam back to the original seam while fixing the foot line: at $y=n(x)$ it gives $y_s=t(x)$, and at $y=b(x)$ it gives $y_s=b(x)$. Outside the profile's active region, coordinates remain unchanged.

The inspected 120 px generic branch rounds to nearest-pixel sampling, makes out-of-bounds samples transparent, requires at least a 3 px wall band, preserves the separate shadow layer, and copies ground-region pixels unchanged. Western dispatches can apply additional region/cutoff rules. Rebuild the outline mask from transformed main alpha. These coefficients are not equivalent to the total-house reduction.

**Roof-Flatten:** reduce roof pitch while retaining eaves and walls. Trials use per-column maps or piecewise-affine roof meshes. At aggressive targets, the tested fixed-eave meshes fold, but this is not a mathematical impossibility theorem. Redesigning ridge positions/topology can relax the constraint. Do not label a wall-compressing hybrid as pure Roof-Flatten.

## Historical v0.2 parameters (110 px)
| Age / selected variant | Roof scale k | Downward shift d | Anchor y |
|---|---:|---:|---:|
| Dark 2 | 0.90 | 3.0 px | 133 |
| Feudal 2 | $1-\frac{15.5}{93}\approx 0.833333$ | 29.0 px | 181 |
| Castle 2 | 0.70 | 16.6 px | 183 |

Profile control points and sampling details are in src/build_trial.py. Dark leaves the shadow unchanged; Feudal and Castle use the aligned historical transforms. The visible output must be measured after encoding, not inferred from these parameters.

## Historical v0.2 native assets
- b_dark_house_age1_x1.sld
- b_west_house_age2_x1.sld
- b_west_house_age3_x1.sld

Each output has three repeated static frames. Main color, shadow, damage-related and player-color layers retain native representation; the writer is bounded to the inspected layer set. BC1/BC4 encoding is lossy. Alpha/outline equality does not prove color equality or correct engine rendering.

## Historical lifecycle dependency (v0.1 to v0.2)
Old v0.1 contains intact + destruction + rubble for each of three age groups (9 SLDs). New v0.2 has only 3 intact SLDs. Moving the new shape into a full lifecycle version requires regenerating the destruction animation and rubble from the selected variant and compatible warp. Approximately 100 unique destruction frames per age are replicated across three appearance groups.

Damage shading and fire are primarily engine overlays; they do not require hand-drawing every HP state. Correct masks and actual progression still require verification. Generic scaffold art remains original. Old destruction files cannot simply be reused because the starting variant/proportion differs.

## Safety boundaries
Never modify DAT, original graphics or unrelated mod settings. Output to an isolated folder. On install, disable conflicting house mods, restart, and restore prior enabled state on rollback. Never write installation paths into build defaults.

