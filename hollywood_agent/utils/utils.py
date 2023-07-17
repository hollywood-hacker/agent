# utils.py
import requests
import socket

def run_request(url):
    """Send a GET request to the given URL."""
    response = requests.get(url)

import psutil

def get_local_ip():
    """Get all local IP addresses excluding the loopback address."""
    ip_addresses = []
    for iface in psutil.net_if_addrs().values():
        for addr in iface:
            if addr.family == socket.AF_INET and not addr.address.startswith('127.'):
                ip_addresses.append(addr.address)

    return ip_addresses[0]