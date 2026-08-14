import cv2
import mediapipe as mp
import numpy as np
import time
import tkinter as tk
import threading



MORSE_MAP = {
    ".-": "A", "-...": "B", "-.-.": "C", "-..": "D",
    ".": "E", "..-.": "F", "--.": "G", "....": "H",
    "..": "I", ".---": "J", "-.-": "K", ".-..": "L",
    "--": "M", "-.": "N", "---": "O", ".--.": "P",
    "--.-": "Q", ".-.": "R", "...": "S", "-": "T",
    "..-": "U", "...-": "V", ".--": "W", "-..-": "X",
    "-.--": "Y", "--..": "Z"
}


decoded_text = ""
current_morse = ""

detection_enabled = True
hand_last_state = False
hand_toggle_cooldown = 0


root = tk.Tk()
root.title("Blink Morse Code Decoder")
root.geometry("550x350")
root.configure(bg="pink")

title = tk.Label(root, text="Blink → Morse Code Decoder", font=("Arial", 22, "bold"), bg="white")
title.pack(pady=10)

display = tk.Label(root, text="", font=("Arial", 18), bg="white")
display.pack(pady=20)

info = tk.Label(root,
                text="Short Blink = Dot (.)\nLong Blink = Dash (-)\nShow Hand = Toggle ON/OFF",
                font=("Arial", 14), bg="white")
info.pack(pady=10)


def update_gui():
    status = "ON" if detection_enabled else "OFF"
    display.config(text=f"Detection: {status}\nDecoded: {decoded_text}\nCurrent: {current_morse}")
    root.update_idletasks()



LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def eye_aspect_ratio(pts):
    A = np.linalg.norm(pts[1] - pts[5])
    B = np.linalg.norm(pts[2] - pts[4])
    C = np.linalg.norm(pts[0] - pts[3])
    return (A + B) / (2.0 * C)


def webcam_loop():
    global decoded_text, current_morse
    global detection_enabled, hand_last_state, hand_toggle_cooldown

    mp_face = mp.solutions.face_mesh
    face_mesh = mp_face.FaceMesh(refine_landmarks=True, max_num_faces=1)

   
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1)

    cap = cv2.VideoCapture(0)

    BLINK_THRESHOLD = 0.19  
    DOT_TIME = 0.25         
    DASH_TIME = 0.65        
    LETTER_GAP = 0.7
    WORD_GAP = 1.5

    blink_start = None
    blink_active = False
    last_blink_end = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        h, w = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        hand_results = hands.process(rgb)
        hand_present = hand_results.multi_hand_landmarks is not None

        current_time = time.time()


        if hand_present and not hand_last_state:
            if current_time - hand_toggle_cooldown > 1.0:
                detection_enabled = not detection_enabled
                hand_toggle_cooldown = current_time

        hand_last_state = hand_present


        if not detection_enabled:
            cv2.putText(frame, "DETECTION OFF - SHOW HAND TO ENABLE",
                        (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (0, 0, 255), 2)
            update_gui()
            cv2.imshow("Blink Detector", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue


        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:
            lm = results.multi_face_landmarks[0].landmark

            left_pts = np.array([(lm[i].x * w, lm[i].y * h) for i in LEFT_EYE])
            right_pts = np.array([(lm[i].x * w, lm[i].y * h) for i in RIGHT_EYE])

            leftEAR = eye_aspect_ratio(left_pts)
            rightEAR = eye_aspect_ratio(right_pts)
            ear = (leftEAR + rightEAR) / 2

            if ear < BLINK_THRESHOLD:
                if not blink_active:
                    blink_start = time.time()
                    blink_active = True

            else:
                if blink_active:
                    blink_duration = time.time() - blink_start

                    if blink_duration < DOT_TIME:
                        current_morse += "."
                    elif blink_duration < DASH_TIME:
                        current_morse += "-"
                    else:
                        current_morse += "-"

                    blink_active = False
                    last_blink_end = time.time()
                    update_gui()

        if time.time() - last_blink_end > LETTER_GAP and current_morse != "":
            letter = MORSE_MAP.get(current_morse, "?")
            decoded_text += letter
            current_morse = ""
            update_gui()

        if time.time() - last_blink_end > WORD_GAP:
            if not decoded_text.endswith(" "):
                decoded_text += " "
                update_gui()

        cv2.putText(frame, "DETECTION ON - BLINK TO TYPE",
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0, 255, 0), 2)

        cv2.imshow("Blink Detector", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


threading.Thread(target=webcam_loop, daemon=True).start()
root.mainloop()
