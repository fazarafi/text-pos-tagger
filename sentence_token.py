class SentenceToken:
	def __init__(self, word, pos_tag_candidates=None, pos_tag=None):
		self.word = word
		self.pos_tag = pos_tag
		self.pos_tag_candidates = pos_tag_candidates
		
	def set_pos_tag(self, pos_tag):
		self.pos_tag = pos_tag

	def set_candidates(self, pos_tag_candidates):
		self.pos_tag_candidates = pos_tag_candidates