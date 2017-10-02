import nltk
from sentence_token import SentenceToken
from random import randint
from TagProbabilityService import TagProbabilityService
from Tag import Tag

class SentenceClassifier(object):
	def __init__(self, available_tags=None, tokenized_sentence=None):
		self.available_tags = available_tags

	def tokenize_sentence(self, sentence):
		words = nltk.word_tokenize(sentence)
		print words
		tokenized_sentence = []
		for word in words:
			token = SentenceToken(word)
			tokenized_sentence.append(token)
			
		self.tokenized_sentence = tokenized_sentence

	def insert_candidates(self, word, candidates):
		for token in self.tokenized_sentence:
			if (word == token.word):
				token.set_candidates(candidates)
				break

	def choose_pos_tag(self):
		for idx in range(len(self.tokenized_sentence)):
			token = self.tokenized_sentence[idx]
			t_1_pos_tag = ""
			t_2_pos_tag = ""
			if (token.pos_tag_candidates != None):
				chosen = ""
				max_prob = -1
				if (idx!=0):
					t_1_pos_tag = self.tokenized_sentence[idx-1].pos_tag
				if (idx>1):
					t_2_pos_tag = self.tokenized_sentence[idx-2].pos_tag
				for cand in token.pos_tag_candidates:
					prob = randint(0,9) #calc_prob(token.word.itself,cand)
					if (prob>max_prob):
						chosen = cand
						max_prob = prob
				token.pos_tag = chosen

tag = TagProbabilityService("UD_English/en-ud-test.conllu")
prob_dict = tag.get_tw_prob_dict()
#P(Tag.ADJ|rice)
print prob_dict[str(Tag.NOUN) + '|' + 'meeting']

ttt_dict = tag.get_ttt_prob_dict()
print ttt_dict[str(Tag.VERB)+"|"+str(Tag.NOUN)+","+str(Tag.NOUN)]

classifier = SentenceClassifier()
classifier.tokenize_sentence("Depending on what you plan to do with your sentence-as-a-list")
for token in classifier.tokenized_sentence:
	print token.word
	classifier.insert_candidates(token.word,["NNP","VB"])

classifier.choose_pos_tag()
for token in classifier.tokenized_sentence:
	print ">"
	print token.word
	print token.pos_tag_candidates
	print token.pos_tag
	print ""

		

