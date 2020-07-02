import random

from lib.cog import Cog
from lib.command import Command, command
from lib.web import Web, get


class Food(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.api_key = self.settings["api_key"]

    @command(aliases=["food", "recipe"], description="")
    def food(self, c: Command):
        if len(self.api_key) == 0:
            self.sendmsg("Missing API key Modules.Food.api_key")
        else:
            response = self.get_food2fork(c.message)
            self.sendmsg(response)

    def get_food2fork(self, search: str) -> str:
        url = "https://food2fork.com/api/search?key={}&q={}".format(self.api_key ,search)
        request = get(url, json=True)
        if request.status_code == 200:
            try:
                total = len(request["recipes"])
                num = random.randint(0, total)
                msg = "{} {} ({}/{})".format(
                    request["recipes"][num]["title"],
                    request["recipes"][num]["f2f_url"],
                    num, total)
            except (IndexError, KeyError) as error:
                msg = error
            return msg
