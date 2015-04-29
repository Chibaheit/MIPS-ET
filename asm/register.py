#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Chiba

import re

class Register:
  names = [
    ["$0", "$zero"],
    ["$1", "$at"],
    ["$2", "$v0"],
    ["$3", "$v1"],
    ["$4", "$a0"],
    ["$5", "$a1"],
    ["$6", "$a2"],
    ["$7", "$a3"],
    ["$8", "$t0"],
    ["$9", "$t1"],
    ["$10", "$t2"],
    ["$11", "$t3"],
    ["$12", "$t4"],
    ["$13", "$t5"],
    ["$14", "$t6"],
    ["$15", "$t7"],
    ["$16", "$s0"],
    ["$17", "$s1"],
    ["$18", "$s2"],
    ["$19", "$s3"],
    ["$20", "$s4"],
    ["$21", "$s5"],
    ["$22", "$s6"],
    ["$23", "$s7"],
    ["$24", "$t8"],
    ["$25", "$t9"],
    ["$26", "$k0"],
    ["$27", "$k1"],
    ["$28", "$gp"],
    ["$29", "$sp"],
    ["$30", "$fp"],
    ["$31", "$ra"],    
  ]
  
  def __init__(self, name = None, pos = None):
    self.pos = None
    if pos is not None:
      self.pos = pos
    else:
      if name is None:
        raise "Empty register"
      else:
        for _, val in enumerate(self.names):
          if name.lower() in val:
            self.pos = _
    if self.pos is None:
      raise "Undefined register" + name
      
  def binary(self):
    return self.pos
    
  def __repr__(self):
    return "Register (%s)" % (self.names[self.pos][1])
    
class EmptyRegister:
  def __init__(self):
    pass
    
  def binary(self):
    return 0
    
  def __repr__(self):
    return "Empty register"        