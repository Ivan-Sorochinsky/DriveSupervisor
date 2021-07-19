import threading

import cv2
import mediapipe as mp
import numpy as np
import pyautogui

from helper import bad_vodiva


def main_auto_util():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        semaphore = threading.Semaphore(1)
        event = threading.Event()
        while True:
            # сделать скриншот
            img = pyautogui.screenshot(region=(200, 200, 960, 540))
            # преобразовываем эти пиксели в правильный массив numpy для работы с OpenCV
            frame = np.array(img)
            # конвертировать цвета из BGR в RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                left_hand = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                right_hand = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                # если водитель убрал обе руки - запускаем поток с ругательствами робота
                if (left_hand[0] > 0.34 or left_hand[0] < 0.14) and (right_hand[0] > 0.34 or right_hand[0] < 0.14):
                    if not event.is_set():
                        t2 = threading.Thread(target=bad_vodiva, args=(1, semaphore, event))
                        t2.start()
            except:
                pass

            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                      )

            # draw line
            # line_s = [(100, 0), (100, 400)]
            # line_e = [(240, 0), (240, 400)]
            # cv2.line(image, line_s[0], line_s[1], (0, 0, 255), 2)
            # cv2.line(image, line_e[0], line_e[1], (0, 0, 255), 2)

            cv2.imshow('Video stream 1', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break


t1 = threading.Thread(target=main_auto_util(), daemon=True)
t1.start()
