from enum import  Enum

class Tag(Enum):
    ADJ = 1
    ADP = 2
    ADV = 3
    AUX = 4
    CCONJ = 5
    DET = 6
    INTJ = 7
    NOUN = 8
    NUM = 9
    PART = 10
    PRON = 11
    PROPN = 12
    PUNCT = 13
    SCONJ = 14
    SYM = 15
    VERB = 16
    X = 17
    NOTEXIST = 18

    def get_tag(self, string):
        if (string == "ADJ"):
            return self.ADJ
        elif (string == "ADP"):
            return self.ADP
        elif (string == "ADV"):
            return self.ADV
        elif (string == "AUX"):
            return self.AUX
        elif (string == "CCONJ"):
            return self.CCONJ
        elif (string == "DET"):
            return self.DET
        elif (string == "INTJ"):
            return self.INTJ
        elif (string == "NOUN"):
            return self.NOUN
        elif (string == "NUM"):
            return self.NUM
        elif (string == "PART"):
            return self.PART
        elif (string == "PRON"):
            return self.PRON
        elif (string == "PROPN"):
            return self.PROPN
        elif (string == "PUNCT"):
            return self.PUNCT
        elif (string == "SCONJ"):
            return self.SCONJ
        elif (string == "SYM"):
            return self.SYM
        elif (string == "VERB"):
            return self.VERB
        elif (string == "X"):
            return self.X
        else :
            return self.NOTEXIST
