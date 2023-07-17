from cement import App, CaughtSignal, Controller, ex
from .task.periodic_task import PeriodicTask
from .server.flask_server import FlaskServer
from .utils.utils import get_local_ip
import socket

def get_configuration_values(app):
    # Load config values
    remote_host = app.config.get('hollywood_agent', 'RemoteHost', fallback='localhost')
    remote_port = app.config.get('hollywood_agent', 'RemotePort', fallback=4200)
    use_hostname = app.config.get('hollywood_agent', 'UseHostname', fallback=True)
    local_address = socket.gethostname() if use_hostname else get_local_ip()
    
    server_ip = app.config.get('hollywood_agent', 'ServerIP', fallback='0.0.0.0')
    server_port = app.config.get('hollywood_agent', 'ServerPort', fallback=5001)

    return remote_host, remote_port, use_hostname, local_address, server_ip, server_port

def start_periodic_task(remote_host, remote_port, use_hostname, local_address):
    # Start the periodic task
    task = PeriodicTask(remote_host, remote_port, use_hostname, local_address)
    task.start()

def start_flask_server(server_ip, server_port):
    # Start the Flask server
    server = FlaskServer(server_ip, server_port)
    server.start()

class Base(Controller):
    class Meta:
        label = 'base'
        description = 'Client agent for Hollywood Hacker'
        epilog = 'Usage: hollywood_agent command1 --foo bar'
        arguments = []

    def _default(self):
        """Default action if no sub-command is passed."""
        self.app.args.print_help()

    @ex(
        help='Start agent server',
    )
    def start(self):
        remote_host, remote_port, use_hostname, local_address, server_ip, server_port = get_configuration_values(self.app)
        start_periodic_task(remote_host, remote_port, use_hostname, local_address)
        start_flask_server(server_ip, server_port)


class MyApp(App):
    class Meta:
        label = 'hollywood_agent'
        handlers = [Base]
        close_on_exit = True

    def get_version(self):
        return '0.0.1'


def main():
    with MyApp() as app:
        try:
            app.run()
        except CaughtSignal as e:
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
