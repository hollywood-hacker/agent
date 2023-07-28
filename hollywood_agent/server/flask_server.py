# flask_server.py
from flask import Flask, request
from werkzeug.utils import secure_filename
import keyboard
import os
import subprocess

class FlaskServer:
    """Class to encapsulate the Flask server."""

    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.app = Flask(__name__)

    def start(self):
        """Start the Flask server."""

        @self.app.route('/keystrokes', methods=['GET'])
        def handle_keystrokes():
            keystrokes = request.args.get('keystrokes').replace(" ", "+")
            if keystrokes is not None:
                keyboard.press_and_release(keystrokes)
                return f"Received keystrokes: {keystrokes}"
            else:
                return "No keystrokes provided."

        @self.app.route('/text', methods=['GET'])
        def handle_text():
            text = request.args.get('text')
            if text is not None:
                keyboard.write(text)
                return f"Received text: {text}"
            else:
                return "No text provided."
        
        @self.app.route('/upload', methods=['POST'])
        def file_upload():
            if 'file' not in request.files:
                return 'No file part in the request', 400

            file = request.files['file']

            if file.filename == '':
                return 'No file selected for uploading', 400

            script_dir = os.path.dirname(os.path.realpath(__file__))
            UPLOAD_FOLDER = os.path.join(script_dir, 'uploaded_assets')

            # Check if the upload directory exists, create it if it doesn't
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # Open the file using the system's default program
            subprocess.run(['open', filepath])

            return f'File {filename} uploaded and opened successfully', 200

        self.app.run(host=self.server_ip, port=self.server_port)
