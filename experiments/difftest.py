import sys
import re
#import nltk

from difflib import *

#regex = re.compile(r"\d+|[-'a-z]+|[ ]+|\s+|[\"\'.,]|\S+", re.I)
regex = re.compile(r"\d+|[A-Za-z][-'A-Za-z]+|[!\"&\'(),\-\.\/\"\'.,]|\S+", re.I)

def tokenize(text, regex):
   txt = text.rstrip()
   slice_starts = [m.start() for m in regex.finditer(txt)] + [None]
   return [txt[s:e].strip() + '\n' for s, e in zip(slice_starts, slice_starts[1:])]

text1 = sys.argv[1]
text2 = sys.argv[2]

f1 = open(text1)
f2 = open(text2)

content1 = f1.readlines()
content2 = f2.readlines()

s1 = []
for line in content1:
   s1 = s1 + tokenize(line, regex)

with open('s1.tokens', 'w') as debug:
   debug.write('\n'.join(s1))
   debug.write('\n')
 
s2 = []
for line in content2:
   s2 = s2 + tokenize(line, regex)

for line in context_diff(s1, s2, fromfile=text1, tofile=text2, n=0):
   sys.stdout.write(line)

