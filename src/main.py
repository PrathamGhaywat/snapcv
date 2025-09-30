"""Run a Snapchat-style face overlay using OpenCV."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

import cv2

from face_detection import FaceDetector
from overlay import apply_overlay


def _find_filter_image(candidate: Path | None, filters_dir: Path) -> Path:
    if candidate:
        path = candidate.expanduser()
        if path.is_dir():
            return _first_image_in(path)
        if not path.exists():
            raise FileNotFoundError(f"Filter image {path} was not found")
        return path

    return _first_image_in(filters_dir)


def _first_image_in(directory: Path) -> Path:
    if not directory.exists():
        raise FileNotFoundError(f"Filters directory {directory} is missing")

    images: List[Path] = sorted(
        p for p in directory.iterdir() if p.suffix.lower() in {".png", ".jpg", ".jpeg"}
    )
    if not images:
        raise FileNotFoundError(
            f"No PNG or JPG filters found in {directory}. Please add a filter image and try again."
        )
    return images[0]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--filter",
        type=Path,
        default=None,
        help="Path to the filter image (PNG with transparency preferred). Defaults to the first image in the filters folder.",
    )
    parser.add_argument(
        "--camera",
        type=int,
        default=0,
        help="Camera index to open (default: 0).",
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=1.35,
        help="Scale factor applied to the detected face before sizing the overlay (default: 1.35).",
    )
    parser.add_argument(
        "--y-offset",
        type=float,
        default=-0.15,
        help="Vertical offset multiplier applied to the overlay height (default: -0.15).",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    project_root = Path(__file__).resolve().parent.parent
    filters_dir = project_root / "filters"

    filter_path = _find_filter_image(args.filter, filters_dir)

    overlay_image = cv2.imread(str(filter_path), cv2.IMREAD_UNCHANGED)
    if overlay_image is None:
        raise ValueError(f"Unable to load image at {filter_path}")

    detector = FaceDetector()

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        raise RuntimeError(
            f"Unable to open camera index {args.camera}. Ensure a webcam is connected and accessible."
        )

    window_title = "snapcv - Face Filter"

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            faces = detector.detect(frame)
            for bbox in faces:
                apply_overlay(frame, overlay_image, bbox, scale=args.scale, y_offset=args.y_offset)

            cv2.imshow(window_title, frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
	main()
