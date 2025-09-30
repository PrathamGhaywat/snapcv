# snapcv

OpenCV-powered face filters resembling Snapchat overlays.

## Setup

1. Create and activate a virtual environment (optional but recommended).
2. Install dependencies:

```powershell
python -m pip install -r src/requirements.txt
```

3. Add at least one PNG (with transparency) filter image to the `filters/` directory. JPG files are also supported, but transparency allows for more realistic compositing.

## Usage

Run the main script to start the webcam filter:

```powershell
python src/main.py
```

### Options

- `--filter PATH` – Path to a specific filter image. Defaults to the first image found in `filters/`.
- `--camera INDEX` – Webcam index (default `0`).
- `--scale VALUE` – Scales the overlay relative to the detected face width (default `1.35`).
- `--y-offset VALUE` – Vertical offset multiplier for fine-tuning placement (default `-0.15`).

Press `q` to quit the application window.

## Troubleshooting

- If you see `Unable to open camera`, verify another application isn't using the webcam.
- For filters without an alpha channel, the script treats non-black pixels as the visible region.
- If the overlay is misaligned, experiment with `--scale` and `--y-offset`.
