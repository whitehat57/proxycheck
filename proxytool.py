import requests
from bs4 import BeautifulSoup
import socket

# URL of the proxy list page
proxy_url = "https://www.sslproxies.org/"

def fetch_proxies():
    response = requests.get(proxy_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    proxies = []
    proxy_table = soup.find(id='proxylisttable')  # Proxy list table
    
    for row in proxy_table.tbody.find_all('tr'):
        proxy_ip = row.find_all('td')[0].text
        proxy_port = row.find_all('td')[1].text
        proxies.append(f"{proxy_ip}:{proxy_port}")
    
    return proxies

# Test the proxy to see if it's valid
def validate_proxy(proxy):
    try:
        proxy_ip, proxy_port = proxy.split(':')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)  # 3 seconds timeout
        sock.connect((proxy_ip, int(proxy_port)))
        sock.close()
        return True
    except Exception as e:
        return False

# Fetch and validate proxies
def get_valid_proxies():
    all_proxies = fetch_proxies()
    valid_proxies = []
    
    for proxy in all_proxies:
        if validate_proxy(proxy):
            valid_proxies.append(proxy)
    
    return valid_proxies
