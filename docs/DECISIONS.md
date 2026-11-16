# Decisions and rationale

| Decision | Rationale / status |
|---|---|
| Graphics-only, no data mod | User rejected data mods; retain normal visual-mod approach. |
| Fire accepted | Actual Anne_HK flat-castle and all-age-TC tests also showed floating flames in sampled states. Accepted limitation, not proof no solution exists. |
| Western + shared Dark asset | Start bounded. Shared Dark consequences explicitly accepted. |
| Three variants unified | Consistent silhouette and direction within each age. |
| Fixed 110 px comparisons | Compare methods at equal total image height where actually achievable. Do not compare 110 vs 140 as if equal. |
| Trial 2/2/2 | User selected shortest-original principle for consistency/scalability; reviewer favored 2/3/2 but selection remains user's 2/2/2. |
| Intact-first POC | Decide standing appearance before spending on damage/destruction. |
| Name methods precisely | Hybrid alone obscured different roof and wall coefficients. Use Roof-Shift Hybrid vs Roof-Flatten, with actual parameters. |
| Keep versions separate | Earlier ZIP and later comparison POCs differed. Explicit labels and manifests prevent another ambiguous comparison. |
| Private GitHub | Review source/specifications without public release of game-derived artwork. |

## Important exploration results
- Old Dark house was 121��84 px and looked too flat. Initial 10% revision preceded final 110 px target.
- Pure rigid30 crossed traced footlines in inspected Feudal/Castle shapes.
- New Hybrid candidates reduce the roof itself more and move it less than the old delivered lifecycle art, preserving more visible wall despite similar total height.
- A roof-only constant-drop mesh crossed fixed eaves at 110 px for inspected Feudal/Castle variants. Some triangles reversed orientation.
- That failure was over-described as ��impossible�� and corrected: it demonstrates a limitation of tested mapping constraints, not every possible roof redesign.
- Roof-Flatten alternatives remain research, not the delivered v0.2 recipe.

## Research reference
Anne_HK catalog: https://sites.google.com/view/aoe-anne-hk/home
Flat Castle: https://www.ageofempires.com/mods/details/60348/
All-age Flat TC: https://www.ageofempires.com/mods/details/72886/

No third-party mod files are included here.


## Subsequent scope decision
The owner accepted the intact 2/2/2 110 px trial after real play and authorized Western lifecycle completion followed by all-civilization expansion. Implementation and coverage remain pending; do not treat authorization as completion.
