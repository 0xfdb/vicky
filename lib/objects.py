import time
from dataclasses import dataclass, field
from typing import List


@dataclass
class User:
    nick: str
    isop: bool
    isowner: bool
    isvoiced: bool


@dataclass
class Message:
    message: str
    user: User
    ts: int = time.time()


@dataclass
class Channel:
    users: List[User]
    name: str

    def getuser(self, nick):
        for user in self.users:
            if user.nick == nick:
                return user

    def remove(self, nick):
        # HACK
        pass
        # user = self.getuser(nick)
        # del self.users[user]

    def setnick(self, nick, newnick):
        user = self.getuser(nick)
        user.nick = newnick
