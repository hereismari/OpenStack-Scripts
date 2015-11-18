import json

class JsonParser:
	
	def __init__(self, config_file_path):
	    self.config = self.loadJsonFile(config_file_path)

	def loadJsonFile(self, config_file_path):
            with open(config_file_path) as data_file:
			return json.load(data_file)

	def get(self, prop):
		try:
			return self.config[prop]
		except:
			print 'Failed to get property ' + prop
			return None
