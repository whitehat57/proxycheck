# proxycheck
python tool to scrape proxy

Berikut adalah penjelasan bagian per bagian dari kode Python yang diberikan:

1. Importing Libraries
```
import requests
from bs4 import BeautifulSoup
import socket
requests: Library ini digunakan untuk melakukan HTTP requests di Python. Di sini, digunakan untuk mengirim permintaan ke halaman web yang berisi daftar proxy.
BeautifulSoup: Bagian dari library bs4 yang digunakan untuk memparsing HTML atau XML agar lebih mudah mengambil data dari halaman web.
socket: Library bawaan Python yang menyediakan akses ke socket-level network interface. Digunakan untuk membuat koneksi jaringan antara client dan server, misalnya, untuk memeriksa apakah proxy dapat terhubung ke suatu alamat IP.
2. Definisi URL Proxy
python
Copy code
proxy_url = "https://www.sslproxies.org/"
Variabel proxy_url berisi URL dari halaman yang menyediakan daftar proxy gratis. Dalam hal ini, URL tersebut mengarah ke "https://www.sslproxies.org/".
```
3. fetch_proxies() Function
python
Copy code
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
Fungsi fetch_proxies() bertujuan untuk mengambil daftar proxy dari halaman web.
requests.get(proxy_url): Mengirim permintaan HTTP GET ke halaman web yang ditentukan di proxy_url.
soup = BeautifulSoup(response.text, 'html.parser'): Memparsing HTML dari halaman web dengan BeautifulSoup untuk memudahkan pengambilan data.
proxy_table = soup.find(id='proxylisttable'): Mencari elemen HTML dengan id='proxylisttable', yang merupakan tabel yang berisi daftar proxy di halaman tersebut.
Loop:
for row in proxy_table.tbody.find_all('tr'):: Melakukan iterasi melalui setiap baris (row) dalam tabel yang ditemukan. Setiap baris berisi informasi mengenai satu proxy.
proxy_ip = row.find_all('td')[0].text: Mengambil alamat IP proxy dari kolom pertama (<td>).
proxy_port = row.find_all('td')[1].text: Mengambil port dari kolom kedua (<td>).
proxies.append(f"{proxy_ip}:{proxy_port}"): Menambahkan proxy dalam format ip:port ke dalam list proxies.
Return: Mengembalikan daftar proxy yang dikumpulkan.
4. validate_proxy(proxy) Function
python
Copy code
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
Fungsi validate_proxy(proxy) memeriksa apakah proxy yang diberikan valid dengan mencoba membuat koneksi menggunakan alamat IP dan port dari proxy.
proxy_ip, proxy_port = proxy.split(':'): Memisahkan alamat IP dan port dari string proxy, yang formatnya ip:port.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM): Membuat socket TCP yang digunakan untuk melakukan koneksi ke IP dan port proxy.
sock.settimeout(3): Menetapkan batas waktu untuk koneksi menjadi 3 detik. Jika koneksi tidak berhasil dalam 3 detik, maka proxy dianggap tidak valid.
sock.connect((proxy_ip, int(proxy_port))): Mencoba melakukan koneksi ke proxy yang ditentukan.
sock.close(): Menutup koneksi socket jika berhasil.
Return True jika koneksi berhasil, menandakan proxy valid.
Exception handling: Jika terjadi kesalahan (misalnya, proxy tidak responsif atau tidak dapat dihubungi), fungsi akan menangkap error dan mengembalikan False yang berarti proxy tersebut tidak valid.
5. get_valid_proxies() Function
python
Copy code
def get_valid_proxies():
    all_proxies = fetch_proxies()
    valid_proxies = []
    
    for proxy in all_proxies:
        if validate_proxy(proxy):
            valid_proxies.append(proxy)
    
    return valid_proxies
Fungsi get_valid_proxies() bertujuan untuk mendapatkan daftar proxy yang valid.
all_proxies = fetch_proxies(): Mengambil semua proxy dari halaman web menggunakan fungsi fetch_proxies().
Loop:
for proxy in all_proxies:: Melakukan iterasi melalui setiap proxy dalam daftar all_proxies.
if validate_proxy(proxy):: Memeriksa apakah proxy tersebut valid menggunakan fungsi validate_proxy().
valid_proxies.append(proxy): Jika proxy valid, tambahkan ke dalam daftar valid_proxies.
Return: Mengembalikan daftar proxy yang telah divalidasi dan terbukti dapat digunakan.
Kesimpulan:
Kode ini mengambil daftar proxy dari sebuah situs web, lalu memeriksa apakah proxy-proxy tersebut dapat digunakan dengan mencoba terhubung ke setiap proxy. Kode tersebut memanfaatkan kombinasi requests, BeautifulSoup, dan socket untuk mengambil data dari web dan melakukan koneksi jaringan.
