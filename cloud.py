from flask import Flask, render_template, request
from flask_cors import CORS
import globallight



app = Flask(__name__, template_folder='templates', static_folder="static")
CORS(app)


#Cloud UI
@app.route('/', methods=["GET"])
def index():
	results = globallight.read()
	return render_template('cloud.html', readings = results)

@app.route('/api/globallight', methods=["PUT"])
def create():
    payload = request.get_json()
    return globallight.create(payload)

@app.route('/api/globallight', methods=["GET"])
def get():
    return globallight.read()

@app.route('/api/lightcluster', methods=["POST"])
def cluster():
    payload = request.get_json()
    return globallight.cluster(payload)

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
