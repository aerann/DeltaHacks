import cv2
import mediapipe as mp
mp_drawing=mp.solutions.drawing_utils
mp_drawing_styles=mp.solutions.drawing_styles
mp_pose=mp.solutions.pose

cap=cv2.VideoCapture(0)
with mp_pose.Pose(min_detection_confidemce=0.5,min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        success, image=cap.read()
        image.flags.writeable = False
        image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        results=pose.process(image)

        #drawing indication lines