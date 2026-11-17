# Historical baselines: 110 px

These records describe earlier packages, not the current 0.6x Beta. Their tests and hashes must not be attributed to the current build.

## Archived v0.4 baseline (110 px)

**17 standard-house architecture sets, 108 native SLD files:** 36 intact, 36 destruction and 36 rubble assets. Every selected intact sprite has a **110 px** visible main-alpha height. Roof-Shift Hybrid uses per-asset roof/wall control profiles, calibrated roof scaling and translation, and fixed ground contact. Source variants and parameter choices are asset-specific, not a universal 2/2/2 preset.

The package includes standard-house assets mapped across 62 installed non-Gaia civilization records, including Chronicles assets. Special Norse longhouses are excluded. This describes asset coverage, **not exhaustive in-game verification of every civilization**.

Three same-height candidates per intact asset received one independent cross-group blind visual review: 25 profiles were retained and 11 changed. This was a preference review, not multi-reviewer consensus.

### Verification

- All native lifecycle frames decoded; outline/mask checks passed.
- The 108 installed graphic files matched the final manifest individually.
- Final ZIP integrity and all 108 packaged asset hashes passed.
- Sampled in-game rendering covered seven architecture sets, including a 4v4 Extreme AI Arabia match at 22–23 minutes.
- Controlled damage/collapse/rubble tests covered Western, Andean, Mediterranean, Central Asian and East Asian examples.
- Matched original/mod gap fixtures covered Western and East Asian Castle houses. Passability was unchanged; reduced roof occlusion improved visibility.

No release blocker was found in the sampled coverage. Greek runtime testing was blocked by an unowned DLC; Greek and other untested Chronicles styles have native-file validation only.

See the [in-game gallery](HISTORICAL-GALLERY.md), [exact QA coverage](../manifests/v0.4-qa-summary.json), [asset hashes](../manifests/v0.4-allstyles.json) and [archive checks](../manifests/v0.4-package-check.json).

## Archived v0.4 installation and limits

Disable other house-graphics mods and older short-house versions, enable v0.4, and restart the game. Keep the previous package for rollback. QA restored the original mod-enabled flags; the test installation was left disabled.

- Graphics only: no DAT, gameplay, population, collision or pathfinding changes.
- Construction scaffolding remains original; fire can float at original attachment positions.
- Native color/shadow recompression is lossy.
- UHD, snow, repair, every player color, every animation frame and actual multiplayer remain unverified or not exhaustively tested.
- Gap comparisons use matching geometry/camera/zoom, but different capture times and original randomized variants. They illustrate visibility, not a new passable route.
