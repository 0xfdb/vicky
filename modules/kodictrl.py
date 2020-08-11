from lib.cog import Cog
from lib.command import Command, command
from kodipydent import Kodi
import json
from lib.paste import pastebin

my_kodi = Kodi('192.168.1.123')
def get_activeplayer(): my_kodi.Player.GetActivePlayers()
def get_movies(): my_kodi.VideoLibrary.GetMovies()
def ctrl_play_pause(): my_kodi.Player.PlayPause(1)
def ctrl_play_item(): my_kodi.Player.Open()
def ctrl_stop_item(): my_kodi.Player.Stop(1)

class kodictrl(Cog):
	@command(aliases=['kodictrl'], description='abc')
	def ctrl_kodi(self, c: Command):
		kodi_msg = c.message.split(" ")											#commands
		nick = c.data.user.nick
		isop = c.data.user.isop
		isowner = c.data.user.isowner
		nick_allowed = False
		if isop == True or isowner == True:
			nick_allowed = True
		print(kodi_msg)
		if kodi_msg[0] == 'playpause' and nick_allowed == True:												#play/pause
			ctrl_play_pause()
			self.sendmsg("Play/Pause")
		elif kodi_msg[0] == 'play' and nick_allowed == True:													#play movie
			movie_name = kodi_msg[:0]+kodi_msg[0+1:]
			movie_name_search = ""
			print(movie_name)
			for i in range(len(movie_name)):
				movie_name_search += str(movie_name[i]).lower().replace('"', '')
			print(movie_name_search)
			self.sendmsg("now playing " + str(movie_name_search) + " with movie id " + str(movie_id(movie_name_search)))
			my_kodi.Player.Open(item={'movieid':movie_id(movie_name_search)})
		elif kodi_msg[0] == 'stop' and nick_allowed == True:													#stop
			ctrl_stop_item()
			self.sendmsg("Stopped Playback")
		elif kodi_msg[0] == 'list':													#list
			#movielistpaste = ""
			#self.sendmsg("Grabbing list...")
			#movielist_raw = my_kodi.VideoLibrary.GetMovies()
			#movielist = movielist_raw['result']['movies']
			#print(movielist)
			#for i in range(len(movielist)): 
			#	movielistpaste = (movielistpaste + movielist[i]['label'] + "\n")
			#self.sendmsg("Done grabbing and formating, sending to pastebin...")
			#self.sendmsg(str(pastebin(movielistpaste)).replace("com/", "com/raw/"))
			self.sendmsg("Movie List - https://kapi.0xfdb.xyz/movies")
			self.sendmsg("TV Show List - https://kapi.0xfdb.xyz/tvshows")
		elif kodi_msg[0] == 'playlist':												#playlist
			playlistmsg = ""
			if len(kodi_msg) >= 2:														#playlist sub commands
				if kodi_msg[1] == 'list': 												#playlist list
					playlist_raw = my_kodi.Playlist.GetItems(1)
					playlist = playlist_raw['result']['items']
					print("playlist is " + str(playlist))
					self.sendmsg("- playlist -")
					for i in range(len(playlist)):
						print("test " + str(i))
						self.sendmsg(str(i + 1) + ". " + playlist[i]['label'])
					self.sendmsg("- end of playlist -")
				elif kodi_msg[1] == 'add' and nick_allowed == True:						#playlist add
					if len(kodi_msg) >= 3:																#title
						movie_name = kodi_msg[:0]+kodi_msg[0+1:]
						movie_name = movie_name[:0]+movie_name[0+1:]
						movie_name_search = ""
						print(movie_name)
						for i in range(len(movie_name)):
							movie_name_search += str(movie_name[i]).lower().replace('"', '')
						self.sendmsg("lol we will try to add " + str(movie_name_search) + " to the playlist")
						my_kodi.Playlist.Add(1, item={'movieid':movie_id(movie_name_search)})
						self.sendmsg("check if that worked son")
					else:
						self.sendmsg("no item given")
				elif kodi_msg[1] == 'swap' and nick_allowed == True:					#playlist swap
					if len(kodi_msg) >= 3:
						item1 = int(kodi_msg[2]) - 1
						item2 = int(kodi_msg[3]) - 1
						self.sendmsg("swapping playlist item " + str(kodi_msg[2]) + " with " + str(kodi_msg[3]))
						my_kodi.Playlist.Swap(1, item1, item2)
					else:
						self.sendmsg("not enough arguments")
				elif kodi_msg[1] == 'remove' and nick_allowed == True:					#playlist remove
					if len(kodi_msg) >= 3:
						item_rem = int(kodi_msg[2]) - 1
						self.sendmsg("removing item " + kodi_msg[2] + " from playlist")
						my_kodi.Playlist.Remove(1, )
					else:
						send.sendmsg("no item given")
				else: self.sendmsg("i dont know that playlist command")
			else:
				self.sendmsg("requires more options")		
		elif kodi_msg[0] == 'help':												#help
			self.sendmsg("kodictrl - Vicky IRC bot module for controlling live stream for 0xfdb network")
			self.sendmsg("USAGE - ;kodictrl option [sub-option] title")
			self.sendmsg("Availible Options:")
			self.sendmsg("  list                    Posts list of availible titles")
			self.sendmsg("  play title              Plays given title")
			self.sendmsg("  playpause               Pauses/Plays title")
			self.sendmsg("  stop                    Stops title")
			self.sendmsg("  playlist                Playlist mgmt (requires the following sub-options)")
			self.sendmsg("           list           Lists Current Playlist")
			self.sendmsg("           add title      Adds additional title to playlist")
			self.sendmsg("           remove	x       Removes title from place in playlist (BROKEN)")
			self.sendmsg("           swap x y       Swaps 2 titles places in playlist (BROKEN)")
		elif nick_allowed == False:
			self.sendmsg( "" + nick + " does not have the required privileges for this command.")
		else:
			self.sendmsg("Command not recognized. Send ';kodictrl help' for a list of options.")

def movie_id(moviename):
	movieid = ""
	movielist_raw = my_kodi.VideoLibrary.GetMovies()
	movielist = movielist_raw['result']['movies']
	for i in range(len(movielist)):
		if str(movielist[i]['label']).lower().replace('"', '').replace(" ","") == moviename:
			movieid = movielist[i]['movieid']
			print("got")
			print(str(movielist[i]['label']).lower().replace('"', '').replace(" ",""))
	print("searched for")
	print(moviename)
	return movieid
