from lib.cog import Cog
from lib.command import Command, command
from lib.web import get


class Kanye(Cog):
    @command(aliases=["kanye"], description="")
    def run(self, c: Command):
        req = get(url="https://api.kanye.rest/", json=True)
        if req.status == 200:
            self.sendmsg(req.data["quote"])
