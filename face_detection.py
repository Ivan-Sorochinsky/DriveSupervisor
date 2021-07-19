import threading
import time

from scipy.spatial import distance as dist
import cv2
import mediapipe as mp
import numpy as np
import pyautogui


# EAR глаз
from helper import bad_vodiva

EAR_ALERT_VALUE = 0.4  # значение при котором происходит срабатывание системы безопасности
FPS = 24  # количество кадров за 2 секунды


def eye_aspect_ratio(eye):
    a = dist.euclidean(eye[1], eye[5])
    b = dist.euclidean(eye[2], eye[4])

    c = dist.euclidean(eye[0], eye[3])

    ear = (a + b) / (2.0 * c)
    return ear


# MAR рта
def mouth_aspect_ratio(mouth):
    a = dist.euclidean(mouth[1], mouth[7])
    b = dist.euclidean(mouth[2], mouth[6])
    c = dist.euclidean(mouth[3], mouth[5])

    d = dist.euclidean(mouth[0], mouth[4])

    mar = (a + b + c) / (2.0 * d)
    return mar


def main_block():
    mp_drawing = mp.solutions.drawing_utils  # Drawing helpers
    mp_holistic = mp.solutions.holistic  # Mediapipe Solutions

    # инициализируем holistic model
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        counter, alert_counter = 0, 0
        lst_ear_r, lst_ear_l, lst_counter, lst_ear_mouth = [], [], [], []
        semaphore = threading.Semaphore(1)
        event = threading.Event()
        while True:
            # сделать скриншот
            img = pyautogui.screenshot(region=(500, 500, 700, 400))
            # преобразовываем эти пиксели в правильный массив numpy для работы с OpenCV
            frame = np.array(img)
            # конвертировать цвета из BGR в RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = holistic.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Draw face landmarks
            mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(80, 110, 10), thickness=1, circle_radius=1),
                                      mp_drawing.DrawingSpec(color=(80, 256, 121), thickness=1, circle_radius=1)
                                      )
            # Extract landmarks
            try:
                landmarks = results.face_landmarks.landmark
                # контрольные точки для правого глаза
                right_eye_33 = (landmarks[33].x, landmarks[33].y)
                right_eye_159 = (landmarks[159].x, landmarks[159].y)
                right_eye_158 = (landmarks[158].x, landmarks[158].y)
                right_eye_133 = (landmarks[133].x, landmarks[133].y)
                right_eye_153 = (landmarks[153].x, landmarks[153].y)
                right_eye_145 = (landmarks[145].x, landmarks[145].y)

                # контрольные точки для левого глаза
                left_eye_362 = (landmarks[362].x, landmarks[362].y)
                left_eye_385 = (landmarks[385].x, landmarks[385].y)
                left_eye_386 = (landmarks[386].x, landmarks[386].y)
                left_eye_263 = (landmarks[263].x, landmarks[263].y)
                left_eye_374 = (landmarks[374].x, landmarks[374].y)
                left_eye_380 = (landmarks[380].x, landmarks[380].y)

                right_eye = [right_eye_33, right_eye_159, right_eye_158, right_eye_133, right_eye_153, right_eye_145]
                left_eye = [left_eye_362, left_eye_385, left_eye_386, left_eye_263, left_eye_374, left_eye_380]

                ear_right_eye = eye_aspect_ratio(right_eye)
                ear_left_eye = eye_aspect_ratio(left_eye)

                lst_ear_r.append(str(ear_right_eye))
                lst_ear_l.append(str(ear_left_eye))
                lst_counter.append(str(counter))

                f = open('r_eye_data.txt', 'w+')
                f.write(', '.join(lst_ear_r))
                f.close()

                f = open('l_eye_data.txt', 'w+')
                f.write(', '.join(lst_ear_l))
                f.close()

                f = open('counter.txt', 'w+')
                f.write(', '.join(lst_counter))
                f.close()

                if len(lst_ear_r) > 120:
                    lst_ear_r.remove(lst_ear_r[0])
                    lst_counter.remove(lst_counter[0])
                if len(lst_ear_l) > 120:
                    lst_ear_l.remove(lst_ear_l[0])

                # если глаза закрыты больше n-секунд, запускаем робота (тестовый режим n=2)
                # определим среднее значение
                ear = (ear_right_eye + ear_left_eye) / 2.0

                if ear < EAR_ALERT_VALUE:
                    alert_counter += 1
                    if alert_counter > FPS:
                        if not event.is_set():
                            t2 = threading.Thread(target=bad_vodiva, args=(0, semaphore, event))
                            t2.start()
                else:
                    alert_counter = 0

                # TODO: код для анализа состояния рта = D
                # контрольные точки
                mouth_78 = (landmarks[78].x, landmarks[78].y)
                mouth_81 = (landmarks[81].x, landmarks[81].y)
                mouth_13 = (landmarks[13].x, landmarks[13].y)
                mouth_311 = (landmarks[311].x, landmarks[311].y)
                mouth_308 = (landmarks[308].x, landmarks[308].y)
                mouth_402 = (landmarks[402].x, landmarks[402].y)
                mouth_14 = (landmarks[14].x, landmarks[14].y)
                mouth_178 = (landmarks[178].x, landmarks[178].y)

                mouth = [mouth_78, mouth_81, mouth_13, mouth_311, mouth_308, mouth_402, mouth_14, mouth_178]

                mar_mouth = mouth_aspect_ratio(mouth)

                lst_ear_mouth.append(str(mar_mouth))

                f = open('mouth_data.txt', 'w+')
                f.write(', '.join(lst_ear_mouth))
                f.close()

                if len(lst_ear_mouth) > 120:
                    lst_ear_mouth.remove(lst_ear_mouth[0])

                counter += 1

            except Exception:
                pass

            cv2.imshow('Video stream 2', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

t1 = threading.Thread(target=main_block(), daemon=True)
t1.start()
