import time
import cv2
import mediapipe as mp
from screeninfo import get_monitors
import math
import subprocess
import random
import Config as cfg
import os

# -------------------- Get monitor sizes --------------------
screen_width = 0
for m in get_monitors():
    print(str(m))
    if m.is_primary:
        screen_width = m.width

print(f"Screen width is {screen_width}")

# -------------------- Load background image --------------------

jsy_video_files = [f for f in os.listdir(cfg.JSY_VIDOE_PATH) if f.endswith('.mp4')]
jsy_video_files.sort()


bg_image = cv2.imread("bg2.jpg")
cv2.namedWindow("bg_image", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("bg_image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.imshow("bg_image", bg_image)
# cv2.waitKey(500) # wait for 5 second

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# cam = cv2.VideoCapture("TzuChi.mp4")

# VIDEO FEED
cap = cv2.VideoCapture(cfg.CAMERA_ID)


def play_jsy_vidoe_randomly():
    # Play one of the JSY videos randomly
    filenum = random.randint(0, len(jsy_video_files) - 1)
    # videofile = f"jsy{filenum}.mp4"
    videofile = cfg.JSY_VIDOE_PATH.replace('/', '\\') + '\\' + jsy_video_files[filenum]
    comm = [cfg.VLC_EXE, videofile, '--fullscreen']
    subprocess.run(comm, shell=True)


# Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

    seq = ""  # Pose sequence. S: stand, P: Palm folded, B: bow down
    palm_distance_percent = 100  # default to be 100 of  the shoulder width

    while cap.isOpened():
        ret, frame = cap.read()

        # Recolour image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Detect pose
        results = pose.process(image)

        # Recolour back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extract Landmarks
        try:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x,
                    landmarks[mp_pose.PoseLandmark.NOSE.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            leftShoulderY = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            hipY = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

            FONT = cv2.FONT_HERSHEY_SIMPLEX
            WHITE = (255, 255, 255)

            # recognize and show shoulder position
            leftShoulderX = int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x * cfg.CAM_WIDTH)
            leftShoulderY = int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y * cfg.CAM_HEIGHT)
            leftShoulderVisibility = int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].visibility * 100) # 0 to 100%
            if not cfg.IS_PRODUCTION:
                cv2.putText(image, f" {leftShoulderX},{leftShoulderY}:{leftShoulderVisibility}%", (leftShoulderX, leftShoulderY), FONT, 0.5, WHITE, 1, cv2.LINE_AA)

            rightShoulderX = int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * cfg.CAM_WIDTH)
            rightShoulderY = int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * cfg.CAM_HEIGHT)
            rightShoulderVisibility = int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].visibility * 100) # 0 to 100%
            if not cfg.IS_PRODUCTION:
                cv2.putText(image, f" {rightShoulderX},{rightShoulderY}:{rightShoulderVisibility}%", (rightShoulderX, rightShoulderY),  FONT, 0.5, WHITE, 1, cv2.LINE_AA)

            shoulder_width = abs(rightShoulderX - leftShoulderX)

            # recognize and show nose position
            noseX = int(landmarks[mp_pose.PoseLandmark.NOSE].x * cfg.CAM_WIDTH)
            noseY = int(landmarks[mp_pose.PoseLandmark.NOSE].y * cfg.CAM_HEIGHT)
            noseVisibility = int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].visibility * 100) # 0 to 100%
            if not cfg.IS_PRODUCTION:
                cv2.putText(image, f" {noseX},{noseY}:{noseVisibility}%", (noseX, noseY), FONT, 0.5, WHITE, 1, cv2.LINE_AA)

            # recognize and show wrist position
            leftWristVisibility = int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST].visibility * 100) # 0 to 100%
            rightWristVisibility = int(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].visibility * 100) # 0 to 100%
            if leftWristVisibility > 10 and rightWristVisibility > 10:
                leftWristX = int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x * cfg.CAM_WIDTH)
                leftWristY = int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y * cfg.CAM_HEIGHT)
                if not cfg.IS_PRODUCTION:
                    cv2.putText(image, f" {leftWristX},{leftWristY}:{leftWristVisibility}%", (leftWristX, leftWristY), FONT, 0.5, WHITE, 1, cv2.LINE_AA)

                rightWristX = int(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x * cfg.CAM_WIDTH)
                rightWristY = int(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y * cfg.CAM_HEIGHT)
                if not cfg.IS_PRODUCTION:
                    cv2.putText(image, f" {rightWristX},{rightWristY}:{rightWristVisibility}%", (rightWristX, rightWristY),  FONT, 0.5, WHITE, 1, cv2.LINE_AA)

                palm_distance = math.sqrt((rightWristX - leftWristX)**2 + (rightWristY - leftWristY)**2)
                palm_distance_percent = int(palm_distance / shoulder_width * 100)

                if palm_distance_percent < 40:
                    if seq == "S":
                        seq += "P"

                if not cfg.IS_PRODUCTION:
                    cv2.putText(image, f"Shoulder width: {shoulder_width},Palm distance: {int(palm_distance)}", (10, 40), FONT, 0.5, WHITE, 1, cv2.LINE_AA)
                    cv2.putText(image, f"Palm distance: {palm_distance_percent}% of shoulder width.", (10, 60), FONT, 0.5, WHITE, 1, cv2.LINE_AA)

            # recognize and show hip position
            leftHipVisibility = int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].visibility * 100) # 0 to 100%
            rightHipVisibility = int(landmarks[mp_pose.PoseLandmark.RIGHT_HIP].visibility * 100)  # 0 to 100%

            if leftHipVisibility > 10 and leftHipVisibility > 10:
                leftHipX = int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].x * cfg.CAM_WIDTH)
                leftHipY = int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].y * cfg.CAM_HEIGHT)
                # cv2.putText(image, f" {leftHipX},{leftHipY}", (leftHipX, leftHipY), FONT, 0.5, WHITE, 1, cv2.LINE_AA)
                if not cfg.IS_PRODUCTION:
                    cv2.putText(image, f"LHIP: {leftHipX},{leftHipY}:{leftHipVisibility}%", (leftHipX, leftHipY), FONT, 0.5, WHITE, 1, cv2.LINE_AA)

                rightHipX = int(landmarks[mp_pose.PoseLandmark.RIGHT_HIP].x * cfg.CAM_WIDTH)
                rightHipY = int(landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y * cfg.CAM_HEIGHT)
                if not cfg.IS_PRODUCTION:
                    cv2.putText(image, f" {rightHipX},{rightHipY}:{rightHipVisibility}%", (rightHipX, rightHipY),  FONT, 0.5, WHITE, 1, cv2.LINE_AA)

            if noseVisibility > 50:
                if leftWristVisibility > 50 and rightWristVisibility > 50: # hands can be seen
                    if leftHipVisibility > 50 and rightHipVisibility > 50:
                        if palm_distance_percent > 40: # standing, palm not folded
                            if seq =="":
                                seq = "S"
                            elif seq == "SP": # has put down the palm
                                seq = "S"
                        if palm_distance_percent < 40: # standing, palm folded
                            if seq =="S":
                                seq += "P"
                        if noseY > leftShoulderY: # bow down
                            if seq == "SP":
                                seq += "B"
                    else: # hip not visible
                        seq = ""
                else: # hands cannot be seen
                    seq = ""
            else:  # person no longer detected since nose is not visible
                seq = ""

            if seq == "SPB":
                time.sleep(0.5)

                play_jsy_vidoe_randomly()

                seq = "" # reset pose sequence
                cv2.destroyWindow("bg_image")
                cv2.destroyWindow("pose_image")

                # show bg image again
                cv2.namedWindow("bg_image", cv2.WINDOW_NORMAL)
                cv2.setWindowProperty("bg_image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.imshow("bg_image", bg_image)

        except:
            pass

        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(255, 12, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                  )

        # ---------- DISPLAY POSE SEQUENCE ----------
        cv2.putText(image, f"Detected (S: Stand, P: Palm folded, B=Bowed): {seq}", (10, 20), FONT, 0.5, WHITE, 1, cv2.LINE_AA)

        # ---------- DISPLAY CURRENT VIDEO FRAME WITH SKELETON ----------
        if cfg.IS_PRODUCTION:
            imS = cv2.resize(image, (320, 240)) # production
        else:
            imS = cv2.resize(image, (960, 720))  # dev


        cv2.namedWindow("pose_image")  # Create a named window
        if cfg.IS_PRODUCTION:
            cv2.moveWindow("pose_image", screen_width - 320, -40)  # Move it to (x,y)  # Production

        cv2.imshow("pose_image", imS)

        # ---------- INTERRUPT KEY STROKE ----------
        key_entered = cv2.waitKey(10)
        if key_entered & 0xFF == ord('q'):
            break

        # Press "j" key to immediately play a JSY video, without bowing.
        if key_entered & 0xFF == ord('j'):
            play_jsy_vidoe_randomly()

            seq = ""  # reset pose sequence
            cv2.destroyWindow("bg_image")
            cv2.destroyWindow("pose_image")

            # show bg image again
            cv2.namedWindow("bg_image", cv2.WINDOW_NORMAL)
            cv2.setWindowProperty("bg_image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow("bg_image", bg_image)

# CLEAN UP RESOURCES
cap.release()
cv2.destroyWindow("pose_image")
cv2.destroyWindow("bg_image")
