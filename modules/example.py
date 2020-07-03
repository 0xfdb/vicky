from irc.client import Event, NickMask

from lib.cog import Cog, event
from lib.command import Command, command
from lib.objects import Events


class Example(Cog):
    @command(aliases=["test", "testing", "foobar"], description="abc")
    def test(self, c: Command):
        self.sendmsg("Test reload")

    @command(aliases=["echo"])
    def echo(self, c: Command):
        self.sendmsg("{} says {}".format(c.user.nick, c.message))

    @event(Events.Join)
    def joined(self, event: Event):
        # TODO shouldn't have to bother with NickMask
        u = NickMask(event.source)
        # TODO easier way to get own info
        if u.nick == self.bot.connection.nick:
            self.sendmsg(
                "Vicky Vicky Vicky, can't you see. Sometimes your joins just hypnotize me."
            )
