from collections import OrderedDict
from conllu.parser import parse, parse_tree, parse_line
import re
import pickle
from Tag import Tag
from ConditionalProbabilityExpression import ConditionalProbabilityExpression


class TagProbabilityService:
    #P[tag|word]
    #Represeted as [ConditionalProbabilityExpression , probability value]
    #ConditionalProbabilityExpression is P[tag|word]
    prob_dict = OrderedDict()

    #Represented as [word, count]
    word_dict = OrderedDict()

    #Represented as [tag|word, count]
    tag_word_dict = OrderedDict()



    def explore_tree(self, tree):
        data_in_ordered_dict = tree.data
        word = data_in_ordered_dict['form']
        tag_detector = Tag.NOTEXIST
        tag = tag_detector.get_tag(data_in_ordered_dict['upostag'])

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

        for node in tree.children:
            self.explore_tree(node)

    def __init__(self, file_path):
        corpus_file = open(file_path,'r')
        corpus_data = re.sub(r" +", r"\t",corpus_file.read())
        sentence_list = parse_tree(corpus_data)

        i = 0
        for sentence in sentence_list:
            #print sentence.data
            print i
            i = i + 1
            self.explore_tree(sentence)

    def count_prob_tag_word(self):
        for tag_word in tag_word_dict:
            prob_dict[tag_word] = tag_word_dict[tag_word]/word_dict[tag_word.second]

    def prob_dict(self):
        return prob_dict;

tag = TagProbabilityService("UD_English/en-ud-dev.conllu")
print '==========='
for tag in word_tag_dict:
    if tag.values() > 5:
        print tag.values()
