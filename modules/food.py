import random

from lib.cog import Cog
from lib.command import Command, command
from lib.web import Web, get


class Food(Cog):

    @command(aliases=["food", "recipe"], description="")
    def food(self, c: Command):
        if len(c.message) >= 4:
            response = self.get_food2fork(c.message)
            self.sendmsg(response)
        else:
            self.sendmsg("Query is too short!")

    def get_food2fork(self, search: str) -> str:
        url = "https://forkify-api.herokuapp.com/api/search?q=" + search
        request = get(url, json=True)
        if request.status_code == 200:
            try:
                total = len(request.data)
                num = random.randint(0, total)
                msg = "({}/{}) {} {}".format(
                    num, total,
                    request.data[num]["title"],
                    request.data[num]["source_url"])
            except (IndexError, KeyError) as error:
                msg = error
            return msg
