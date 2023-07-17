from cement import App, CaughtSignal, Controller, ex
from .task.periodic_task import PeriodicTask
from .server.flask_server import FlaskServer
from .utils.utils import get_local_ip
import socket

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
        arguments=[
            (['-i', '--ip'],
             {'help': 'IP address of the server',
              'action': 'store',
              'dest': 'ip'}),
            (['-p', '--port'],
             {'help': 'Port number of the server',
              'action': 'store',
              'dest': 'port'})
        ],
    )
    def start(self):
        # Load config values directly
        remote_host = self.app.config.get('hollywood_agent', 'RemoteHost', fallback='localhost')
        remote_port = self.app.config.get('hollywood_agent', 'RemotePort', fallback=4200)
        use_hostname = self.app.config.get('hollywood_agent', 'UseHostname', fallback=True)
        local_address = socket.gethostname() if use_hostname else get_local_ip()
        
        if '.local' not in local_address and use_hostname:
            local_address = '{0}.local'.format(local_address)
        
        # Get server ip and port values, use user-provided values if available, else use configuration or fallback values
        server_ip = self.app.pargs.ip if self.app.pargs.ip else self.app.config.get('hollywood_agent', 'ServerIP', fallback=get_local_ip())
        server_port = self.app.pargs.port if self.app.pargs.port else self.app.config.get('hollywood_agent', 'ServerPort', fallback=5001)
        
        # Start the periodic task
        task = PeriodicTask(remote_host, remote_port, use_hostname, local_address)
        task.start()

        # Start the Flask server
        server = FlaskServer(server_ip, server_port)
        server.start()


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
