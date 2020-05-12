from bs4 import BeautifulSoup as bs4
from lib.cog import Cog
from lib.command import Command, command
from lib.web import get
from modules.imdb import get_imdb


class ZeroX(Cog):
    @command(aliases=["nowplaying", "np"], description="")
    def nowplaying(self, c: Command):
        if "music" in c.message:
            self.get_music()
        elif "tv" in c.message:
            self.get_tv()
        else:
            self.get_tv(short=True)
            self.get_music()

    def get_tv(self, short=False):
        req = get("https://0xfdb.xyz/nowplaying/test.html")
        soup = bs4(req.data, 'html.parser')
        title = soup.find(id="nowplaying").get_text().strip()
        info, overview = get_imdb(title)
        if info:
            self.sendmsg(f"Now Playing: {info}")
            if short:
                self.sendmsg(overview)
        else:
            self.sendmsg(title)

    def get_music(self):
        req = get("https://taro.0xfdb.xyz/radio.html")
        soup = bs4(req.data, 'html.parser')
        title = soup.find(id="NowPlaying").get_text().strip()
        self.sendmsg(title)
