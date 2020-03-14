import socket
import logging
import tabulate
from tabulate import tabulate
import templates

logging.basicConfig(format="%(asctime)s!%(levelname)s!%(message)s")


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("192.168.19.96", 5000))
server_socket.listen()

table = tabulate(tabular_data={("Egor", 45), ("Pavel", 12), ("Bogdan", 1)},
                 headers= {"user", "hours"},
                 tablefmt="HTML"
)
def get_response(request):
    if request:
        url = request[0].split()
        if len(url) > 1:
            url = url[1]
        else:
            logging.error("url is empty")
            return
        if url == "/favicon.ico":
            logging.error("favicon.ico")
            return
        if url == "/main":
            return b"HTTP/1.1 200 OK\n\n" + templates.main
        elif url == "/shop":
            return b"HTTP/1.1 200 OK\n\n" + templates.shop
        elif url == "/users":
            return ("HTTP/1.1 200 OK\n\n" + table).encode("utf-8")
        else:
            return b"HTTP/1.1 404 Not found\n\n<h1>404<h1>"


def sender(client, msg):
    if msg:client.sendall(msg)
    client.close()

while True:
    client, addr = server_socket.accept()
    logging.warning(f"accept client by addr {addr}")
    print(f"accept client by addr {addr}")
    msg = client.recv(2048)
    request = msg.decode("utf-8").split("\n")
    respons = get_response(request)
    sender(client, respons)
    client.close()

