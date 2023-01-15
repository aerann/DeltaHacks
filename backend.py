# from flask import Flask, render_template, Response
# from test import VideoCamera

# website = Flask(__name__)

# @website.route("/")
# def page():
#   return render_template('index.html')

# def gen(camera):
#     while True:
#       frame = camera.get_frame()
#       yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n'
#       + frame + b'\r\n\r\n')

# @website.route('/video_feed')
# def video_feed():
#   return Response(gen(VideoCamera()),
#   mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == '__main__':
#   website.run(host='0.0.0.0', port='5000', debug=True)