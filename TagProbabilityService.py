from collections import OrderedDict
from conllu.parser import parse, parse_tree, parse_line
import re
from Tag import Tag
from ConditionalProbabilityExpression import ConditionalProbabilityExpression


class TagProbabilityService:
    #P[tag|word]
    #Represeted as [ConditionalProbabilityExpression , probability value]
    #ConditionalProbabilityExpression is P[tag|word]
    prob_dict = OrderedDict()

    #Represented as [word , tag]
    word_tag_dict = OrderedDict()

    #Represented as [tag, word]
    tag_word_dict = OrderedDict()



    def explore_tree(self, tree):
        data_in_ordered_dict = tree.data
        word = data_in_ordered_dict['form']
        tag_detector = Tag.NOTEXIST
        tag = tag_detector.get_tag(data_in_ordered_dict['upostag'])

        expression_tag_word = ConditionalProbabilityExpression(tag,word)
        expression_word_tag = ConditionalProbabilityExpression(word,tag)

        if expression_word_tag in self.word_tag_dict.keys():
            value = self.word_tag_dict[expression_word_tag]
            value = value + 1
            self.word_tag_dict[expression_word_tag] = value
        else :
            self.word_tag_dict[expression_word_tag] = 1


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

tag = TagProbabilityService("UD_English/en-ud-dev.conllu")
print '==========='
for tag in word_tag_dict:
    if tag.values() > 5:
        print tag.values()
