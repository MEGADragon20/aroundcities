import socket
import requests

def get_local_ip():
    """
    Obtains the local IP address by attempting to connect to an server
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def get_public_ip():
    """
    Obtains the public IP address using an API endpoint
    """
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip_publica = response.json()['ip']
        return ip_publica
    except requests.RequestException as e:
        return f"Error obteniendo IP pública: {e}"