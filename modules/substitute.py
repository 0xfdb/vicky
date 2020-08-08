from lib.cog import Cog, event
from lib.command import Command, command
from lib.objects import Events


class Substitute(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.previous_messages = {}

    def find_in_previous(self, nick: str, word: str):
        # TODO params should be msg obj
        for message in self.previous_messages[nick]:
            if word in message:
                return message

    def string_substitute(self, nick: str, msg: str):
        # TODO params should be msg obj
        parts = msg.split("/")
        old_msg = self.find_in_previous(nick, parts[1])
        if old_msg:
            if parts[-1] != "g":
                # replace first found word
                return old_msg.replace(parts[1], parts[2], 1)
            else:
                # replace all
                return old_msg.replace(parts[1], parts[2])

    def addmsg(self, nick: str, msg: str):
        # TODO params should be msg obj
        if nick in self.previous_messages.keys():
            self.previous_messages[nick].insert(0, msg)
            if len(self.previous_messages[nick]) > 5:
                self.previous_messages[nick].pop()
        else:
            self.previous_messages[nick] = [msg]

    @event(Events.Nick)
    def readnick(self, event: Events):
        nick = event.source.split("!")[0]
        if nick in self.previous_messages.keys():
            self.previous_messages[event.target] = self.previous_messages.pop(nick)

    @event(Events.PubMsg)
    def readmsg(self, event: Events):
        nick = event.source.split("!")[0]
        msg = event.arguments[0]
        if msg.startswith("s/"):
            try:
                replaced_str = self.string_substitute(nick, msg)
                if replaced_str is not None:
                    self.sendmsg(f"{nick} meant to say: {replaced_str}")
            except:
                pass
        # ignore commands
        elif msg[0] not in self.bot.bot_config["prefixes"]:
            self.addmsg(nick, msg)
