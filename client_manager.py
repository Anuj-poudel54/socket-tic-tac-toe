import socket
from dataclasses import dataclass 
import os

DEFAULT_ROOM_NAME = 'world'
COMMAND_PREFIX = '$'
LINESEP = os.linesep


@dataclass
class ClientManager:
    socket: socket.socket
    host_port: tuple[str, str | int]
    name: str = ""
    room: str = DEFAULT_ROOM_NAME
    _msg = ""

    def __post_init__(self):
        self.name = ":".join( map(lambda x: str(x), self.host_port) )
    
    def send_built_msg(self):
        n = self.sendln(self._msg)
        self._msg = ""
        return n
    
    def sendln(self, data: str, flags: int = 1, *args, **kwargs):
        if not data.endswith(LINESEP):
            data += LINESEP
        return self.socket.send(data.encode(), flags, *args, **kwargs)
    
    def build_msg(self, msg: str):
        if not msg.endswith(LINESEP):
            msg += LINESEP
        self._msg += msg

        return self
    
    def exit_room(self):
        room = self.room
        self.room = DEFAULT_ROOM_NAME
        return room

