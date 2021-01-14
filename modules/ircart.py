from pathlib import Path
import time

from lib.cog import Cog
from lib.command import Command, command


class ircart(Cog):
	def __init__(self, bot):
		super().__init__(bot)

	@command(aliases=["ircart", "art"], description="bangs out irc art")
	def run(self, c: Command):
		ircart_msg = c.message.split(" ")
		
		if ircart_msg[0] != '':
			artwork_path = "/home/alarm/vicky/files/ircart/" + ircart_msg[0] + ".txt"
			try:
				file1 = open(artwork_path, 'r')
			except IOError:
				self.sendmsg("Couldnt find file")
			Lines = file1.readlines() 
			count = 0
			for line in Lines: 
				self.sendmsg(line.strip('\n'))
		else:
			self.sendmsg("Couldn't find ircart directory.")
