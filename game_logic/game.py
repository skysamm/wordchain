from .dictionnary import Dictionnary
from .score import Score
from .utils import bcolors, warning, info, server_print
import random

DEBUG = False
FAST_ANSWER = 15 # in seconds
SCORING_FACTOR = 1.5

class Error(object):
	NOT_VALID = 1
	ALREADY_SEEN = 2

class Game(object):
	game_dict = None
	user_score = None
	previous_words = None
	last_word = None
	has_started = 0
	user_score = 0
	server_score = 0

	def __init__(self, path):
		self.game_dict = Dictionnary(path)
		self.scorer = Score() 
		self.previous_words = set()

	def next(self, player_input, timing=1.0):
		"""
		@input: string new_player_input
				float  timing 
		@output:
				(animal_name, error_flag)
		"""
		error_flag = 0
		player_input = player_input.lower()

		# Handle starting
		if not self.has_started:
			if self.game_dict.is_valid_word(player_input):
				next_server_move = self.get_best_word(player_input[-1])
				self.last_word = next_server_move[1]
				self.server_score += next_server_move[0]

				#Save the player input
				self.previous_words.add(player_input)
				self.has_started = True
			else:
				error_flag = Error.NOT_VALID
				warning("Not valid word  _ first step")
		else:
			# Check validity of input
			if self.last_word and player_input[0] == self.last_word[-1] \
			                  and self.game_dict.is_valid_word(player_input):
				
				if not player_input in self.previous_words:
					
					current_score = self.scorer.check_score(player_input)
					self.user_score += current_score * timing

					#self.compute_server_logic(player_input[-1])
					next_server_move = self.get_best_word(player_input[-1])
					self.last_word = next_server_move[1]
					self.server_score += next_server_move[0]

					#Save the player input
					self.previous_words.add(player_input)

				else:
					error_flag = Error.ALREADY_SEEN
					warning("Already seen the word ! Please use another word.")
			else:
				error_flag = Error.NOT_VALID
				warning("Not a valid word _ nth steps")
		
		server_print("Server plays : " + str(self.last_word))
		info(f"Current scores: user has {self.user_score} and server has : {self.server_score}")
		
		self.previous_words.add(self.last_word)
		
		return (self.last_word, error_flag)

	def end(self):
		"""
			Clear the dic
		"""
		self.game_dict.clear()

	def get_best_word(self, letter):
		"""
		@TODO: May need optimization here
			@input: str   letter
			@ouput: tuple (best_score, best_word)
		"""
		best_score = 0
		best_word = ""
		for word in self.game_dict.get_names(letter):
			word_score = self.scorer.check_score(word)
			if word_score > best_score and not word in self.previous_words:
				best_score = word_score
				best_word  = word
		return (best_score, best_word)

	def check_timing(self, time_in_sec):
		"""
			@input: int   time_in_sec 
			@ouput: float scoring_factor
		"""
		if time_in_sec < FAST_ANSWER:
			return SCORING_FACTOR
		else:
			return 1

def main():
	game_inst = Game("words.txt")
	try:
		game_inst.run()
	except KeyboardInterrupt:
		game_inst.end()
		print("Game is finished")


if __name__ == "__main__":
	if DEBUG:
		game_inst = Game("words.txt")
		assert game_inst.get_best_word('w') == (25, "water buffalo breeds")
	else:
		main()
