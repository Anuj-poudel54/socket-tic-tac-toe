import socket
from threading import Thread

class ServerSockert(socket.socket):

    def __init__(self) -> None:
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = self._get_server_host()
        self.PORT = 9000
        self.bind((self.HOST, self.PORT))
        self.clients: list[socket.socket] = []
        self.waiter: socket.socket | None = None
        self.game_rooms: dict[str, tuple[socket.socket, socket.socket]] = {}

    def _get_server_host(self):
        with open("server_host.txt", "r") as f:
            host = f.readline().strip()
            if host == "self":
                return socket.gethostbyname(socket.gethostname())
        return host

    def _new_room_id(self):
        ids = list(self.game_rooms.keys())
        if not ids:
            return 0

        return int(ids[-1]) + 1
    
    def _broadcast_room(self, room_id: str, msg: str | bytes):
            if isinstance(msg, str):
                msg = msg.encode()

            socks = self.game_rooms.get(room_id)
            if not socks:
                return
            for sock in socks:
                sock.send(msg)

    def _read_msg(self, sock: socket.socket):
        msg = sock.recv(1024).decode()
        if not msg:
            return None

        return msg

    def _handle_client_socket(self, sock: socket.socket):
        while True:
            msg = self._read_msg(sock)
            if not msg:
                continue

            room_id, msg = msg.split(" ")
            self._broadcast_room(room_id, msg)

    def _create_room(self, sock1: socket.socket, sock2: socket.socket):
        new_id = str(self._new_room_id())
        self.game_rooms[new_id] = (sock1, sock2)
        # self._broadcast_room(new_id, self._build_info_msg("MATCH_FOUND"))

        Thread(target=self._handle_client_socket, args=(sock1,), daemon=True).start()
        Thread(target=self._handle_client_socket, args=(sock2,), daemon=True).start()

        return new_id

    def _build_info_msg(self, msg: str):
        return ("I"+msg).encode()

    def start_server(self):
        self.listen(3)
        while True:
            print(f"Listening at port {self.HOST}:{self.PORT}...")
            sock, _ = self.accept()
            if self.waiter is None:
                self.waiter = sock
                sock.send(f"{self._new_room_id()} X".encode())
            else:
                room_id = self._create_room(self.waiter, sock)
                sock.send(f"{room_id} O".encode())
                self.waiter = None

        self.close()


if __name__ == "__main__":
    ServerSockert().start_server()