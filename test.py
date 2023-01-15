import cv2
import mediapipe as mp

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5)
        self.height = self.video.get(4)
        self.good_left = 0
        self.good_right = 0

    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        frame = self.video.read()
        jpeg = cv2.imdecode('.jpg', frame)

    def calculatePercentage(self, l_shldr_y, r_shldr_y,):
        range = self.height - self.good_left
        relative = l_shldr_y - self.good_left
        percentage = 0
        # if(self.good_left == 0 and self.good_right == 0): 
        #     print("Press P to record your position, or q to quit!")
        if(l_shldr_y > self.good_left + 15 or r_shldr_y > self.good_right + 15):
            percentage = 100- ((relative/range) * 100)
            if (percentage <= 0):
                percentage = 0
            # print("BAD POSTURE, %", percentage)
        else:
            percentage = 100
            # print("GOOD POSTURE!, %", percentage)
        return percentage

    def processPosture(self):
        success, image = self.video.read()
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image)

        #drawing indication lines
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        self.mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            self.mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
        )


        # Use lm and lmPose as representative of the following methods.
        # Process the image.
        keypoints = self.pose.process(image)
        lm = keypoints.pose_landmarks
        lmPose = self.mp_pose.PoseLandmark
        h,w = image.shape[:2]


        #flip image horizontally for mirrored view
        cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))

        # wait for user to type in p 
        if cv2.waitKey(1) == ord('p'):
            print('POSITION RECORDED!')
            self.good_left = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h) 
            self.good_right = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)

        l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)
        r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)

        return self.calculatePercentage(l_shldr_y, r_shldr_y)
    

    # variables made for convenience
    # mp_drawing = mp.solutions.drawing_utils
    # mp_drawing_styles = mp.solutions.drawing_styles
    # mp_pose = mp.solutions.pose
    # cap = cv2.VideoCapture(0)


    # pose = mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5)
    # while webcam is running


    #returns the percentage of how good your posture is 

aaaa = VideoCamera()

while True:
    aaaa.processPosture()
