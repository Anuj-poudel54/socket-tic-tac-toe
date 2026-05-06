import socket
from threading import Thread

class ClientSocket(socket.socket):
    def __init__(self) -> None:
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)

        self.connect(self._read_sock_address())
        self.msg = None
        Thread(target=self._start_reading_thread).start()

    def _start_reading_thread(self):
        while True:
            msg = self.recv(1024).decode()
            if not msg:
                continue
            self.msg = msg

    def _read_sock_address(self):
        with open("addr.txt", "r") as f:
            addr = f.readline()

        addr, port = addr.split(" ")
        return (addr, int(port))

    def is_closed(self):
        return self._closed

    @property
    def _socket_msg(self):
        msg = self.msg
        self.msg = None
        return msg
    
    def get_ind(self):
        msg = self._socket_msg
        if not msg:
            return None
        return msg

if __name__ == "__main__":
    from time import sleep
    cs = ClientSocket()
    while True:
        cs.send("IG0 8".encode())
        ind = cs.get_ind()
        if ind:
            print(ind)
        if(cs._closed):
            break
        sleep(.5)