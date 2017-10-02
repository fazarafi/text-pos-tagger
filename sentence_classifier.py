import nltk
from sentence_token import SentenceToken
from random import randint
# from TagProbabilityService import TagProbabilityService
from Tag import Tag
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from sklearn.feature_extraction import DictVectorizer
import numpy as np
from conllu.parser import parse, parse_tree, parse_line

import re

class SentenceClassifier(object):
	train_file_path = "UD_English/en-ud-test.conllu"
		
	def __init__(self, available_tags=None, tokenized_sentence=None, dataset=None, dataset_class=None):
		self.available_tags = available_tags

	def tokenize_sentence(self, sentence):
		words = nltk.word_tokenize(sentence)
		print words
		tokenized_sentence = []
		for word in words:
			token = SentenceToken(word)
			tokenized_sentence.append(token)

		self.tokenized_sentence = tokenized_sentence

	
	def preprocess_data(self):
		sentence_list = self.read_external_file("UD_English/en-ud-test.conllu")
		dataset = []
		dataset_class = []
		feature_names = ['word', 'prev_tag', 'next_tag', 'tag_class']
		all_classes = ["ADJ","ADP","ADV","AUX","CCONJ","DET","INTJ","NOUN","NUM","PART","PRON","PROPN","PUNCT","SCONJ","SYM","VERB","X"]
		prev_tag = ''
		row_id = 0
		for sentence in sentence_list:
			for token in sentence:
				word = str.lower(token['form'])
				tag = token['upostag']
				dataset_class.append(tag)
				dataset.append([word,prev_tag,''])
				if (row_id!=0):
					dataset[row_id-1][2] = tag				
				prev_tag = tag
				row_id += 1
		print dataset[0][0]+" = "+dataset_class[0]
		print dataset[1][0]+" = "+dataset_class[1]
		print dataset[2][0]+" = "+dataset_class[2]
		print dataset[3][0]+" = "+dataset_class[3]
		print dataset[4][0]+" = "+dataset_class[4]
		self.dataset = dataset
		self.dataset_class = dataset_class
		le = preprocessing.LabelEncoder()
		

	def vectorize(self):
		v = DictVectorizer(sparse=False)

	def read_external_file(self, file_path):
		corpus_file = open(file_path,'r')
		corpus_data = re.sub(r" +", r"\t",corpus_file.read())
		sentence_list = parse(corpus_data)
		return sentence_list

	

sc = SentenceClassifier()
sc.preprocess_data()

# def insert_candidates(self, word, candidates):
# 		for token in self.tokenized_sentence:
# 			if (word == token.word):
# 				token.set_candidates(candidates)
# 				break

# 	def choose_pos_tag(self, tag_array, prob_dict):
# 		for token in self.tokenized_sentence:
# 			print "====================="
# 			print token.word
# 			for pos in tag_array:
# 				print token.word+" -> "+str(pos)
# 				print prob_dict[str(pos) + '|' + token.word]


	# classifier.insert_candidates(token.word,["NNP","VB"])

# classifier.choose_pos_tag()
# for token in classifier.tokenized_sentence:
# 	print ">"
# 	print token.word
# 	print token.pos_tag_candidates
# 	print token.pos_tag
# 	print ""

# def choose_pos_tag(self):
# 	for idx in range(len(self.tokenized_sentence)):
# 		token = self.tokenized_sentence[idx]
# 		t_1_pos_tag = ""
# 		t_2_pos_tag = ""
# 		if (token.pos_tag_candidates != None):
# 			chosen = ""
# 			max_prob = -1
# 			if (idx!=0):
# 				t_1_pos_tag = self.tokenized_sentence[idx-1].pos_tag
# 			if (idx>1):
# 				t_2_pos_tag = self.tokenized_sentence[idx-2].pos_tag
# 			for cand in token.pos_tag_candidates:
# 				prob = randint(0,9) #calc_prob(token.word.itself,cand)
# 				if (prob>max_prob):
# 					chosen = cand
# 					max_prob = prob
# 			token.pos_tag = chosen
	