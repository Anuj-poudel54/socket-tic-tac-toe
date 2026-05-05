import socket
from threading import Thread

from client_manager import ClientManager, DEFAULT_ROOM_NAME, COMMAND_PREFIX
from rooms import admit_client_in_room, collect_msg, broadcast_msg
from commands import handle_command

def handle_client_socket(client: ClientManager):

    client.build_msg("Welcome!!")\
        .build_msg("You are connected to global room")\
        .build_msg("Use '$join <room name>' to create/join room.")\
        .send_built_msg()

    admit_client_in_room(client, DEFAULT_ROOM_NAME)
    while True:
        msg_str = collect_msg(client.socket)

        if msg_str.startswith(COMMAND_PREFIX):
            handle_command(msg_str[1:], client)
            continue

        broadcast_msg(client.room, msg_str, client.name)
        print(f"{client.name} ({client.room}) > {msg_str}")


def start_server_broad_cast():
    while True:
        msg = input("$$>>> ")
        broadcast_msg(DEFAULT_ROOM_NAME, msg)

def start_server(server_sock: socket.socket):
    
    # ip_address = socket.gethostbyname(socket.gethostname())
    ip_address = "localhost"

    HOST, PORT = ip_address, 9000
    server_sock.bind((HOST, PORT))
    Thread(target=start_server_broad_cast, daemon=True).start()
    while True:
        print(f"Listening at port {HOST}:{PORT}...")
        server_sock.listen(3)

        sock, addr = server_sock.accept()

        client = ClientManager(socket=sock, host_port=addr)

        print(f"Client connected: {client.name}")

        client_th = Thread(target=handle_client_socket, args=(client,), daemon=True)
        client_th.start()

if __name__ == "__main__":
    sock = socket.socket()
    start_server(sock)
