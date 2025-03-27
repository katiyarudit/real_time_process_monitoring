from flask import Flask, jsonify, request
import psutil
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_process_info():
    processes = []
    try:
        for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            processes.append(proc.info)
    except Exception as e:
        return {"error": str(e)}
    return processes

@app.route('/processes', methods=['GET'])
def processes():
    return jsonify(get_process_info())

@app.route('/cpu', methods=['GET'])
def cpu_usage():
    return jsonify({'cpu': psutil.cpu_percent(interval=1)})

@app.route('/memory', methods=['GET'])
def memory_usage():
    return jsonify({'memory': psutil.virtual_memory().percent})

@app.route('/terminate', methods=['POST'])
def terminate_process():
    try:
        data = request.get_json()
        pid = data.get("pid")
        if pid is None:
            return jsonify({"error": "PID is required"}), 400
        process = psutil.Process(pid)
        process.terminate()
        return jsonify({"message": f"Process {pid} terminated successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
