#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Chiba

import itertools
import re
import sys
import traceback

from command import Command
from register import Register, EmptyRegister

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
    loc = sum([_.Size() for _ in self.command])
  
    for rep, val in self.defines.iteritems():
      line = re.sub(rep, val, line)
  
    if re.match("^\s*$", line) is not None:
      return
    
    try:
      m = re.match(
        r'''^\s*#DataAddr\s*(?P<dataaddr>[_a-zA-Z0-9]+)\s*$''',
      line)
      if m is not None:
        self.dataBase = eval(m.group('dataaddr')) if m.group('dataaddr')[0:2] == "0x" else eval('0b' + m.group('dataaddr')) 
        return
        
      m = re.match(
        r'''^\s*#BaseAddr\s*(?P<baseaddr>[_a-zA-Z0-9]+)\s*$''',
      line)
      if m is not None:
        self.textBase = eval(m.group('baseaddr')) if m.group('baseaddr')[0:2] == "0x" else eval('0b' + m.group('baseaddr'))
        return
      
      m = re.match(
        r'''^\s*\.DEFINE\s*(?P<label>[_a-zA-Z0-9]+)\s*(?P<value>.*)$''',
      line)
      if m is not None:
        self.defines[m.group('label')] = m.group('value')
        return
    
      m = re.match(
        r'''^\s*\.DATA\s*(?P<label>[_a-zA-Z0-9]+)\s*(?P<str>".*")''',
      line)
      if m is not None:
        self.registerDataLabel(m.group('label'), eval(m.group('str')))
        return
        
      m = re.match("^\s*(?P<label>[_a-zA-Z0-9]+):$", line)
      if m is not None:
        self.registerLabel(m.group('label'), loc)
        return
    
      m = re.match(
        "^\s*#.*$", 
      line)
      if m is not None:
        return
      inst = Command.parseLine(self, loc, line)
      self.command.append(inst)
    except Exception as ERR:
      print
      print traceback.format_exc(ERR)
      print "*** Invalid line: '%s'" % (line)
      print
      sys.exit(1)
  
  def registerLabel(self, label, addr):
    self.labels[label] = addr
  
  def registerDataLabel(self, label, string):
    string = string + "\0"
    pos = sum([len(x) for x in self.data])
    self.labels[label] = self.dataBase + pos
    self.data.append(string)
    
  def Label(self, label):
    if hasattr(label, '__call__'):
      value = label()
      return value
    if label not in self.labels.keys():
      raise Exception("Unknown label: '%s'" % (label))
    return self.labels[label]
    
  def Bytes(self):
    return list(itertools.chain(*[x.Bytes() for x in self.command]))