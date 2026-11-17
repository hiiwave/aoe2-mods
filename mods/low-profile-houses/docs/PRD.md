# Product requirements: 0.6x Beta

Author: **hiiwave**. Current standard: **120 px upper bound**.

## Purpose

Make bases easier to read in competitive play without replacing houses with flat foundations. Preserve recognizable architectural character while exposing more nearby units, terrain and wall gaps. This is a visibility improvement, not a change to passability.

## Current requirements

- Work from original game graphics. Do not rescale the former 110 px outputs.
- Target 120 px for taller standard houses; do not enlarge shorter originals, including the shared 119 px Dark Age house.
- Select a variant per architecture/age. Use the owner's reviewed selections, not a universal variant number or an unreviewed reviewer preference.
- Repeat the selected shape across variation slots for consistency; document the loss of variety.
- Keep ground placement, footprint, collision and game rules unchanged. Update visual outline/mask data consistently with the transformed sprite where applicable.
- Preserve player-color/layer alignment; validate encoded assets and sample them in game. A valid file is not proof of correct rendering.
- Present real, labelled before/after examples at comparable viewing scale. Do not present historical 110 px captures as current evidence.
- Attribute the mod to hiiwave. Keep the source repository private until explicitly authorized otherwise.

## Scope and acceptance

Standard houses across competitive architecture sets are the intended scope. Greek/Chronicles coverage is not a required acceptance gate; the special Norse longhouse is excluded. Exact delivered asset coverage must come from a current package manifest, not the historical v0.4 count.

Standing, damage, destruction and rubble evidence must identify the package tested. No claim of full current lifecycle verification follows from earlier-version tests. Existing gameplay screenshots establish sampled visual results only.

Scaffolding and floating fire positions are accepted limitations. Separate transparency, tree and military-building experiments do not change this house beta's specification.

## Historical requirements

Earlier Western-only 2/2/2, intact-only and 110 px milestones are superseded as current requirements. See [historical baselines](HISTORICAL-BASELINES.md), [decisions](DECISIONS.md) and [versioned test records](TEST-STATUS.md) for their context. Earlier prose remains available in Git history.
