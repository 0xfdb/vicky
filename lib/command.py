import re

from lib.objects import Message  # , Role


# TODO roles
def command(aliases: list, description: str, role=None, **attrs):
    def wrap(f):
        f.__command__ = True
        f.__command_name__ = aliases
        if description:
            f.__description__ = description
        else:
            f.__description__ = "N/A"
        if role:
            f.__role__ = role
            f.__restricted__ = True
        else:
            f.__restricted__ = False
        return f
    return wrap


class Command:
    def __init__(self, prefix: str, data: Message):
        self.prefix = prefix
        self.data = data
        self.message = data.message
        self.name = ""

        parsed = re.search(
            "{}(\w+)(\\b.*)".format(self.prefix),
            self.message)
        if parsed is not None:
            self.name, self.message = parsed.groups()
            self.message = self.message.lstrip()
