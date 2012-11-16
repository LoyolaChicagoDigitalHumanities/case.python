import sys
import re
import nltk

from difflib import *

EOLMARKER = '==\n' 

def tokenize(text):
   return [token + '\n' for token in nltk.word_tokenize(text)]

def dump_tokens(filename, tokens):
   with open(filename, 'w') as out:
      out.write('\n'.join(tokens))
      out.write('\n')

import os.path
text1 = sys.argv[1]
text2 = sys.argv[2]
(basename1, ext) = os.path.splitext(text1)
(basename2, ext) = os.path.splitext(text2)
tokens1 = basename1 + '.tokens'
tokens2 = basename2 + '.tokens'

f1 = open(text1)
f2 = open(text2)

content1 = f1.readlines()
content2 = f2.readlines()

print("Processing %s" % basename1)
s1 = []
for line in content1:
   s1 = s1 + tokenize(line) + [ EOLMARKER ]

dump_tokens(tokens1, s1)
 
print("Processing %s" % basename2)
s2 = []
for line in content2:
   s2 = s2 + tokenize(line) + [ EOLMARKER ]

dump_tokens(tokens2, s2)

(head, tail1) = os.path.split(basename1)
(head, tail2) = os.path.split(basename2)
compare_filename = 'diff-%s-%s.out' % (tail1, tail2) 

print("Writing %s" % compare_filename)

with open(compare_filename, "w") as out:
   for line in context_diff(s1, s2, fromfile=text1, tofile=text2, n=0):
      out.write(line)

