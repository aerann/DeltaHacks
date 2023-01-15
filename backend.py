from flask import Flask, render_template


website = Flask(__name__)

@website.route("/")
def page():
  return render_template('index.html', barValue = checkPosture())

if __name__ == '__main__':
  website.run(debug=True)