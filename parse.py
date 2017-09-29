from conllu.parser import parse, parse_tree, parse_line
import re

file_path = "/home/asus/Semester7/NLP/POSTagger/UD_English/en-ud-dev.conllu"
corpus_file = open(file_path,'r')
data = re.sub(r" +", r"\t",corpus_file.read())
tree = parse_line(data)
print tree[0]
