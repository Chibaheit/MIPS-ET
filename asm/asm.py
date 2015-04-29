#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Chiba

import argparse
import sys
import re
import os
import os.path
import mips
from register import Register
from command import Command
import command

parser = argparse.ArgumentParser()
parser.add_argument('inputFile')
parser.add_argument('-o', '--output', default=argparse.SUPPRESS,
  help="Output file", metavar="filename")
parser.add_argument('-f', '--outfile', default=argparse.SUPPRESS,
  help="Output extends", metavar="filename")

  
args = vars(parser.parse_args())

f = open(args['inputFile'])
lines = f.readlines()
lines = [x.replace("\n", "") for x in lines]
f.close()

mp = mips.MIPSProgram(textBase = 0, dataBase = 0x4000)
mp.addLines(lines)

f, e = os.path.splitext(args['inputFile'])

output = args['output'] if 'output' in args else f + '.bin'
ext = args['outfile']
if ext == "bin":
  with open(f + '.bin', 'w') as out:
  #  print "Writing binary to '%s..." %(args['output']), 
    Bytes = mp.Bytes()
    for ans in Bytes:
      out.write("%c" % (ans,))
else:
  with open(f + '.coe', 'w') as out:
    Bytes = mp.Bytes()
    out.write("memory_initialization_radix=16;\n")
    out.write("memory_initialization_vector=")
    for _ in xrange(len(Bytes) / 4):
      out.write("\n%02x %02x %02x %02x" % (tuple(Bytes[_ * 4 : _ * 4 + 4])),)
      out.write(',' if _ != (len(Bytes) / 4 - 1) else ';')
    out.write('\n')

      
print os.path.dirname(os.path.abspath(args['inputFile']))
#  print "Done!"
#else:
#  binary = mp.Bytes()
#  for j in xrange(len(binary) / 4):
#    print "%02x %02x %02x %02x" % (tuple(binary[j * 4 : j * 4 + 4]))
