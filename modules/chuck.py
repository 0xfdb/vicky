from lib.cog import Cog
from lib.command import Command, command
from lib.web import get


class Chuck(Cog):
    @command(aliases=["chuck", "norris", "cn", "chucknorris"], description="")
    def run(self, c: Command):
        req = get(url="https://api.chucknorris.io/jokes/random", json=True)
        if req.status == 200:
            self.sendmsg(req.data["value"])
