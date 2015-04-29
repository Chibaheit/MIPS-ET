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

parser = argparse.ArgumentParser()
parser.add_argument('inputFile')
parser.add_argument('-o', '--output', default=argparse.SUPPRESS,
  help="Output file", metavar="filename")
  
args = vars(parser.parse_args())
fileName, fileExt = os.path.splitext(args['inputFile'])
lines = []
if fileExt == ".bin":
  with open(args['inputFile'], "rb") as f:
    tmp = f.read(1)
    ans = 0
    t = 0
    while tmp != "":
      t += 1
      ans = ans * 256 + int(tmp.encode('hex'), 16)     
      tmp = f.read(1)    
      if t == 4:
        t = 0
        lines.append(ans)      
        ans = 0
else:
  with open(args['inputFile'], "r") as f:
    tmp = f.readline()
    tmp = f.readline()
    tmp = f.readline()[:-2]
    while tmp:
      t = tmp.split(' ')
      num = int(t[0], 16) * 256 * 256 * 256 + int(t[1], 16) * 256 + int(t[2], 16) * 256 + int(t[3], 16)
      lines.append(num)
      tmp = f.readline()[:-2]    
mp = mips.MIPSProgram(textBase = 0, dataBase = 0x4000)
mp.addLines(lines)

f, e = os.path.splitext(args['inputFile'])

output = args['output'] if 'output' in args else f + '.asm'


with open(output, 'w') as out:
#  print "Writing asm to '%s..." %(args['output']), 
  data = mp.Data()
  for ans in data:
    out.write(ans)
    out.write('\n')
  print os.path.dirname(os.path.abspath(args['inputFile']))
#  print "Done!"
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Chiba