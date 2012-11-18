import sys
import re
import nltk
import optparse
import difflib
import os.path
import optparse

def tokenize(text):
   return [token + '\n' for token in nltk.word_tokenize(text)]

def get_spans(text, tokens):
   i = -1
   for t in tokens:
      i = text.find(i+1, t)
      yield (i, i+len(t))

def dump_tokens(filename, tokens):
   with open(filename, 'w') as out:
      out.write('\n'.join(tokens))
      out.write('\n')

def get_command_line():
   usage = """usage: %prog [options] master-file compare-file"""
   parser = optparse.OptionParser(usage)
   parser.add_option("-t", "--tokens", action="store_true", default=False,
      help='Store hte tokens for debugging purposes')
   parser.add_option("-l", "--lines", type="int", default=0,
      help="Set number of context lines (default 0). Don't change this unless you know why.")
   parser.add_option("-o", "--output", type="string", default=None,
      help='Set the output filename. Default is diff-<MASTER>-<COMPARE>.out')
   options, args = parser.parse_args()
   if len(args) == 0:
      parser.print_help()
      sys.exit(1)
   return options, args

def main():
   options, args = get_command_line()
   if len(args) != 2:
      parser.error("need to specify both a master and compare file")

   master_file, compare_file = args # as specified in the usage string

   text1 = master_file
   text2 = compare_file
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
      s1 = s1 + tokenize(line) 

   if options.tokens:
      dump_tokens(tokens1, s1)
    
   print("Processing %s" % basename2)
   s2 = []
   for line in content2:
      s2 = s2 + tokenize(line)

   if options.tokens:
      dump_tokens(tokens2, s2)

   if options.output == None:
      (head, tail1) = os.path.split(basename1)
      (head, tail2) = os.path.split(basename2)
      compare_filename = 'diff-%s-%s.out' % (tail1, tail2)
   else:
      compare_filename = options.output

   print("Writing %s" % compare_filename)

   with open(compare_filename, "w") as out:
      for line in difflib.context_diff(s1, s2, fromfile=text1, tofile=text2, n=0):
         out.write(line)

if __name__ == '__main__':
   main()
