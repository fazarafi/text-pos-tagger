import nltk
from sentence_token import SentenceToken
from single_token import SingleToken
from random import randint

class SentenceClassifier(object):
	def __init__(self, available_tags=None, tokenized_sentence=None):
		self.available_tags = available_tags

	def tokenize_sentence(self, sentence):
		words = nltk.word_tokenize(sentence)
		print words
		tokenized_sentence = []
		for idx in range(len(words)):
			prev_word = ""
			next_word = ""
			if (idx==0):
				prev_word = "-"
			else:
				prev_word = words[idx-1]

			if (idx==(len(words)-1)):
				next_word = "-"
			else:
				next_word = words[idx+1]
			word = SingleToken(words[idx],prev_word,next_word)
			token = SentenceToken(word)
			tokenized_sentence.append(token)
		self.tokenized_sentence = tokenized_sentence

	def insert_candidates(self, word, candidates):
		for token in self.tokenized_sentence:
			if (word == token.word.itself):
				token.set_candidates(candidates)
				break

	def choose_pos_tag(self):
		for token in self.tokenized_sentence:
			if (token.pos_tag_candidates != None):
				chosen = ""
				max_prob = -1
				for cand in token.pos_tag_candidates:
					prob = randint(0,9) #calc_prob(token.word.itself,cand)
					if (prob>max_prob):
						chosen = cand
						max_prob = prob
				token.pos_tag = SingleToken(chosen,None,None)

classifier = SentenceClassifier()
classifier.tokenize_sentence("Depending on what you plan to do with your sentence-as-a-list")
classifier.insert_candidates("on",["NNP","VB"])
classifier.choose_pos_tag()
for token in classifier.tokenized_sentence:
	print ">"
	print token.word.itself
	print token.pos_tag_candidates
	if (token.pos_tag!=None):
		print token.pos_tag.itself
	print ""

		

