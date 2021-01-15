# Sql Module (lib/sql.py)

import sqlite3

# Some sql functions
def list_from_db(database, query, tup):
    with sqlite3.connect(database) as conn:
        cur = conn.cursor()
        cur.execute(query, tup)
        return cur.fetchall()

def add_to_db(database, sqlcmd, tup):
    with sqlite3.connect(database) as conn:
        cur = conn.cursor()
        cur.execute(query, tup)
        conn.commit()

# Quotes

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
        print(parts)
        if len(parts) > 1:
            add_to_db(self.path, "insert into quotes values(?, ?, ?)", (madeby, parts[0], parts[1]))
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
        print(self.quotes)
        if self.quotes:
            thequote = choice(self.quotes)
            self.sendmsg(f"{thequote[2]} - {thequote[1]} | Added by {thequote[0]}")
        else:
            self.sendmsg(f"There are no quotes for {parts[0]}")
