# flask_server.py
from flask import Flask, request
import keyboard

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
        
        self.app.run(host=self.server_ip, port=self.server_port)
