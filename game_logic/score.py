class Score(object):
	def __init__(self):
		return

	def check_score(self, word):
		"""
			@input: string word
			@output: int score
		"""
		if not len(word):
			return 0

		word = word.lower()
		current_score = 0
		for char in word:
			if char in "aeiouy":
				current_score += 2
			elif char.isalpha():
				current_score += 1
			else:
				continue
		return current_score

if __name__ == "__main__":
	Scorer = Score()

	assert Scorer.check_score("aaa") == 6
	assert Scorer.check_score("AaB") == 5
	assert Scorer.check_score("122") == 0
	assert Scorer.check_score("1AZAZaa") == 10
	assert Scorer.check_score("water buffalo breeds") == 25