# Versions and evidence

## v0.2-intact-222-110 (current delivered trial)
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

## Required next game checks
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

Status: in progress; this section specifies the agreed procedure, not a claim that all styles have passed.

For each architecture style, generate multiple transformation-parameter candidates at the same target height. Keep source variant, pixel scale and framing consistent within each comparison. Present candidates with neutral IDs to an independent visual reviewer, hiding parameter choices and the proposed favorite. Judge roof/wall proportions, recognizable doors and windows, silhouette, ground contact and likely gap readability. Use practical visual judgment rather than a parameter score alone.

Apply objective guardrails before selection: target height after native encoding/readback; positive, nonfolding roof/wall mapping with usable wall bands; fixed ground/hotspot placement; aligned masks/player color; valid native files. Reject technical failures even when a small preview looks attractive. A visually preferred candidate must still pass lifecycle and in-game checks before release. Record candidate parameters, reviewer recommendation, final choice and actual test results separately.
