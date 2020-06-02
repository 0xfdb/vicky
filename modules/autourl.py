import re

from bs4 import BeautifulSoup as bs4
from irc.client import Event

from lib.cog import Cog, event
from lib.objects import Events
from lib.web import get


class AutoURL(Cog):
    @event(Events.PubMsg)
    def run(self, event: Event):
        msg = event.arguments[0]
        if "http" in msg:
            if title := self.autourl(msg):
                self.sendmsg(title)

    def autourl(self, msg: str):
        urlexpression = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        possible = re.findall(urlexpression, msg)
        req = get(possible[0], allow_redirects=True, timeout=10)
        domain = re.findall("https?:\/\/(.+?)\/", req.url)[0]
        if req.status == 200:
            if soup := bs4(req.data, "html.parser"):
                try:
                    title = soup.title.string.strip()
                except AttributeError as error:
                    return None
                else:
                    return "[ {} ] - {}".format(title, domain)
