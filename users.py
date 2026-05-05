
from dataclasses import dataclass
from client_manager import ClientManager

class XUser:
    client: ClientManager


@dataclass
class AdminUserManager(XUser):
    ...