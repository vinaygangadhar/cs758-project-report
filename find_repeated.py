#!/usr/bin/python
import sys
import string
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  
  def disable(self):
    self.HEADER = ''
    self.OKBLUE = ''
    self.OKGREEN = ''
    self.WARNING = ''
    self.FAIL = ''
    self.ENDC = ''

input_files=[]

for i in sys.argv[1:]:
  input_files.append(i)

if(len(input_files)==0):
  bashCommand = "find . -name *.tex "
  import subprocess
  process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
  stdout = process.communicate()
  something=""
  for i in stdout:
    if i!=None:
      something+=i

  for i in something.split("\n"):
    i=string.strip(i)
    if len(i)==0:
      continue
    input_files.append(i)


for input_file_name in input_files:
  with open(input_file_name) as input_file:
    prev_word = ""
    prev_line = ""
    rep_words = []
    should_print_prev_line=False
    printed_prev_line=False
    printed_cur_line=False
    total_errors=0

    for i, line in enumerate(input_file):
      del rep_words[:]
      should_print_prev_line=False

      #iterate over line to find duplicates
      for j, word in enumerate(line.split(" ")):
         word = string.strip(word)

         if len(word) == 0:
           continue

         if word[0] == '%':
           prev_word=""
           break

         if "^" in word or "@" in word or "&" in word or "/" in word or "\\" in word \
                        or "%" in word or "{" in word or "}" in word or is_number(word)\
                        or "." == word or (len(word)==1 and not word == "a"):
           prev_word=""
           continue

         if word == prev_word:
           rep_words.append(j)
           total_errors+=1
           if j==0:
             should_print_prev_line=True

         prev_word=word

      if should_print_prev_line and not printed_prev_line:
        print str(i)+":   ",
        print prev_line,

      if len(rep_words) > 0:
        print str(i+1)+":   ",

        words = line.split(" ")
        for j, word in enumerate(words):
           if j in rep_words:
             sys.stdout.write(bcolors.FAIL)
           else:
             sys.stdout.write(bcolors.ENDC)
           if j == len(words)-1:
             print word,
           else:
             print word+" ",
           
        printed_cur_line=True
      else:
        printed_cur_line=False

      sys.stdout.write(bcolors.ENDC)
      printed_prev_line=printed_cur_line
      prev_line = line

  if total_errors > 0:
    print bcolors.WARNING,
    print "{0} repeated words found".format(total_errors) + " in file: \"" + input_file_name + "\" !" + bcolors.ENDC
    print
