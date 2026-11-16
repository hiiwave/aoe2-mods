# Product requirements

Status: reviewable working specification, 2026-11-16. Author: hiiwave.

## Problem and outcome
Tall isometric house roofs can hide gaps between buildings, especially on slopes. Reduce visual obstruction while retaining a recognizable house and its original ground placement. The goal is better visibility, not a new collision model or a guarantee that every hidden gap becomes visible.

## Scope
1. Western architecture houses: Feudal, Castle and Imperial (Castle/Imperial share art).
2. Shared default Dark Age house asset is explicitly included, even though this affects other civilizations using it.
3. Current prototype is normal-resolution, intact houses only. Damage/destruction work is deferred until the standing appearance is accepted.
4. Author labels and public attribution use **hiiwave**, never a personal full name.
5. User installs on their own PC; SER6 is a development/test machine, not the assumed user-test destination.

## Current selection
| Age | Source variation (1-based) | Source main height | Target | Method |
|---|---:|---:|---:|---|
| Dark | 2 | 119 px | 110 px | Roof-Shift Hybrid |
| Feudal | 2 | 155 px | 110 px | Roof-Shift Hybrid |
| Castle / Imperial | 2 | 153 px | 110 px | Roof-Shift Hybrid |

This is the user's selected trial, even though visual review favored Feudal 3. Do not silently substitute the reviewer's choice.

## Selection policy for later expansion
Start with the shortest original variant per architecture/age to keep a consistent, scalable process. Prefer another variant only if the shortened result is materially clearer or better looking. Avoid mandatory exhaustive three-way experiments for every future civilization. Expansion was subsequently explicitly authorized; see latest follow-through below.

## Acceptance criteria
- Full standing-house main alpha bounds are exactly 110 px high; width and hotspot retained.
- Uniform shape across all three static variation slots in each selected age.
- No rule/data files; no base-game overwrite.
- Preserve visual ground position, player-color support and aligned native layers. Binary validity is not visual correctness.
- Preview comparisons show original and candidate at common pixel scale, with explicit method, height and version labels.
- User real-play assessment remains the strongest acceptance test for occlusion/readability.
- Packaging changes alone or author metadata edits do not warrant repeated test requests.

## Non-goals / accepted limits
No data mod. Do not fix floating flames by moving shared effects or changing game data. No ranked/multiplayer compatibility promise without evidence. Construction scaffolding can remain original. A full lifecycle release is separate from this intact trial.


## Latest authorized follow-through
After real-play testing, the owner reported no problem with the 2/2/2 110 px trial and requested completion of the remaining collapse/lifecycle states. Western completion is the first milestone; all remaining civilizations are then in scope. These are authorized work items, **not completed features**. Use the shortest-original default and exceptions policy while retaining graphics-only constraints and the accepted fire limitation. Record each architecture/age coverage rather than claiming all civilizations complete after a subset.
