from __future__ import division
from collections import OrderedDict
from conllu.parser import parse, parse_tree, parse_line
from Tag import Tag
from ConditionalProbabilityExpression import ConditionalProbabilityExpression
import re
import pickle
import os.path

class TagProbabilityService:
    #Represeted as [ConditionalProbabilityExpression , probability value]
    #ConditionalProbabilityExpression is P[tag|word]
    tw_prob_dict = OrderedDict()
    #ConditionalProbabilityExpression is P[word\tag]
    wt_prob_dict = OrderedDict()
    #ConditionalProbabilityExpression is P[tag\tag-1,tag-2]
    #For first word in sentence:
    #   tag-1 = Tag.NOTEXIST
    #   tag-2 = Tag.NOTEXIST
    ttt_prob_dict = OrderedDict()


    #Represented as [word, count]
    word_dict = OrderedDict()
    #Represented as [tag|word, count]
    tag_word_dict = OrderedDict()
    #Represented as [tag, tag-1, tag-2]
    ttt_dict = OrderedDict()
    #Represented as [tag-1, tag-2]
    tt_dict = OrderedDict()
    #Represented as [tag]
    t_dict = OrderedDict()

    #File Path to save TagProbabilityService object
    tw_object_file_path = 'single_tag_probability_service.dat'
    wt_object_file_path = 'three_tag_probability_service.dat'
    ttt_object_file_path = 'three_tag_probability_service.dat'


    def __init__(self, file_path):
        if os.path.exists(self.tw_object_file_path) and os.path.exists(self.tw_object_file_path) and os.path.exists(self.ttt_object_file_path):
            self.read_external_file()
        else :
            corpus_file = open(file_path,'r')
            corpus_data = re.sub(r" +", r"\t",corpus_file.read())
            sentence_list = parse(corpus_data)

            i = 0
            for sentence in sentence_list:
                print i
                i = i + 1

                tag1 = Tag.NOTEXIST
                tag2 = Tag.NOTEXIST
                for token in sentence:

                    word = token['form']
                    tag_detector = Tag.NOTEXIST
                    tag = tag_detector.get_tag(token['upostag'])

                    self.update_word_dict(word)
                    self.update_tag_word_dict(str(tag)+'|'+word)

                    ttt_tag_key = str(tag) + '|' + str(tag1) + '|' + str(tag2)
                    tt_tag_key = str(tag1) + '|' + str(tag2)
                    self.update_ttt_dict(ttt_tag_key)
                    self.update_tt_dict(tt_tag_key)
                    self.update_t_dict(str(tag))

                    #update tag
                    tag2 = tag1
                    tag1 = tag

            self.count_tw_prob_dict()
            self.count_wt_prob_dict()
            self.count_ttt_prob_dict()
            self.write_external_file()


    def count_tw_prob_dict(self):
        for tag_word in self.tag_word_dict:
            tag, word = tag_word.split('|')
            self.tw_prob_dict[tag_word] = self.tag_word_dict[tag_word]/self.word_dict[word]

    def count_wt_prob_dict(self):
        for tag_word in self.tag_word_dict:
            tag, word = tag_word.split('|')
            cond = ConditionalProbabilityExpression()
            cond.set_two_param(word,tag)
            self.wt_prob_dict[cond.get_key()] = self.tag_word_dict[tag_word]/self.t_dict[tag]


    def count_ttt_prob_dict(self):
        for ttt in self.ttt_dict:
            tag, tag1, tag2 = ttt.split('|')
            cond = ConditionalProbabilityExpression()
            cond.set_three_param(tag, tag1, tag2)
            self.ttt_prob_dict[cond.get_key()] = self.ttt_dict[ttt]/self.tt_dict[tag1 + '|' + tag2];

    def get_tw_prob_dict(self):
        return self.tw_prob_dict

    def get_wt_prob_dict(self):
        return self.wt__probdict

    def get_ttt_prob_dict(self):
        return self.ttt_prob_dict;

    def update_ttt_dict(self, key):
        if key in self.ttt_dict:
            value = self.ttt_dict[key]
            self.ttt_dict[key] = value + 1
        else :
            self.ttt_dict[key] = 1

    def update_tt_dict(self, key):
        if key in self.tt_dict:
            value = self.tt_dict[key]
            self.tt_dict[key] = value + 1
        else:
            self.tt_dict[key] = 1

    def update_t_dict(self, key):
        if key in self.t_dict:
            value = self.t_dict[key]
            self.t_dict[key] = value + 1
        else:
            self.t_dict[key] = 1

    def update_word_dict(self, word):
        if word in self.word_dict.keys():
            value = self.word_dict[word]
            value = value + 1
            self.word_dict[word] = value
        else :
            self.word_dict[word] = 1

    def update_tag_word_dict(self, key):
        if key in self.tag_word_dict.keys():
            value = self.tag_word_dict[key]
            value = value + 1
            self.tag_word_dict[key] = value
        else :
            self.tag_word_dict[key] = 1

    def read_external_file(self):
        with open(self.tw_object_file_path, "rb") as f:
            dump = pickle.load(f)
            self.tw_prob_dict = dump

        with open(self.wt_object_file_path, "rb") as f:
            dump = pickle.load(f)
            self.wt_prob_dict = dump

        with open(self.ttt_object_file_path, "rb") as f:
            dump = pickle.load(f)
            self.ttt_prob_dict = dump

    def write_external_file(self):
        with open(self.tw_object_file_path, "wb") as f:
            pickle.dump(self.tw_prob_dict, f, pickle.HIGHEST_PROTOCOL)
        with open(self.wt_object_file_path, "wb") as f:
            pickle.dump(self.wt_prob_dict, f, pickle.HIGHEST_PROTOCOL)
        with open(self.ttt_object_file_path, "wb") as f:
            pickle.dump(self.ttt_prob_dict, f, pickle.HIGHEST_PROTOCOL)

tag = TagProbabilityService("UD_English/en-ud-test.conllu")
prob_dict = tag.get_tw_prob_dict()
#P(Tag.ADJ|rice)
# print prob_dict[str(Tag.NOUN) + '|' + 'meeting']
