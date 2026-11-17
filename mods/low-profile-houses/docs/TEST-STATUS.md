# Release and build evidence

## Current version: 2611.1-beta.5

**0.6x** is the height label (120 px upper bound), not the release version. The publication-description formatting revision uses `2611.1-beta.5`; that suffix is not evidence of a geometry change.

The owner-selected [25-minute before/after](GAMEPLAY-GALLERY.md) is current in-game visual evidence. It shows original versus shortened houses, not exhaustive validation of all assets or lifecycle states.

The repository still contains historical v0.2/v0.4 code, manifests and QA records. The [120 px build snapshot and payload verification](../manifests/2611.1-beta.5-verification.md) now record 108 assets whose hashes match the local publishing payload and subscribed public mod. The snapshot’s native-check results are build-time evidence, not a new full runtime test. Complete current reproducible source and comprehensive lifecycle runtime QA remain separate gaps. Do not relabel old results as current validation.

## Historical v0.4 package (110 px)

108 SLDs: 36 intact at 110 px, 36 destruction, 36 rubble; 17 standard-house architecture sets. Native lifecycle decoding and mask checks passed. All 108 installed files matched the final manifest, and final ZIP integrity/asset hashes passed.

Runtime sampling covered seven architecture sets through 4v4 Arabia and controlled fixtures. Western, Andean, Mediterranean, Central Asian and East Asian lifecycle examples passed sampled damage/collapse/rubble checks. Western and East Asian matched gap tests preserved open/closed passage while reducing visual occlusion. No release blocker was observed in these samples.

Greek runtime testing was blocked by an unowned DLC. Other untested Chronicles styles have native checks only. UHD, snow, repair, every player color, exhaustive animation frames and actual multiplayer are not fully verified. Scaffolding and fire attachment positions remain original.

Historical v0.4 evidence: [QA summary](../manifests/v0.4-qa-summary.json), [asset manifest](../manifests/v0.4-allstyles.json), [archive verification](../manifests/v0.4-package-check.json), [historical gameplay evidence](HISTORICAL-GALLERY.md). Earlier sections below are historical records, not the current release status.

## v0.2-intact-222-110 (historical delivered trial)
Selected 2/2/2; 110 px; Roof-Shift Hybrid. Author hiiwave.

Passed before delivery:
- Three native files decoded, three frames each.
- Main alpha height 110 for all nine frames.
- Three slots identical per age.
- Outline mask matches main occupancy.
- File extent and ZIP integrity checked.
- Packaged asset hashes matched the validation manifest.
- No DAT / AI / XS file in package.

**Not tested before delivery:** exact new package in game. No new lifecycle validation, all-color sweep, repair progression, snow, UHD or multiplayer session.

Reference asset hashes are in ../manifests/v0.2-intact-222-110.json. Rebuild verification must be recorded separately; do not inherit v0.1 runtime evidence.

## v0.1 lifecycle (earlier delivered ZIP)
Different source variants and deformation parameters. Included 9 SLDs for intact, destruction and rubble across Dark, Western Feudal, Western Castle/Imperial.

Historical controlled QA records report:
- Each age: construction completion, population increase and native damaged appearance.
- Feudal, Castle, Imperial: Onager destruction / collapse / final rubble.
- Dark: recorded damaged shading and fire at 299/550 HP, Onager destruction and direct deletion.
- Fire misalignment remained. Scaffolding unchanged.

These are recorded historical tests, not new independent reruns by the documentation pass.

## Historical v0.2 follow-up checklist
1. Install this trial alone; restart and inspect all ages.
2. Verify blue/red and additional player colors.
3. Same camera/zoom, flat ground and slope, single house and adjacent rows.
4. Walk a villager through a known gap: distinguish geometric passage from visual visibility.
5. After lifecycle adaptation, inspect construction -> standing, HP steps, repair, initial collapse and final rubble without shape/height pop.
6. Snow/UHD and actual multiplayer remain separately marked unverified until run.

## Release checklist
Record source game version and hashes, selected source frames, exact parameters, generated hashes, static checks, actual test coverage, known limits and rollback instructions. Never call successful decoding a successful in-game test.


## Owner acceptance after delivery
The owner subsequently reported that actual play looked fine and authorized completing remaining Western lifecycle art, then expanding to all civilizations. This is owner-reported acceptance of the intact trial, not an independently observed test of damage/destruction or universal compatibility. The earlier pre-delivery status above remains historically accurate.

## All-style candidate selection: authorized QA plan

Status: candidate selection and sampled runtime QA completed for v0.4. The procedure below records the agreed plan. Each of 36 intact assets had three candidates and one independent cross-group reviewer; 25 profiles were retained and 11 changed. This was not multi-reviewer consensus, and runtime coverage was sampled rather than universal.

For each architecture style, generate multiple transformation-parameter candidates at the same target height. Keep source variant, pixel scale and framing consistent within each comparison. Present candidates with neutral IDs to an independent visual reviewer, hiding parameter choices and the proposed favorite. Judge roof/wall proportions, recognizable doors and windows, silhouette, ground contact and likely gap readability. Use practical visual judgment rather than a parameter score alone.

Apply objective guardrails before selection: target height after native encoding/readback; positive, nonfolding roof/wall mapping with usable wall bands; fixed ground/hotspot placement; aligned masks/player color; valid native files. Reject technical failures even when a small preview looks attractive. A visually preferred candidate must still pass lifecycle and in-game checks before release. Record candidate parameters, reviewer recommendation, final choice and actual test results separately.
