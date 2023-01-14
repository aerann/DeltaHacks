import cv2
import mediapipe as mp

# variables made for convenience
mp_drawing=mp.solutions.drawing_utils
mp_drawing_styles=mp.solutions.drawing_styles
mp_pose=mp.solutions.pose

cap=cv2.VideoCapture(0)
with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:
    # while webcam is running
    while cap.isOpened():
        success, image=cap.read()
        image.flags.writeable = False
        # converting the color settings from BGR to RGB (webcam is using BGR but we want to view in RGB)
        image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        results=pose.process(image)

        #drawing indication lines
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
        )

        # flip image horizontally and display video
        # note imshow() is the method displaying the footage
            # parameters are ('Window Name', image)
        cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))

        # stops program when any key is pressed BUT DOESN"T WORK
        if cv2.waitKey(5) & 0xFF == 27:
            break

    # end with cap.release() to release webcam usage
    cap.release()