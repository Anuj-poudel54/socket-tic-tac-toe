from enum import Enum
from dataclasses import dataclass

class MessageType(Enum):
    INFO = 0
    IN_GAME = 1

type_initial_map = {
    MessageType.INFO: "I",
    MessageType.IN_GAME: "G",
}

@dataclass
class Message:
    msg: str
    # msg_type: MessageType | None = None

    def __post_init__(self):
        self.determine_message_type()

    def determine_message_type(self):

        self.msg_type = None

        if self.msg.startswith("IG"):
            self.msg_type = MessageType.IN_GAME

        elif self.msg.startswith("I"):
            self.msg_type = MessageType.INFO

        if self.msg_type:
            self.msg = self.msg[len(type_initial_map.get(self.msg_type, "")):]

