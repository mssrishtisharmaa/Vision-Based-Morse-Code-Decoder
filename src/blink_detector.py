import numpy as np


LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]


def eye_aspect_ratio(points):
    """
    Calculate Eye Aspect Ratio (EAR).

    EAR decreases when the eye closes.
    """
    A = np.linalg.norm(points[1] - points[5])
    B = np.linalg.norm(points[2] - points[4])
    C = np.linalg.norm(points[0] - points[3])

    return (A + B) / (2.0 * C)


def calculate_face_ear(landmarks, width, height):
    """
    Calculate average EAR for both eyes from MediaPipe landmarks.
    """

    left_points = np.array([
        (landmarks[i].x * width, landmarks[i].y * height)
        for i in LEFT_EYE
    ])

    right_points = np.array([
        (landmarks[i].x * width, landmarks[i].y * height)
        for i in RIGHT_EYE
    ])

    left_ear = eye_aspect_ratio(left_points)
    right_ear = eye_aspect_ratio(right_points)

    return (left_ear + right_ear) / 2.0