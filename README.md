# hiiwave Short Houses

Private AoE2 DE graphics-mod project. Author: **hiiwave**.

## Current delivered trial
**v0.2-intact-222-110**: Dark / Western Feudal / Western Castle use source variant **2 / 2 / 2**, with **110 px** visible main-image height, using **Roof-Shift Hybrid**. Imperial shares the Castle asset. Each age's three static variation slots contain the same selected shape.

This is **not** the earlier v0.1 lifecycle package. v0.2 changes intact houses only. Its nine static frames passed decoder, height, outline and ZIP checks. It was **not game-tested before delivery**, but the owner subsequently reported successful real-play testing and accepted the trial. Old v0.1 had different shapes/proportions and recorded controlled lifecycle tests.

## Review documents
- [PRD: purpose, scope and acceptance](docs/PRD.md)
- [Technical specification and architecture](docs/TECHNICAL-SPEC.md)
- [Decisions and alternatives](docs/DECISIONS.md)
- [Versions and test evidence](docs/TEST-STATUS.md)
- [Build and installation](docs/BUILD.md)
- [Rights and repository boundaries](docs/RIGHTS.md)

## Important limits
- Graphics only. No DAT, gameplay, population, collision or pathfinding changes.
- Floating fire is an accepted known issue, not an absolute claim that every conceivable graphical solution is impossible.
- Trial destruction/rubble do not match the new shape yet. Disable the old Wavy mod rather than mix its lifecycle assets with this one.
- Shared default Dark Age graphics affect more civilizations than the Western set.
- UHD, snow, all colors, repair progression and actual multiplayer compatibility are unverified.

The repository holds authored source, specifications and hashes. Original game graphics and generated image/mod binaries are deliberately excluded. A lawful local game installation is required to rebuild. The portable rebuild reproduced all three delivered sprite hashes exactly; see [rebuild evidence](docs/REBUILD.md). ZIP metadata/text differ, so only sprite-byte equivalence is claimed.

