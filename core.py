import os
import json
import shelve
import hashlib

import tmdbsimple as tmdb
from guessit import guessit
# from pythonopensubtitles.opensubtitles import OpenSubtitles
# from pythonopensubtitles.utils import File

from utils import File

with open('credentials.json', 'r') as f:
	creds = json.load(f)

EMAIL = creds['opensubtitles']['email']
PASSWORD = creds['opensubtitles']['password']
TMDB_APIKEY = creds['tmdb']['APIKey']

class Media:
	def __init__(self, path):
		if not os.path.isfile(path):
			raise Exception

		self.path = path
		self.abspath = os.path.abspath(path)
		self.filename = os.path.basename(path)
		self.info = {}

		self.parse_filename(self, self.filename)
		self.media_type = self.get_mediatype()

	def parse_filename(self, filename, type=None, title=None):
		options = {
		'--type': type,
		'--title': title,
		}
		self.info.update(guessit(self.filename, options))

	def edit_info(self, infodict):
		self.info.update(infodict)

	def get_mediatype(self):
		vid_containers = ['3g2', 'wmv', 'webm', 'mp4', 'avi', 'mp4a', 'mpeg', 'mka', 'm4v', 'ts', 'mkv', 'ra', 'rm', 'wma', 'ass', 'mpg', 'ram', '3gp', 'ogv', 'mov', 'ogm', 'asf', 'divx', 'ogg', 'ssa', 'qt', 'idx', 'nfo', 'wav', 'flv', '3gp2', 'iso', 'mk2']
		sub_containers = ['sub', 'srt']



		file_extension = os.path.splitext(self.filename)[1][1:]
		if file_extension in vid_containers:
			return 'vid'
		elif file_extension in sub_containers:
			return 'sub'


class Proliflicks:
	def __init__(self, shelf):
		self.shelf = shelf

	def add_directory(self, directory):
		medias = self.scan_directory(directory)
		for media in medias:
			self.update_shelf(media)

	def update_shelf(self, media):
		hash = self.get_hash(media.abspath)
		shelf[hash] = media

	def scan_directory(self, directory):
		media_containers = ['3g2', 'wmv', 'webm', 'mp4', 'avi', 'mp4a', 'mpeg', 'mka', 'm4v', 'ts', 'mkv', 'ra', 'rm', 'wma', 'ass', 'mpg', 'ram', '3gp', 'ogv', 'mov', 'ogm', 'asf', 'divx', 'ogg', 'ssa', 'qt', 'idx', 'nfo', 'wav', 'flv', '3gp2', 'iso', 'mk2', 'sub', 'srt']	
		files = []
		for (dirpath, dirnames, filenames) in os.walk(directory):
			for file in filenames:
				if (os.path.splitext(file)[1][1:] in media_containers):
					files.append(os.path.join(dirpath, file))

		medias = []
		for file in files:
			media = Media(file)
			medias.append(media)

		return medias

	def fetch_subtitles(self, media):
		os = OpenSubtitles()

		token = os.login(EMAIL, PASSWORD)
		if not type(token) == str:
			raise Exception('[*] Bad OpenSubtitles credentials!')

		f = File(media.abspath)
		hash = f.get_hash()
		size = f.size()

		data = os.search_subtitles([{'sublanguageid': 'all', 'moviehash': hash, 'moviebytesize': size}])
		return data

	def get_hash(self, file_path):
	    '''Return the md5 hash of a file.
	    '''

	    file = File(file_path)
	    hash = file.get_hash()
	    return hash

	    # with open(file_path, 'rb') as file:
	    # 	hash = hashlib.md5(file.read()).hexdigest()
	    # return hash



with shelve.open('spam') as shelf:
	pf = Proliflicks(shelf)
	pf.add_directory("E:\Movies")

	for (key, data) in shelf.items():
		print(key, ': ', data.info['title'])