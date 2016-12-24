import os
from guessit import guessit


class Media:
	def __init__(self, path):
		if not os.path.isfile(path):
			raise Exception

		self.path = path
		self.abspath = os.path.abspath(path)
		self.filename = os.path.basename(path)
		self.info = {}

		self.parse_filename(self, self.filename)

	def parse_filename(self, filename, type=None, title=None):
		options = {
		'--type': type,
		'--title': title,
		}
		self.info.update(guessit(self.filename, options))

	def edit_info(self, infodict):
		self.info.update(infodict)

def scan_directory(directory):
	media_containers = ['3g2', 'wmv', 'webm', 'mp4', 'avi', 'mp4a', 'mpeg', 'sub', 'mka', 'm4v', 'ts', 'mkv', 'ra', 'rm', 'wma', 'ass', 'mpg', 'ram', '3gp', 'ogv', 'mov', 'ogm', 'asf', 'divx', 'ogg', 'ssa', 'qt', 'idx', 'nfo', 'wav', 'flv', '3gp2', 'iso', 'mk2', 'srt']
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