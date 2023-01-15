from flask import Flask,render_template,Response
import mediapipe as mp
import cv2
# import postureChecker

app=Flask(__name__)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5)
# global good_left
# global good_right
# good_left = 0
# good_right = 0


camera=cv2.VideoCapture(0)

def generate_frames():
    good_left = 0
    good_right = 0
    while True:
        ## read the camera frame
        success,image=camera.read()
        if not success:
            break
        else:
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
            global keypoints
            global lm
            global lmPose
            global h,w
            global percentage

            keypoints = pose.process(image)
            lm = keypoints.pose_landmarks
            lmPose = mp_pose.PoseLandmark
            h,w = image.shape[:2]

            
        
            # wait for user to type in p 
            if cv2.waitKey(1) == ord('p'):
                print('POSITION RECORDED!')
                good_left = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h) 
                good_right = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)

            l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)
            r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)

            height = camera.get(4)  # float `height`
            range = height - good_left
            relative = l_shldr_y - good_left
            percentage = 0

            if(good_left == 0 and good_right == 0): 
                print("Press P to record your position, or q to quit!")
            if(l_shldr_y > good_left + 15 or r_shldr_y > good_right + 15):
                percentage = 100- ((relative/range) * 100)
                if (percentage <= 0):
                    percentage = 0
                print("BAD POSTURE, %", percentage)
            else:
                percentage = 100
                print("GOOD POSTURE!, %", percentage)

            #flip image horizontally for mirrored view
            image = cv2.flip(image, 1)
            cv2.imshow('MediaPipe Pose', image)
            
            ret,buffer=cv2.imencode('.jpg',image)

            image=buffer.tobytes()


            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/calibrate')
def calibrate():

    good_left = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h) 
    good_right = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)
    print(good_left)
    print(good_right)
    return render_template('index.html')

@app.route('/percentage')
def percentage():
    return percentage


if __name__=="__main__":
    app.run(debug=True)


