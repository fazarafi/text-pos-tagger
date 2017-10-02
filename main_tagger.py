from ConditionalProbabilityExpression import ConditionalProbabilityExpression
from TagProbabilityService import TagProbabilityService
from sentence_classifier import SentenceClassifier
from sentence_token import SentenceToken
import re

class Main:

    test_file_path = "UD_English/en-ud-dev.conllu"
    train_file_path = "UD_English/en-ud-train.conllu"
    tw_prob_dict
    wt_prob_dict
    ttt_prob_dict

    def __init__(self):
        sentence_list = self.read_external_file()
        self.read_prob_data()

        number_of_sentence = 0
        number_of_token = 0
        number_of_sentence_correctly_tagged = 0;
        number_of_token_correctly_tagged = 0

        for sentence in sentence_list:
            number_of_sentence = number_of_sentence + 1
            sentence_correctly_tagged = True

            tag1 = Tag.NOTEXIST
            tag2 = Tag.NOTEXIST
            for token in sentence:
                number_of_token = number_of_token + 1

                word = token['form']
                tag_detector = Tag.NOTEXIST
                tag = tag_detector.get_tag(token['upostag'])

                is_tag_correctly = self.get_tag(word, tag1, tag2, real_tag)
                if is_tag_correctly:
                    number_of_token_correctly_tagged = number_of_token_correctly_tagged + 1
                else:
                    sentence_correctly_tagged = False
                tag2 = tag1
                tag1 = tag

            if sentence_correctly_tagged:
                number_of_sentence_correctly_tagged = number_of_sentence_correctly_tagged + 1

        print "number of sentence               " + number_of_sentence
        print "sentence correctly tagged        " + number_of_sentence_correctly_tagged
        print "ratio sentence correctly tagged  " + number_of_sentence_correctly_tagged/number_of_sentence
        print "number of token                  " + number_of_token
        print "token correctly tagged           " + number_of_token_correctly_tagged
        print "ratio token correcly tagged      " + number_of_token_correctly_tagged/number_of_token


    def get_tag(self, word, tag1, tag2, real_tag):
        #count P(tag|word) = P(word|tag)*P(tag|tag-1,tag-2)
        tag_with_highest_prob = Tag.X
        current_prob_value = 0.00000

        for tag_candidate in Tag:
            cond1 = ConditionalProbabilityExpression(tag_candidate, word)
            cond2 = ConditionalProbabilityExpression(tag_candidate, tag1, tag2)
            if cond1.get_key() in self.wt_prob_dict.keys() and cond2.get_key() in self.ttt_prob_dict.keys():
                prob_value = wt_prob_dict[cond1.get_key()]*ttt_prob_dict[cond2.get_key()]
                if prob_value > current_prob_value:
                    tag_with_highest_prob = tag_candidate
                    current_prob_value = prob_value
        if tag_with_highest_prob.value == real_tag.value:
            return True
        else:
            return False

    def read_external_file(self):
        corpus_file = open(file_path,'r')
        corpus_data = re.sub(r" +", r"\t",corpus_file.read())
        sentence_list = parse(corpus_data)
        return sentence_list

    def read_prob_data(self):
        tagProb = TagProbabilityService(train_file_path)
        self.tw_prob_dict = tagProb.get_tw_prob_dict()
        self.wt_prob_dict = tagProb.get_wt_prob_dict()
        self.ttt_prob_dict = tagProb.get_ttt_prob_dict()
