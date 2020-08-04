import random
from pathlib import Path

from lib.cog import Cog
from lib.command import Command, command


class Bofh(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.path = Path.cwd() / self.settings["excuse_path"]

    @command(
        aliases=["bofh", "excuse"],
        description="f0ur0nes excuse for why shit sucks in any particular instance",
    )
    def run(self, c: Command):
        if self.path.exists():
            excuses = self.path.read_text().split("\n")
            excuse = random.choice(excuses).strip()
            self.sendmsg(excuse)
        else:
            self.sendmsg("Couldn't find excuses file.")
