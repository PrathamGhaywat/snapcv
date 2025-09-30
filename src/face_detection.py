"""Utilities for detecting faces in a video frame."""

from __future__ import annotations

from typing import List, Tuple, cast

import cv2
from cv2 import data as cv2_data


BoundingBox = Tuple[int, int, int, int]


class FaceDetector:
    """Wraps OpenCV's Haar cascade face detector."""

    def __init__(
        self,
        cascade_path: str | None = None,
        scale_factor: float = 1.1,
        min_neighbors: int = 5,
        min_size: Tuple[int, int] = (60, 60),
    ) -> None:
        if cascade_path is None:
            cascade_path = cv2_data.haarcascades + "haarcascade_frontalface_default.xml"

        self._cascade = cv2.CascadeClassifier(str(cascade_path))
        if self._cascade.empty():
            raise ValueError(f"Failed to load face cascade from {cascade_path!r}")

        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        self.min_size = min_size

    def detect(self, frame) -> List[BoundingBox]:
        """Detect faces in a BGR frame and return bounding boxes."""

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self._cascade.detectMultiScale(
            gray,
            scaleFactor=self.scale_factor,
            minNeighbors=self.min_neighbors,
            minSize=self.min_size,
        )
        return [cast(BoundingBox, tuple(int(v) for v in face)) for face in faces]


def _demo() -> None:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Unable to open default camera (index 0)")

    detector = FaceDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        for (x, y, w, h) in detector.detect(frame):
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("snapcv - Face Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    _demo()
