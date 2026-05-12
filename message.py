from enum import Enum

class MessageType(Enum): 
    PLAY        = 0 # for game play related
    PLAYER_QUIT = 1 # if player quits the game in between
    SERVER_MSG  = 2 # server sends message to player
    PLAYER_MSG  = 3 # player sending message to another player

class Message:
    def __init__(self, msg: bytes | str, message_type: int | None = None):
        if isinstance(msg, (bytes, bytearray)):
            self._msg = str(msg)
        else:
            self._msg = msg

        self.type: int | None = message_type if message_type else None
        self._decode_msg()

    def _decode_msg(self):
        raise NotImplementedError()

    def build_message_for_socket(self):
        return f"{self.type} {self.msg}".encode()

class ServerMessage(Message):
    """
    message architecture from server to client
    `message_type msg`
    """
    def __init__(self, msg: str | bytes):
        super().__init__(msg)

    def _decode_msg(self):
        msg_type, self.msg = self._msg.split(" ")
        if msg_type.isnumeric():
            self.type = int(msg_type)

class ClientMessage(Message):
    """
    message architecture from server to client
    `room_id message_type msg`
    """

    def __init__(self, msg: str | bytes):
        self.room_id: str
        super().__init__(msg)

    def _decode_msg(self):
        self.room_id, self.type, self.msg = self._msg.split(" ")

    def build_message_for_socket(self):
        return f"{self.room_id} {self.type} {self.msg}".encode()