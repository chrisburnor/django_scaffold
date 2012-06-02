import sys

from fabric.api import *

# Utility functions for deploymnent

# Return True or false, default to false if empty response
def yes_or_no_input(question, defaultToYes=False):
  yes = set(['y', 'ye','yes' ])
  no  = set(['n','no'])

  # Add the empty string to yes if set to default to yse, oltherwas no
  if defaultToYes:
    yes.add("")
    optionsString = "(Y/n)"
  else:
    no.add("")
    optionsString =  "(y/N)"

  while True:
    choice = raw_input("%s %s " % (question, optionsString)).lower()
    if choice in yes:
      return True
    elif choice in no:
      return False
    else:
      sys.stdout.write("Please respond with 'yes' or 'no'")
