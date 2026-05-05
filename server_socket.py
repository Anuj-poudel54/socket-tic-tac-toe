import socket

class ServerSockert(socket.socket):

    def __init__(self) -> None:
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.HOST = "localhost"
        self.PORT = 9000
        self.bind((self.HOST, self.PORT))
        self.clients: list[socket.socket] = []
        self.waiter: socket.socket
        self.game_rooms: dict[str, tuple[socket.socket, socket.socket]] = {}

    def handle_client_socket(self):
        ...

    def start_server(self):
        while True:
            print(f"Listening at port {self.HOST}:{self.PORT}...")
            self.listen(3)
            sock, addr = self.accept()
            if self.waiter is None:
                self.waiter = sock

            self.close()


if __name__ == "__main__":
    ServerSockert().start_server()