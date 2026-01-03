import cv2
import mediapipe as mp
import math
import numpy as np
import time

cloak_active = False
cloak_start_time = 0
CLOAK_DURATION = 10


def calculate_angle(a, b, c):
    ba = (a.x - b.x, a.y - b.y)
    bc = (c.x - b.x, c.y - b.y)

    dot = ba[0]*bc[0] + ba[1]*bc[1]
    mag_ba = math.hypot(ba[0], ba[1])
    mag_bc = math.hypot(bc[0], bc[1])

    angle = math.degrees(math.acos(dot / (mag_ba * mag_bc)))
    return angle


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)
mp_hands = mp.solutions.hands
hand = mp_hands.Hands()
draw = mp.solutions.drawing_utils
finger_names = ["index","middle","ring","pinky"]
tip_ids = [8, 12, 16, 20]
pip_ids = [6, 10, 14, 18]
background = cv2.imread('background.jpg')
force = False
while True:

    current_time = time.time()
    open_fingers = 0
    ret, frame = cap.read()

    if ret:

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_red1 = np.array([0, 120, 70])
        upper_red1 = np.array([8, 255, 255])

        lower_red2 = np.array([172, 120, 70])
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = mask1 + mask2
        frame1 = cv2.bitwise_and(background, background, mask=mask)
        inverted_mask = cv2.bitwise_not(mask)
        frame2 = cv2.bitwise_and(frame, frame, mask=inverted_mask)
        final_magic = frame1 + frame2
        cv2.putText(
            final_magic,
            f"CLOAK MODE ON!!",
            (100, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (102,0,255),
            2
        )

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hand.process(rgb_frame)


        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                lm = handLms.landmark
                thumb_angle = calculate_angle(lm[2], lm[3], lm[4])

                if thumb_angle > 165:
                    open_fingers = open_fingers + 1


                hand_label = results.multi_handedness[0].classification[0].label
                for name,pip,tip in zip(finger_names, pip_ids, tip_ids):
                    if lm[tip].y < lm[pip].y:

                        open_fingers = open_fingers + 1



                draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
        if open_fingers==0:
            cv2.putText(
                frame,
                f"no fingers are open",
                (50, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                2
            )
        elif open_fingers==1:
            cv2.putText(
                frame,
                f"1 finger is open",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                2
            )
        else:
            cv2.putText(
                frame,  # image
                f"{open_fingers} fingers are open",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                2
            )


        if open_fingers == 2 and not cloak_active:

            output = final_magic
            cloak_active = True
            cloak_start_time = time.time()





        if cloak_active:
            output = final_magic
            cv2.putText(
                final_magic,
                f"{int(10 - current_time + cloak_start_time)}",
                (550, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (51,0,102),
                4
            )
            if current_time - cloak_start_time > CLOAK_DURATION:

                cloak_active = False
                output = frame
            if open_fingers == 5:
                force = True
                force_time = time.time()
                cloak_active = False
                output = frame
            cv2.imshow('Video', output)
        else:

            if force:
                if current_time - force_time < 3:
                    cv2.putText(
                        frame,
                        f"Forced exit!",
                        (420, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2
                    )
                else:
                    force = False
            output = frame
            cv2.imshow('Video', output)
        if cv2.waitKey(1)== ord('q'):
            break



cv2.destroyAllWindows()