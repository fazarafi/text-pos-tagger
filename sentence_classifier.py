import nltk
from sentence_token import SentenceToken
from random import randint
from conllu.parser import parse, parse_tree, parse_line
import time

from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier

# import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline 
import re

class SentenceClassifier(object):
	train_file_path = "UD_English/en-ud-train.conllu"
	test_file_path = "UD_English/en-ud-test.conllu"

	def __init__(self, available_tags=None, tokenized_sentence=None, dataset=None, target=None, my_clf=None):
		self.available_tags = available_tags
		self.dataset = dataset
		self.target = target
		self.my_clf = my_clf
	

	def preprocess_training_data(self):
		sentence_list = self.read_external_file("UD_English/en-ud-train.conllu")
		dataset = []
		target = []
		prev_tag = ''
		prev_word = ''
		next_tag = ''
		next_word = ''
		row_id = 0
		for sentence in sentence_list:
			word_id = 0
			for token in sentence:
				word = str.lower(token['form'])
				tag = token['upostag']
				target.append(tag)
				dataset.append({'word': word, 'prev_word': prev_word, 'next_word': next_word,'prev_tag': prev_tag, 'next_tag': '', 'is_numeric': word.isdigit()})
				if (row_id!=0):
					dataset[row_id-1]['next_word'] = word
					dataset[row_id-1]['next_tag'] = tag				
				prev_tag = tag
				prev_word = word
				row_id += 1
				word_id+= 1

		self.dataset = dataset
		self.target = target
	
	def preprocess_testing_data(self):
		sentence_list = self.read_external_file("UD_English/en-ud-test.conllu")
		dataset = []
		target = []
		prev_tag = ''
		prev_word = ''
		next_tag = ''
		next_word = ''
		row_id = 0
		for sentence in sentence_list:
			word_id = 0
			for token in sentence:
				word = str.lower(token['form'])
				tag = token['upostag']
				target.append(tag)
				dataset.append({'word': word, 'prev_word': prev_word, 'next_word': next_word,'prev_tag': prev_tag, 'next_tag': '', 'is_numeric': word.isdigit()})
				if (row_id!=0):
					dataset[row_id-1]['next_word'] = word
					dataset[row_id-1]['next_tag'] = tag				
				prev_tag = tag
				prev_word = word
				row_id += 1
				word_id+= 1
		return dataset, target
	
	def train_eval_data(self, algo_name):
		print ""
		test_data, test_target = self.preprocess_testing_data()
		start_time = time.time()
		if (algo_name == "GNB"):
			print "Gaussian Naive Bayes"
			self.my_clf = Pipeline([
			    ('vectorizer', DictVectorizer(sparse=False)),
			    ('classifier', GaussianNB())
			])
			
		elif (algo_name == "RFC"):
			print "Random Forest Classifier"
			self.my_clf = Pipeline([
			    ('vectorizer', DictVectorizer(sparse=False)),
			    ('classifier', RandomForestClassifier(max_depth=2, random_state=0))
			])
			
		elif (algo_name == "DTL"):
			print "Decision Tree"
			self.my_clf = Pipeline([
			    ('vectorizer', DictVectorizer(sparse=False)),
			    ('classifier', DecisionTreeClassifier(criterion='entropy'))
			])
			
		elif (algo_name == "MLP"):
			print "Multi-Layer-Perceptron"
			self.my_clf = Pipeline([
			    ('vectorizer', DictVectorizer(sparse=False)),
			    ('classifier', MLPClassifier(solver='lbfgs', alpha=1e-5,
                     hidden_layer_sizes=(5, 2), random_state=1))
			])
				
		self.my_clf.fit(self.dataset, self.target)
		elapsed_time = time.time() - start_time
		print "Time lapsed: ", float("{0:.2f}".format(elapsed_time))," s"
		print "Accuracy:", float("{0:.2f}".format(100*self.my_clf.score(test_data, test_target)))," %"
		print "Determining POS of :\"I want to go to school at 5 PM.\""
		tokens = self.preprocess_new_sentence("I want to go to school at 5 PM.")
		for token in tokens:
			print token['word']+" -> "+self.my_clf.predict(token)[0]
		
	def preprocess_new_sentence(self, sentence):
		words = nltk.word_tokenize(sentence)
		tokens = []
		prev_tag = ''
		prev_word = ''
		next_tag = ''
		next_word = ''
		row_id = 0
		word_id = 0
		for word in words:
			word = str.lower(word)
			token = {'word': word, 'prev_word': prev_word, 'next_word': next_word, 'prev_tag': '', 'next_tag': next_tag, 'is_numeric': word.isdigit()}
			tokens.append(token)
			d = DictVectorizer(sparse=False)
			pred1_tag = ''#self.my_clf.predict(d.fit_transform(token))
			if (row_id!=0):
				tokens[row_id-1]['next_word'] = word
				tokens[row_id-1]['next_tag'] = pred1_tag

			prev_word = word
			prev_tag = pred1_tag
			row_id += 1
			word_id += 1
		return tokens
		# return zip(sentence, tags)

	def read_external_file(self, file_path):
		corpus_file = open(file_path,'r')
		corpus_data = re.sub(r" +", r"\t",corpus_file.read())
		sentence_list = parse(corpus_data)
		return sentence_list

sc = SentenceClassifier()
sc.preprocess_training_data()
# sc.train_eval_data("DTL")
sc.train_eval_data("RFC")
sc.train_eval_data("GNB")
sc.train_eval_data("MLP")