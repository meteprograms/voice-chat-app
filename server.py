import socket
import threading

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000
BUFFER_SIZE = 4096

clients = []

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            broadcast(client_socket, data)
        except:
            clients.remove(client_socket)
            break
    client_socket.close()


def broadcast(sender_socket, data):
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(data)
            except:
                clients.remove(client)


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen(5)
    print(f"[*] Server listening on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr}")
        clients.append(client_socket)
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    start_server()