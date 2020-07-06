import re

from irc.client import Event

from lib.cog import Cog, event
from lib.command import Command, command
from lib.objects import Events
from lib.web import Web, get


class Youtube(Cog):
    @event(Events.PubMsg)
    def youtube(self, event: Event):
        # TODO store videoid's in db
        if re.search("youtu(be\.com|\.be)", event.arguments[0]):
            ytid = re.search("(?:v=|\.be\/)(.{11})", event.arguments[0])[1]
            info = self.lookup(ytid)
            if len(info) != 0:
                self.sendmsg(
                    "[ {} — {} ({}) ] - youtu.be".format(
                        info["title"], info["channel"], info["duration"]
                    )
                )

    def lookup(self, videoid: str) -> dict:
        searchurl = (
            "https://www.googleapis.com/youtube/v3/videos?"
            "part=contentDetails,snippet&id={vid}&fields="
            "items(contentDetails%2Fduration%2Csnippet(channelTitle%2Ctitle))"
            "&key={key}"
        )
        url = searchurl.format(vid=videoid, key=self.settings["api_key"])
        ytjson = get(url, json=True)
        if ytjson.data.get("error", False):
            return {}
        # videoid = ytjson.data["items"][0]["id"]["videoId"]
        title = ytjson.data["items"][0]["snippet"]["title"]
        channel = ytjson.data["items"][0]["snippet"]["channelTitle"]
        _duration = ytjson.data["items"][0]["contentDetails"]["duration"]
        duration = _duration.lstrip("PT").lower()
        return {"title": title, "channel": channel, "duration": duration}
