class SingleToken:
	def __init__(self, itself=None, prev_token=None, next_token=None):
		self.itself = itself
		self.prev_token = prev_token
		self.next_token = next_token

	def set_itself(self, el):
		self.itself = el

	def set_prev(self, el):
		self.prev_token = el

	def set_next(self, el):
		self.next_token = el