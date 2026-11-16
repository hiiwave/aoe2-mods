# Build and install

## Repository boundary
Only authored source and documentation are stored here. Supply the three original SLD files from a lawful local AoE2 DE installation. Do not commit them.

## Build
Python 3 with NumPy and Pillow is required. Use an isolated virtual environment.

```sh
python -m venv .venv
# Activate the environment using the command appropriate to your OS.
python -m pip install -r requirements.txt
python src/build_trial.py --graphics-dir "/path/to/AoE2DE/resources/_common/drs/graphics" --output-dir build
```

The command is intended to write only beneath the output directory. It does not install or enable a mod, alter originals, run the game, or regenerate collapse animation. It validates the source format, selected-frame outputs and reference hashes. Inputs with different game hashes may require a fresh review.

The portable wrapper is new; see docs/REBUILD-RESULT.json for its actual local verification status. Dependency versions used for the local check are recorded there rather than claiming every version is supported.

## Install trial
1. Close AoE2 DE.
2. Copy the generated mod folder (not a wrapper containing it) into the active player profile's mods/local.
3. Enable this trial; disable older Wavy / other house graphics mods.
4. Restart the game to clear cached graphics.
5. To revert, disable the trial and re-enable the prior mod, then restart.

Use Mods �� Open Directory to locate the active profile. Do not copy a development machine's profile identifier.

## Future lifecycle
Regenerate three destruction and three rubble assets using the chosen source variant and matched transform. Reuse the existing codec rather than drawing hundreds of frames manually. Inspect masks/color and sample animation continuity; then run controlled live tests. Previous estimate of 45�V90 minutes was a rough engineering estimate, not a guarantee or authorization to skip QA.

