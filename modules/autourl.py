import re

from bs4 import BeautifulSoup as bs4

from lib.cog import Cog, event
from lib.web import get


class AutoURL(Cog):
    @event("pubmsg")
    def run(self, event):
        # TODO refactor!
        msg = " ".join(event.arguments)
        if "http" in msg:
            try:
                urlexpression = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
                possible = re.findall(urlexpression, msg)
                req = get(possible[0], allow_redirects=True, timeout=15)
                domain = re.findall("https?:\/\/(.+?)\/", req.url)
                if req.status == 200:
                    soup = bs4(req.data, "html.parser")
                    if soup is not None:
                        try:
                            title = soup.title.string
                        except AttributeError as error:
                            pass
                        else:
                            self.sendmsg("[ {} ] - {}".format(title.strip(), domain[0]))
            except:
                pass
