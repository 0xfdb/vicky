#! /usr/bin/env python

import logging
import re
from dataclasses import dataclass
from typing import List

import irc.bot
import irc.strings
from irc.client import NickMask
from lib.cog import CogManager
from lib.command import Command
from lib.objects import Channel, Message, User

# urlexpression = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
logging.basicConfig(level=logging.DEBUG)


class Vicky(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667, enabled=[]):
        self.bot = irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname,
                                            nickname)
        self.channel = Channel(users=[], name=channel)
        self.cm = CogManager()

    def run(self):
        enabled_modules = ['example']
        self.cm.load_all(enabled_modules, bot=self)
        self.start()

    def sendmsg(self, msg: str, channel=None):
        # TODO split and send for long messages
        self.connection.privmsg(self.channel.name, msg)

    def on_nicknameinuse(self, client, event):
        client.nick(client.get_nickname() + "_")

    def on_welcome(self, client, event):
        client.join(self.channel.name)

    def on_join(self, c, event):
        print(event)
        # self.connection.privmsg(self.channel, "I have joined!")
        self.sendmsg("")

    def on_namreply(self, c, event):
        self.gen_userlist()

    def on_nick(self, c, event):
        self.channel.setnick(event.source.nick, event.target)
        print(self.channel)

    def on_part(self, c, event):
        self.channel.remove(event.source.nick)

    def on_quit(self, c, event):
        self.channel.remove(event.source.nick)

    def on_privmsg(self, c, event):
        print(event)

    def on_pubmsg(self, c, event):
        prefix = ";"
        msg = Message(
            message=event.arguments[0],
            user=self.channel.getuser(event.source.nick)
        )
        if msg.message.startswith(prefix):
            command = Command(prefix=prefix, data=msg)
            # TODO move these
            if command.name == "reload" or command.name == "load":
                if m := self.cm.import_module(command.message, self):
                    self.cm.add_cog(m, command.message, self)
                    self.sendmsg(f"{command.name}ed {command.message}")
                else:
                    self.sendmsg(f"failed to {command.name} {command.message}")
            elif command.name == "unload":
                if self.cm.unload(command.message):
                    self.sendmsg(f"unloaded {command.message}")
                else:
                    self.sendmsg(f"Could not unload {command.message}")
            elif command.name == "loaded":
                self.sendmsg(f"modules: {self.cm.modules}, cogs:{self.cm.cogs}")
            else:
                self.cm.do_command(command)
        return

    def gen_userlist(self):
        # maybe better management of users
        # probably shouldnt be here
        # TODO NickMask() and hold more user info
        channel = self.channels[self.channel.name]
        for user in channel.users():
            newuser = User(
                nick=user,
                isop=channel.is_oper(user),
                isowner=channel.is_owner(user),
                isvoiced=channel.is_voiced(user)
            )
            self.channel.users.append(newuser)


def main():
    # bot = Vicky('#main', 'vicky', 'localhost', 6667)
    bot = Vicky('#main', 'vicky', 'irc.0xfdb.xyz', 6667)
    bot.run()


if __name__ == "__main__":
    main()
