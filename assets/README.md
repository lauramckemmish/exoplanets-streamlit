# Project visual assets

`assets/` is the single home for project visual assets. Code should refer to
these files through a nearby `ASSETS_DIR` path constant rather than using
scattered relative strings.

## Approved UNSW Sydney master logos

- `unsw-sydney-logo-landscape.png` — canonical landscape master, used in the
  sidebar.
- `unsw-sydney-logo-portrait.png` — canonical portrait master, used in the
  landing-page provenance area.

Both files are supplied master artwork and must not be cropped, recoloured,
recompressed, separated or otherwise modified.

## Current application assets

The NASA artwork, explanatory SVGs, detection-method PNGs and travel posters
in this directory are referenced by the application or its shared classroom
resources. Keep their existing descriptive filenames and credits in the
calling experience.

## Retained legacy assets

The following files have no current runtime reference:

- `direct-imaging.svg`
- `transit-detection.svg`
- `exoplanet-detection-methods.svg`
- `nasa-trappist-1e-travel-poster.jpg`

They are retained because repository history shows they supported earlier
classroom scaffolding. Do not remove them without an explicit content/asset
ownership decision.
