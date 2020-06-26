from lib.cog import Cog
from lib.command import Command, command
import random

class Bofh(Cog):
	@command(aliases=["bofh", "excuse"], description="f0ur0nes excuse for why shit sucks in any particular instance")
	def run(self, c: Command):
		excuse_num = random.randint(1, 466)
		excuse_want = int()
		f = open("modules/excuses.txt", "r")
		for x in f:
			excuse_want = excuse_want + 1
			if excuse_want == excuse_num:
				self.sendmsg(x.strip("\n"))
				#print(x.strip("\n"))
				print(excuse_want)
