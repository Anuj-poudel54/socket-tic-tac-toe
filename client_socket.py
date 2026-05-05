import socket

class ClientSocket(socket.socket):
    def __init__(self) -> None:
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)

        self.connect(self._read_sock_address())

    def _read_sock_address(self):
        with open("addr.txt", "r") as f:
            addr = f.readline()

        addr, port = addr.split(" ")
        return (addr, int(port))

    def is_closed(self):
        return self._closed

    def read_msg(self):
        return self.recv(1024).decode()

if __name__ == "__main__":
    cs = ClientSocket()
    while True:
        cs.read_msg()
        if(cs._closed):
            break