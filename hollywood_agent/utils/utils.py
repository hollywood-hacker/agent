# utils.py
import requests
import socket

def run_request(url):
    """Send a GET request to the given URL."""
    response = requests.get(url)

def get_local_ip():
    """Get the local IP address."""
    hostname = socket.getfqdn()
    ip_addresses = [addr[4][0] for addr in socket.getaddrinfo(hostname, None)]
    network_ips = [ip for ip in ip_addresses if not ip.startswith("127.") and not ip.startswith("::1")]
    return network_ips[0] if network_ips else '127.0.0.1'
