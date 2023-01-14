import cv2
import mediapipe as mp

# variables made for convenience
mp_drawing=mp.solutions.drawing_utils
mp_drawing_styles=mp.solutions.drawing_styles
mp_pose=mp.solutions.pose
cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence = 0.5,min_tracking_confidence = 0.5) as pose:
    # while webcam is running

    good_left=0
    good_right= 0

    while cap.isOpened():
        success, image = cap.read()
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        #drawing indication lines
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
        )


        # Use lm and lmPose as representative of the following methods.
        # Process the image.
        keypoints = pose.process(image)
        lm = keypoints.pose_landmarks
        lmPose  = mp_pose.PoseLandmark
        h,w = image.shape[:2]


        #flip image horizontally for mirrored view
        cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))

         #stores height of left shoulder
        l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)

        #stores height of right shoulder 
        r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)

        # wait for user to type in p 
        if cv2.waitKey(1) == ord('p'):
            print('HELLOOOOOOOOOOO')
            good_left = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h) 
            good_right = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)

        l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)
        r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)
        
        if(good_left == 0 and good_right == 0 ): 
            print("Press P to record your position, or q to quit!")
        elif(l_shldr_y > good_left+15 or r_shldr_y > good_right+15):
            print("BAD POSTURE")
        else:
            print("GOOD POSTURE!")
        

        #stops running webcam until 'q' is clicked 
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()        

def getFrame(capture):
    ret, frame = capture.read()
    
    ret, jpeg = cv2.imencode('.jpg', frame)