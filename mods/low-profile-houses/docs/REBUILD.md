# Rebuild verification

> **Historical v0.2 / 110 px only.** These instructions and results do not rebuild or verify the current 0.6x Beta (120 px upper bound).

2026-11-16: the portable wrapper was executed on Windows with Python 3.11.5, NumPy 1.24.3 and Pillow 9.4.0 against the local original game graphics.

All three generated SLD SHA256 values exactly match the previously delivered v0.2 trial. All nine decoded frames measure 110 px, outline checks pass, and three static variation slots match per age. This establishes sprite-byte reproducibility for these source hashes, not universal compatibility or runtime rendering.

The new wrapper ZIP has revised README/info text and ZIP metadata; its overall ZIP bytes are not expected to match the earlier delivered ZIP. The graphics bytes do match. No installation or game test was performed by this rebuild.
