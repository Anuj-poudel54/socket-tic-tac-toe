from typing import Callable

from client_manager import ClientManager, DEFAULT_ROOM_NAME
from rooms import rooms, admit_client_in_room, broadcast_msg

_cmd_func_map: dict[str, Callable[[list, ClientManager], bool]] = {}
_admin_cmd_func: dict[str, Callable[[list, ClientManager], bool]] = {}

def register_command(names: str | list, admin_command=False):
    global _cmd_func_map, _admin_cmd_func

    def wrapper(func):
        if isinstance(names, str):
            names_list = [names]
        else:
            names_list = names

        for name in names_list:
            if not admin_command:
                _cmd_func_map[name] = func
            else:
                _admin_cmd_func[name] = func

    return wrapper

@register_command(names="join")
def join_command(command: list, client: ClientManager):
    print(command)
    print("Here")
    if not command[1]:
        client.sendln("Enter valid room name")
        return False

    client_room_name = command[1]
    admit_client_in_room(client, client_room_name)


@register_command(names="me")
def me_command(command: list, client: ClientManager):
    msg = f"'{client.name}' is in '{client.room}' room"
    client.sendln(msg)

@register_command(names="name")
def name_command(command: list, client: ClientManager):
    if len(command) >= 2:
        name = command[1].strip()
        if name:
            client.name = name

    client.sendln(f"Name: {client.name}")
    return True

@register_command(names="admin")
def admin_command(command: list, client: ClientManager):
    if len(command) < 2:
        client.sendln("Enter valid command for admin switching")
        return False

    admin_pwd = command[1]
    if not admin_pwd:
        client.sendln("not valid admin password")
        return False

    if admin_pwd == "123":
        raise NotImplemented()
    
@register_command(names="rooms")
def rooms_command(command: list, client: ClientManager):
    all_rooms = rooms.keys()
    msg = ' | '.join(all_rooms)
    client.sendln(msg)

@register_command(names="bye")
def bye_command(command: list, client: ClientManager):
    cur_room = client.exit_room()
    rooms[cur_room].remove(client)
    admit_client_in_room(client, DEFAULT_ROOM_NAME)
    broadcast_msg(cur_room, f"'{client.name}' exited this room :(")


def handle_command(command_wo_pref: str, client: ClientManager):

    command = command_wo_pref.split(" ")
    pref = command[0]

    func = _cmd_func_map.get(pref)
    if func and func(command, client) is False:
        return False
    elif not func:
        res = f"'${command_wo_pref}' is not a valid command"
        client.sendln(res)
        return False
    
    return True