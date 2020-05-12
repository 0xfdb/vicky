from lib.cog import Cog
from lib.command import Command, command


class Example(Cog):
    @command(aliases=['test', 'testing', 'foobar'], description='abc')
    def test(self, c: Command):
        self.sendmsg("Test reload")
