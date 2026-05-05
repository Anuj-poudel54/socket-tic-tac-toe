import socket
from collections import defaultdict

from client_manager import ClientManager, DEFAULT_ROOM_NAME, LINESEP

rooms: dict[str, list[ClientManager]] = defaultdict(list)
rooms.update({DEFAULT_ROOM_NAME: []})

def admit_client_in_room(client: ClientManager, room: str):
    if client.room != DEFAULT_ROOM_NAME:
        client.build_msg("You are already in a room, exit the room first using '$bye'").send_built_msg()
        return

    client.room = room
    rooms[room].append(client)
    # removing client if they are not in default room.
    rooms[DEFAULT_ROOM_NAME].remove(client) if room != DEFAULT_ROOM_NAME and client in rooms[DEFAULT_ROOM_NAME] else None
    res = f"'{client.name}' joined the room '{client.room}'"
    broadcast_msg(client.room, res)
    print(res)

def broadcast_msg(room_name: str, msg: str, sender: str = "", self_broadcast=False):
    global rooms
    room_clients =  rooms.get(room_name)
    if not room_clients:
        print(f"ERROR: room {room_name} not found!")
        return False

    if sender:
        msg = f"{sender}> {msg} "
    for client in room_clients:
        if not self_broadcast and sender and client.name == sender:
            continue
        client.sendln(msg)

def collect_msg(client_socket: socket.socket):

    msg_str = ""
    while True:
        letter = client_socket.recv(1024).decode('utf-8')

        if letter != LINESEP:
            msg_str += letter
            continue

        return msg_str