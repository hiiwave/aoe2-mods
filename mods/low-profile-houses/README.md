# Low-Profile Houses - 0.6x (Beta)

Author: **hiiwave**.

## A clearer view, without flat foundations

Tall houses can hide units, terrain and small gaps in a wall. Low-Profile Houses lowers their silhouette while keeping recognizable architecture. This is a visual trade-off: clearer bases and consistent house shapes, rather than maximum original variety.

![Original versus 0.6x Beta in a real game](docs/images/current-06x/live-25m-before-after.jpg)

*Around 25 minutes of gameplay. Left: original graphics. Right: 0.6x Beta. The comparison illustrates reduced obstruction, not changed collision or a newly passable route.*

## Current standard

- **120 px upper bound**, measured in the native standing-house main image. Houses at or below the target are not enlarged.
- Transform from the **original assets**, not by enlarging the older 110 px output.
- One selected variant per architecture and age, repeated across the normal variation slots for a consistent look. Selections are asset-specific.
- **0.6x is an approximate above-ground height description**, not a universal 0.6 multiplier on image coordinates or an exact recovered 3D measurement.
- Graphics only. Ground footprints, collision and gameplay data remain unchanged. The sprite selection outline is a separate visual concern from ground collision.

## Install

[Open the published mod on Age of Empires](https://www.ageofempires.com/mods/details/583664).

## Method at a glance

Keep the ground fixed; shorten the roof and the wall band separately, with per-house parameters:

```math
H_{\mathrm{target}}=\min(H_{\mathrm{original}},120\,\mathrm{px}),\qquad n(x)=a+k[t(x)-a]+d.
```

Here $t(x)$ is the original roof/wall seam; $n(x)$ is the transformed seam. Roof scale $k$, shift $d$ and anchor $a$ vary by asset. Special cases protect details and ground contact; this is **not a uniform 0.6 image resize**.

![World-coordinate projection schematic](docs/images/lecture-world-axes.svg)

*Coordinate illustration, not a sprite control mesh. [Transformation details](docs/TECHNICAL-SPEC.md) · [Mathematical derivation](docs/MATHEMATICS.md)*

## Using the beta

Enable only one house-height mod at a time; disable conflicting house-graphics mods and restart the game after changing them. Construction scaffolding and fire-effect positions remain original, so flames can appear above the shortened roof. Special Norse longhouses are excluded. Greek/Chronicles support is not an acceptance requirement for this competitive-gameplay project.

The before/after above is current visual evidence, not exhaustive testing of every civilization, lifecycle state or player color. See [verification boundaries](docs/TEST-STATUS.md).

## Documentation

- [Current gameplay comparison](docs/GAMEPLAY-GALLERY.md)
- [Product requirements](docs/PRD.md)
- [Technical specification](docs/TECHNICAL-SPEC.md)
- [Mathematics and annotated house diagrams](docs/MATHEMATICS.md)
- [Decisions and alternatives](docs/DECISIONS.md)
- [Test status and evidence](docs/TEST-STATUS.md)
- [Build scope and instructions](docs/BUILD.md)
- [Historical 110 px baselines](docs/HISTORICAL-BASELINES.md)
- [Rights and repository boundaries](docs/RIGHTS.md)

## Source versus release

The checked-in builder reproduces the **historical v0.2 three-sprite 110 px trial**. The v0.4 manifests also document a historical 110 px package. Neither is a complete reproducible source export of the current 0.6x Beta. Current parameters, package manifests and lifecycle verification must be imported and checked before claiming that capability.

Raw game assets and mod binaries are excluded from this repository. Rebuilding historical examples requires a lawful local game installation. [License](../../LICENSE) and [game-content notice](../../GAME-CONTENT-NOTICE.md).
