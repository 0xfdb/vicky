import time
from dataclasses import dataclass, field
from typing import List, NoReturn


class Events:
    Nick = "nick"
    PubMsg = "pubmsg"
    PrivMsg = "privmsg"
    Join = "join"
    Topic = "topic"
    Part = "part"
    Quit = "quit"


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
    ts: float = time.time()


@dataclass
class Channel:
    users: List[User]
    name: str

    def getuser(self, nick) -> User:
        for user in self.users:
            if user.nick == nick:
                return user

    def adduser(self, user: User) -> NoReturn:
        self.users.append(user)

    def remove(self, nick) -> NoReturn:
        user = self.getuser(nick)
        # mehhhhh
        for i, _ in enumerate(self.users):
            if user == _:
                del self.users[i]

    def setnick(self, nick, newnick) -> NoReturn:
        user = self.getuser(nick)
        print(user)
        user.nick = newnick
