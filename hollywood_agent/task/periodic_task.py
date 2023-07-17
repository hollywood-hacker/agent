import threading
import os
from ..utils.utils import run_request
import logging
import requests

class PeriodicTask:
    """Class to encapsulate the periodic pinging of the remote host."""

    def __init__(self, remote_host, remote_port, use_hostname, local_address):
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.use_hostname = use_hostname
        self.local_address = local_address

    def start(self):
        """Start the periodic task."""
        self._run_periodically()

    def _run_periodically(self):
        """Function to run periodically."""
        print('Pinging manager application')
        try:
            os_info = os.uname()   # Retrieve OS information
            run_request(f"http://{self.remote_host}:{self.remote_port}?host={self.local_address}&port={self.remote_port}&os={os_info.sysname}")
        except requests.exceptions.RequestException as e:
            logging.error('Error reaching host: %s', e)
        except Exception as e:
            logging.error('Unexpected error: %s', e)

        threading.Timer(10, self._run_periodically).start()
