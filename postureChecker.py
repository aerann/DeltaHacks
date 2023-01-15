import cv2
import mediapipe as mp

# variables made for convenience
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
cap = cv2.VideoCapture(0)


pose = mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5)
# while webcam is running

good_left = 0
good_right = 0

#returns the percentage of how good your posture is 
def checkPosture(l_shldr_y, r_shldr_y):
    height = cap.get(4)  # float `height`
    range = height - good_left
    relative = l_shldr_y - good_left

    if(good_left == 0 and good_right == 0): 
        print("Press P to record your position, or q to quit!")
    elif(l_shldr_y > good_left + 15 or r_shldr_y > good_right + 15):
        percentage = 100- ((relative/range) * 100)
        if (percentage <= 0):
            percentage = 0
        print("BAD POSTURE, %", percentage)
    else:
        percentage = 100
        print("GOOD POSTURE!, %", percentage)
    return percentage


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
    lmPose = mp_pose.PoseLandmark
    h,w = image.shape[:2]


    #flip image horizontally for mirrored view
    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))

    # wait for user to type in p 
    if cv2.waitKey(1) == ord('p'):
        print('POSITION RECORDED!')
        good_left = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h) 
        good_right = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)

    l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)
    r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)

    checkPosture(l_shldr_y, r_shldr_y) 

    #stops running webcam until 'q' is clicked 
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()        

