from pathlib import Path
from lib.cog import Cog
from lib.command import Command, command
from lib.sql import list_from_db, add_to_db 
from random import choice

class Quotes(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.path = Path.cwd() / self.settings["quotes_path"]
        # Plan to cache or something
        self.quotes = []

    # This is broken
    @command(aliases=["addquote", "newquote"], description="Records bad takes")
    def addquotes(self, c: Command):
        madeby = c.user.nick
        parts = c.message.split(" ")
        quote = " "
        if len(parts) > 1:
            add_to_db(self.path, "insert into quotes values(?, ?, ?)", (madeby, parts[0], quote.join(parts[1:])))
            self.sendmsg("Quote added!")
        else:
            self.sendmsg("Forgot some arguments baka")

    # This works for the most part
    @command(aliases=["quote"], description="Prints a saved quote")
    def printquote(self, c: Command):
        parts = c.message.split(" ")
        # Quote a person
        self.quotes = list_from_db(self.path, "select * from quotes where name = (?)", (parts[0],))
        # A specific 
        # self.quotes = list_from_db(self.path, "select * from quotes where rowid = (?)", (parts[0],))
        # Quote all - need to change the lib/sql.py
        # self.quotes = list_from_db(self.path, "select * from quotes")
        if self.quotes:
            thequote = choice(self.quotes)
            self.sendmsg(f"{thequote[2]} - {thequote[1]} | Added by {thequote[0]}")
        else:
            self.sendmsg(f"There are no quotes for {parts[0]}")

    @command(aliases=["delquote"], description="Deletes a quote")
    def delquote(self, c: Command):
        if c.user.isop:
            add_to_db(self.path, "delete from quotes where rowid = (?)", (c.message.split(" ")[0]))
        else:
            self.sendmsg("You need to be an op to delete a quote")
