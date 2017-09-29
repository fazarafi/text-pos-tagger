from collections import OrderedDict
from conllu.parser import parse, parse_tree, parse_line
from Tag import Tag
from ConditionalProbabilityExpression import ConditionalProbabilityExpression
import re
import pickle
import os.path

class TagProbabilityService:
    #P[tag|word]
    #Represeted as [ConditionalProbabilityExpression , probability value]
    #ConditionalProbabilityExpression is P[tag|word]
    prob_dict = OrderedDict()

    #Represented as [word, count]
    word_dict = OrderedDict()

    #Represented as [tag|word, count]
    tag_word_dict = OrderedDict()

    #File Path to save TagProbabilityService object
    object_file_path = 'tag_probability_service.dat'


    def __init__(self, file_path):
        if os.path.exists(self.object_file_path):
            with open(self.object_file_path, "rb") as f:
                dump = pickle.load(f)
                self.prob_dict = dump
                
                cond = ConditionalProbabilityExpression(self.prob_dict.keys()[0].get_first(),self.prob_dict.keys()[0].get_second())
                print self.prob_dict[cond]

        else :
            corpus_file = open(file_path,'r')
            corpus_data = re.sub(r" +", r"\t",corpus_file.read())
            sentence_list = parse(corpus_data)

            i = 0
            for sentence in sentence_list:
                print i
                i = i + 1
                for token in sentence:

                    word = token['form']
                    tag_detector = Tag.NOTEXIST
                    tag = tag_detector.get_tag(token['upostag'])

                    expression_tag_word = ConditionalProbabilityExpression(tag,word)

                    if word in self.word_dict.keys():
                        value = self.word_dict[word]
                        value = value + 1
                        self.word_dict[word] = value
                    else :
                        self.word_dict[word] = 1


                    if expression_tag_word in self.tag_word_dict.keys():
                        value = self.tag_word_dict[expression_tag_word]
                        value = value + 1
                        self.tag_word_dict[expression_tag_word] = value
                    else :
                        self.tag_word_dict[expression_tag_word] = 1

            self.count_prob_tag_word()
            with open(self.object_file_path, "wb") as f:
                pickle.dump(self.prob_dict, f, pickle.HIGHEST_PROTOCOL)

            for t in self.prob_dict:
                print t


    def count_prob_tag_word(self):
        for tag_word in self.tag_word_dict:
            self.prob_dict[tag_word] = self.tag_word_dict[tag_word]/self.word_dict[tag_word.get_second()]

    def get_prob_dict(self):
        return self.prob_dict

    def get_tag_word_dict(self):
        return self.tag_word_dict

tag = TagProbabilityService("UD_English/en-ud-test.conllu")
print '==========='
#for t in tag.get_prob_dict():
    #print t.get_second()
