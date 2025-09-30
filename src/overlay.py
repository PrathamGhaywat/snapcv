"""Logic for compositing transparent overlays onto video frames."""

from __future__ import annotations

import cv2
import numpy as np

from face_detection import BoundingBox


def apply_overlay(
    frame: np.ndarray,
    filter_image: np.ndarray,
    face: BoundingBox,
    *,
    scale: float = 1.2,
    y_offset: float = 0.0,
) -> None:
    """Draw ``filter_image`` over ``frame`` anchored to ``face`` in-place."""

    if frame is None or filter_image is None:
        return

    x, y, w, h = face
    overlay_width = max(1, int(w * scale))
    overlay_height = max(1, int(h * scale))

    resized = cv2.resize(filter_image, (overlay_width, overlay_height), interpolation=cv2.INTER_AREA)

    # Center overlay horizontally and allow vertical adjustment.
    x_start = int(x - (overlay_width - w) / 2)
    y_start = int(y - (overlay_height - h) / 2 + y_offset * overlay_height)

    x_end = x_start + overlay_width
    y_end = y_start + overlay_height

    # Clip to frame boundaries and compute the corresponding slice on the overlay.
    frame_h, frame_w = frame.shape[:2]
    x_start_clipped = max(0, x_start)
    y_start_clipped = max(0, y_start)
    x_end_clipped = min(frame_w, x_end)
    y_end_clipped = min(frame_h, y_end)

    if x_start_clipped >= x_end_clipped or y_start_clipped >= y_end_clipped:
        return

    overlay_x_start = x_start_clipped - x_start
    overlay_y_start = y_start_clipped - y_start
    overlay_x_end = overlay_x_start + (x_end_clipped - x_start_clipped)
    overlay_y_end = overlay_y_start + (y_end_clipped - y_start_clipped)

    overlay_slice = resized[overlay_y_start:overlay_y_end, overlay_x_start:overlay_x_end]
    frame_slice = frame[y_start_clipped:y_end_clipped, x_start_clipped:x_end_clipped]

    if overlay_slice.ndim < 3:
        return

    if overlay_slice.shape[2] == 4:
        alpha = (overlay_slice[:, :, 3:] / 255.0).astype(np.float32)
        overlay_rgb = overlay_slice[:, :, :3]
    else:
        overlay_rgb = overlay_slice
        gray = cv2.cvtColor(overlay_rgb, cv2.COLOR_BGR2GRAY)
        alpha = (gray > 0).astype(np.float32)[..., None]

    if alpha.size == 0:
        return

    inv_alpha = 1.0 - alpha
    frame_slice[:] = (
        alpha * overlay_rgb.astype(np.float32) + inv_alpha * frame_slice.astype(np.float32)
    ).astype(frame_slice.dtype)
