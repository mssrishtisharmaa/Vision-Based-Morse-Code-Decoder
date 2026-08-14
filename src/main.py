import cv2
import mediapipe as mp
import time

from blink_detector import calculate_face_ear
from morse_decoder import decode_morse
from hand_controller import HandToggleController


def main():

    # -----------------------------
    # MediaPipe initialization
    # -----------------------------

    mp_face = mp.solutions.face_mesh
    face_mesh = mp_face.FaceMesh(
        refine_landmarks=True,
        max_num_faces=1
    )

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        max_num_hands=1
    )

    # -----------------------------
    # Webcam
    # -----------------------------

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # -----------------------------
    # Detection configuration
    # -----------------------------

    BLINK_THRESHOLD = 0.19
    DOT_TIME = 0.25
    DASH_TIME = 0.65
    LETTER_GAP = 0.7
    WORD_GAP = 1.5

    # -----------------------------
    # State
    # -----------------------------

    current_morse = ""
    decoded_text = ""

    blink_start = None
    blink_active = False
    last_blink_end = time.time()

    hand_controller = HandToggleController()

    # -----------------------------
    # Main loop
    # -----------------------------

    while True:

        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read webcam frame.")
            break

        height, width = frame.shape[:2]

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        current_time = time.time()

        # -----------------------------
        # Hand detection
        # -----------------------------

        hand_results = hands.process(rgb)

        hand_present = (
            hand_results.multi_hand_landmarks
            is not None
        )

        detection_enabled = hand_controller.update(
            hand_present,
            current_time
        )

        # -----------------------------
        # Detection OFF
        # -----------------------------

        if not detection_enabled:

            cv2.putText(
                frame,
                "DETECTION OFF - SHOW HAND",
                (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

            cv2.imshow(
                "Vision-Based Morse Decoder",
                frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            continue

        # -----------------------------
        # Face detection
        # -----------------------------

        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:

            landmarks = results.multi_face_landmarks[
                0
            ].landmark

            ear = calculate_face_ear(
                landmarks,
                width,
                height
            )

            # -----------------------------
            # Blink detection
            # -----------------------------

            if ear < BLINK_THRESHOLD:

                if not blink_active:

                    blink_start = current_time
                    blink_active = True

            else:

                if blink_active:

                    blink_duration = (
                        current_time - blink_start
                    )

                    # Short blink = DOT
                    if blink_duration < DOT_TIME:

                        current_morse += "."

                    # Medium/long blink = DASH
                    elif blink_duration < DASH_TIME:

                        current_morse += "-"

                    else:

                        current_morse += "-"

                    blink_active = False
                    last_blink_end = current_time

        # -----------------------------
        # Letter detection
        # -----------------------------

        if (
            current_time - last_blink_end > LETTER_GAP
            and current_morse
        ):

            letter = decode_morse(
                current_morse
            )

            decoded_text += letter

            current_morse = ""

        # -----------------------------
        # Word detection
        # -----------------------------

        if (
            current_time - last_blink_end > WORD_GAP
            and decoded_text
        ):

            if not decoded_text.endswith(" "):

                decoded_text += " "

        # -----------------------------
        # Display information
        # -----------------------------

        cv2.putText(
            frame,
            "DETECTION ON - BLINK TO TYPE",
            (10, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"EAR: {ear:.3f}" if results.multi_face_landmarks
            else "EAR: --",
            (10, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Morse: {current_morse}",
            (10, 105),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Decoded: {decoded_text}",
            (10, 140),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        # -----------------------------
        # Show frame
        # -----------------------------

        cv2.imshow(
            "Vision-Based Morse Decoder",
            frame
        )

        # Press Q to exit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # -----------------------------
    # Cleanup
    # -----------------------------

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()