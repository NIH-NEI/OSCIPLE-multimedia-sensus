from flask import Flask, render_template, send_from_directory

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
	return render_template("index.html")

@app.route('/static/css/<path:path>')
def send_report(path):
    return send_from_directory('static/css', path)


if __name__ == '__main__':
	app.run(debug=True)