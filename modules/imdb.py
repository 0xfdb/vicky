from lib.cog import Cog
from lib.command import Command, command
from lib.web import Web, get


class Imdb(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.api_key = self.settings["api_key"]

    @command(aliases=["imdb", "movie"], description="")
    def movie(self, c: Command):
        print("RAN")
        if len(self.api_key) == 0:
            self.sendmsg("Missing API key in config.toml -> Modules.Imdb api_key")
        else:
            response, overview = get_imdb(c.message, self.api_key)
            if response is not None:
                self.sendmsg(response)
                self.sendmsg(overview)
            else:
                self.sendmsg("Couldn't find that")


# These are exposed outside of the Cog so other things can use
# kinda gross, maybe revise a way to hanlde this
# EHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
def get_imdb(title, api_key):
    search_url = (
        "https://api.themoviedb.org/3/search/multi?api_key={apikey}&query={query}"
    )
    id_url = "https://api.themoviedb.org/3/{media_type}/{id}?api_key="
    search = get(search_url.format(apikey=api_key, query=title), json=True)
    if search.data is None or "results" not in search.data:
        return None, None
    if len(search.data["results"]) == 0:
        return None, None
    else:
        info = get(id_url.format(**search.data["results"][0]) + api_key, json=True)
        if search.data["results"][0]["media_type"] == "movie":
            response, overview = formatresponse(info.data, is_movie=True)
            return response, overview
        else:
            response, overview = formatresponse(info.data, is_movie=False)


def formatresponse(info, is_movie):
    if is_movie:
        response = """🍿 {title} ({original_title}) [{release_date}] {vote_average} — https://imdb.com/title/{imdb_id}""".format(
            **info
        )
    else:
        response = """🍿 {original_name} ({first_air_date} Rating: {vote_average}) Episodes: {episode_run_time[0]}""".format(
            **info
        )
    return response, info["overview"]
