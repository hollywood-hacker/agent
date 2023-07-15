import configparser
import keyboard
from flask import Flask, request
import requests
import socket
import threading

app = Flask(__name__)

@app.route('/keystrokes', methods=['GET'])
def handle_keystrokes():
    keystrokes = request.args.get('keystrokes').replace(" ", "+")
    if keystrokes is not None:
        keyboard.press_and_release(keystrokes)
        return f"Received keystrokes: {keystrokes}"
    else:
        return "No keystrokes provided."

@app.route('/text', methods=['GET'])
def handle_text():
    text = request.args.get('text')
    if text is not None:
        keyboard.write(text)
        return f"Received text: {text}"
    else:
        return "No text provided."

def run_request(url):
    response = requests.get(url)
    print("Response status: ", response.status_code)
    print("Response body: ", response.text)

def get_local_ip():
    hostname = socket.getfqdn()
    ip_addresses = [addr[4][0] for addr in socket.getaddrinfo(hostname, None)]
    network_ips = [ip for ip in ip_addresses if not ip.startswith("127.") and not ip.startswith("::1")]
    if network_ips:
        return network_ips[0]
    else:
        return '127.0.0.1'

def main():
    # Load config values
    config = configparser.ConfigParser()
    config.read('config.ini')
    remote_host = config['DEFAULT']['RemoteHost']
    remote_port = config['DEFAULT']['RemotePort']

    def run_periodically():
        print('Pinging manager application')
        try:
            config = configparser.ConfigParser()
            config.read('config.ini')
            use_hostname = config.getboolean('DEFAULT', 'UseHostname')
            
            if use_hostname:
                local_address = socket.gethostname()
            else:
                local_address = get_local_ip()
            
            run_request(f"http://{remote_host}:{remote_port}?{local_address}")
        except:
            pass
        threading.Timer(10, run_periodically).start()

    # Start the thread that runs run_request every 10 seconds
    run_periodically()

    # Run the main app in the main thread
    app.run(host='0.0.0.0', port=5001)
    
if __name__ == '__main__':
    main()
