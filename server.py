import ctypes
import socket
from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return '127.0.0.1'

@app.route('/')
def index():
    return 'Laptop Server is Running 🎯'

@app.route('/command', methods=['POST'])
def handle_command():
    data = request.get_json()
    print(f"Received data: {data}")  # Log the received data
    command = data.get('command')
    
    if command == "ping":
        return jsonify({"message": "Connection successful", "status": "success"}), 200
    elif command == "open_notepad":
        subprocess.Popen(['notepad.exe'])
        return jsonify({"message": "Notepad opened", "status": "success"}), 200
    elif command == "shutdown":
        os.system("shutdown /s /f /t 0")
        return jsonify({"message": "Shutting down", "status": "success"}), 200
    elif command == "lock_screen":
        ctypes.windll.user32.LockWorkStation()
        return jsonify({"message": "Screen locked", "status": "success"}), 200
    else:
        return jsonify({"message": "Unknown command", "status": "error"}), 400


if __name__ == '__main__':
    ip = get_local_ip()
    print(f"🚀 Server is live at http://{ip}:5000")
    app.run(host='0.0.0.0', port=5000)
