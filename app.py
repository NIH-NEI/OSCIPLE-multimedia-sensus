from flask import Flask, render_template, send_from_directory, request, make_response
from automator import *
import json

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
	return render_template("index.html")

@app.route('/static/css/<path:path>')
def send_report(path):
	return send_from_directory('static/css', path)

automator = Automator()
@app.route("/ajax")
def ajax():
	cmd = request.args["cmd"]
	cmdparse = automator.commandParse(cmd)
	print (cmdparse)
	print (automator.cell, automator.ws)
	resp = make_response(json.dumps(cmdparse), 200)
	resp.mimetype = "application/json"
	return resp


if __name__ == '__main__':
	app.run(debug=True)