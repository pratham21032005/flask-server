from flask import Flask, request, jsonify, send_from_directory, abort
from functools import wraps
import logging

app = Flask(__name__, static_folder='static')

# === Logging ===
logging.basicConfig(level=logging.INFO)

# === Basic Authentication ===
USERNAME = 'admin'
PASSWORD = 'secret'

def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

def authenticate():
    return jsonify({"message": "Authentication required"}), 401, {'WWW-Authenticate': 'Basic realm="Login Required"'}

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# === Static File Serving ===
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# === API Route Example ===
@app.route('/api/hello', methods=['GET'])
@requires_auth
def api_hello():
    app.logger.info("Hello API called")
    return jsonify({"message": "Hello, authenticated user!"})

@app.route('/api/echo', methods=['POST'])
@requires_auth
def api_echo():
    data = request.json
    app.logger.info(f"Received data: {data}")
    return jsonify({"you_sent": data})

# === Error Handling ===
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

# === Run Server ===
if __name__ == '__main__':
    app.run(debug=True, port=5000)
