from cement import App, CaughtSignal, Controller, ex
import keyboard
from flask import Flask, request
import requests
import socket
import threading
import logging


def run_request(url):
    response = requests.get(url)
    # print("Response status: ", response.status_code)
    # print("Response body: ", response.text)

def get_local_ip():
    hostname = socket.getfqdn()
    ip_addresses = [addr[4][0] for addr in socket.getaddrinfo(hostname, None)]
    network_ips = [ip for ip in ip_addresses if not ip.startswith("127.") and not ip.startswith("::1")]
    if network_ips:
        return network_ips[0]
    else:
        return '127.0.0.1'


class Base(Controller):
    class Meta:
        label = 'base'

        # text displayed at the top of --help output
        description = 'Client agent for Hollywood Hacker'

        # text displayed at the bottom of --help output
        epilog = 'Usage: hollywood_agent command1 --foo bar'

        # controller level arguments. ex: 'hollywood_agent --version'
        arguments = []


    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()


    @ex(
        help='Start agent server',
    )
    def start(self):
        # Load config values
        def run_periodically():
            print('Pinging manager application')
            try:
                remote_host = self.app.config.get('hollywood_agent', 'RemoteHost', fallback='localhost')
                remote_port = self.app.config.get('hollywood_agent', 'RemotePort', fallback=4200)
                use_hostname = self.app.config.get('hollywood_agent', 'UseHostname', fallback=True)
                
                if use_hostname:
                    local_address = socket.gethostname()
                else:
                    local_address = get_local_ip()
                            
                run_request(f"http://{remote_host}:{remote_port}?{local_address}")
            except requests.exceptions.RequestException as e:
                # Log the error
                logging.error('Error reaching host: %s', e)
            except Exception as e:
                # Catch-all for other exceptions
                logging.error('Unexpected error: %s', e)
            threading.Timer(10, run_periodically).start()

        # Start the thread that runs run_request every 10 seconds
        run_periodically()

        # Run the main app in the main thread
        server_ip = self.app.config.get('hollywood_agent', 'ServerIP', fallback='0.0.0.0')
        server_port = self.app.config.get('hollywood_agent', 'ServerPort', fallback=5001)

        flask = Flask(__name__)
        
        @flask.route('/keystrokes', methods=['GET'])
        def handle_keystrokes():
            keystrokes = request.args.get('keystrokes').replace(" ", "+")
            if keystrokes is not None:
                keyboard.press_and_release(keystrokes)
                return f"Received keystrokes: {keystrokes}"
            else:
                return "No keystrokes provided."

        @flask.route('/text', methods=['GET'])
        def handle_text():
            text = request.args.get('text')
            if text is not None:
                keyboard.write(text)
                return f"Received text: {text}"
            else:
                return "No text provided."
                
        flask.run(host=server_ip, port=server_port)


class MyApp(App):
    class Meta:
        # application label
        label = 'hollywood_agent'

        # register handlers
        handlers = [
            Base
        ]

        # call sys.exit() on close
        close_on_exit = True

    def get_version(self):
        return '0.0.1'



def main():
    with MyApp() as app:
        try:
            app.run()
        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
