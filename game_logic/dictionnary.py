from pprint import pprint

class Dictionnary(object):
	"""
		Store animal names using the first char as a key
		and a set of names as value.
	"""
	maindict = {}

	def __init__(self, file_path):
		self.load_names(file_path)

	def load_names(self, file_path):
		"""
			Loads animal names into maindict
			
			@input: str file_path
			@None: str file_path
		"""
		with open(file_path) as f:
			for line in f.readlines():
				line = line.lower()[:-1] # Remove \n
				first_char = line.strip()[0]

				# handle start char
				if not self.maindict.get(first_char):
					names_set = set()
					self.maindict[first_char] = names_set
				self.maindict[first_char].add(line)
	
	def print_dict(self):
		"""
			Prints the maindict content

			@input: None
			@output: None
		"""
		pprint(self.maindict)

	def is_valid_word(self, word):
		"""
			Does the word is in maindict ?

			@input: string word
			@output: bool validity
		"""
		if not len(self.maindict):
			return False

		word = word.lower()
		
		if word[0] in self.maindict.keys():
			if word in self.maindict[word[0]]:
				return True
		return False

	def clear(self):
		"""
			@input: None
			@output: None
		"""
		self.maindict.clear()

	def get_names(self, letter):
		"""
			Gets animal names for current letter

			@input: string letter
			@output: set animal_names
		"""
		names = set()
		if not letter in self.maindict.keys():
			return names
		
		return self.maindict[letter]

	def get_length(self):
		"""
			@input: None
			@output: int maindict_length
		"""
		return len(self.maindict)


if __name__ == "__main__":
	game_dict = Dictionnary("words.txt")

	""" Unitests """
	assert game_dict.get_length() != 0

	valid_animals = ["Laboratory rat strains", "Sheep breeds","Pigeon breeds"]
	for animal in valid_animals:
		assert game_dict.is_valid_word(animal) == True
	non_valid_animals = ["Laborezatory rat strains", "Sheezerp breeds","Pigerzeon breeds"]
	for animal in non_valid_animals:
		game_dict.is_valid_word(animal) == False


	v_names = {'vampire squid', 'vole', 'vicuna', 'viper', 'vampire bat', 'vulture'}
	assert game_dict.get_names("v") == v_names
