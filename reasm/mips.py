#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Chiba

import itertools
import re
import sys
import traceback

from register import Register
from command import rType
from command import iType
from command import jType

class MIPSProgram:
  def __init__(self, lines = None, textBase = 0, dataBase = 0x4000):
    self.textBase = textBase if isinstance(textBase, int) else eval(textBase)
    self.dataBase = dataBase if isinstance(dataBase, int) else eval(dataBase)
    self.command =[]
    self.data = []
    self.labels = {}
    self.defines = {}
    
    if lines is not None:
      self.addLines(lines)
      
  def addLines(self, lines):
    for l in lines:
      self.handleLine(l)
      
  def handleLine(self, line):
    tmp = []
    x = line >> 26
    line = line - (x << 26)   # opcode
    ans = ""
    # rType command
    if x == 0: 
      x = line % (1 << 6)
      line >>= 6            # func
      line >>= 5            # shamt
      for _ in rType:
        if _[2] == x:
          cnt = len(_[3])
          ans += _[0]
          for i in xrange(cnt):
            ans += " "
            if _[3][i] == "rd":
              ans += Register.names[(line >> 10)][1]
            elif _[3][i] == "rs":
              ans += Register.names[(line >> 5) % (1 << 5)][1]
            else:
              ans += Register.names[line % (1 << 5)][1]
            ans += ("" if i == cnt - 1 else ",")
          break
          
    # iType command
    elif x != (0b000010) and x != (0b000011):
      for _ in iType:
        if _[1] == x:
          cnt = len(_)
          ans = _[0] + " " + hex(line % (1 << 21))
          line = line % (1 << 21)
          tmp = line % (1 << 16)
          line = line % (1 << 16)
          if cnt > 3:
            x -= _[2]
          ans += (", " + hex(x) + ", " + hex(line))
          break
      
    # jType command
    else:
      if x == jType[0][1]:
        ans = jType[0][0] + " " + hex(line)
      else:
        ans = jType[1][0] + " " + hex(line)
        
    self.data.append(ans)
    self.command.append(ans)

  def Data(self):
    return self.data