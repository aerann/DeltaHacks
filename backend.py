from flask import Flask, render_template, Response
import test import VideoCamera
import cv2

website = Flask(__name__)

@website.route("/")
def page():
  return render_template('index.html')

def gen():
    # frame = getWebFrame(cap)
    # yield (b'--frame\r\n'
    # b'Content-Type: image/jpeg\r\n\r\n' + frame
    # + b'\r\n\r\n')

@website.route('/video_feed')
def video_feed():
  return Response(gen(VideoCamera()))

if __name__ == '__main__':
  website.run(host='0.0.0.0', port='5000', debug=True)