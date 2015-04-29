#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Chiba

import re
import itertools
from register import Register, EmptyRegister

_NAME = "(?P<name>[a-zA-Z]+)"
NAME = _NAME + "\s+"
FIRST = "(?P<first>\$[0-9a-zA-Z]+)\s*"
SECOND = "(?P<second>\$[0-9a-zA-Z]+)\s*"
THIRD = "(?P<third>\$[0-9a-zA-Z]+)\s*"
IMM = "(?P<imm>[0-9][x0-9A-Fa-f]*)\s*"
LABEL = "(?P<label>[a-zA-Z_][_0-9a-zA-Z]+)\s*"
COMMA = "\s*,\s*"
#EOL = ";$"
EOL = "\s*(#.*)?$"

LINEBEGIN = r"(?i)^[^#]*?"

commandTypes = [
  re.compile(LINEBEGIN + 
    NAME + FIRST + COMMA + SECOND + COMMA + THIRD + EOL
  ),
  re.compile(LINEBEGIN + 
    NAME + FIRST + COMMA + SECOND + COMMA + LABEL + EOL
  ),
  re.compile(LINEBEGIN + 
    NAME + FIRST + COMMA + SECOND + COMMA + IMM + EOL
  ),
  re.compile(LINEBEGIN + 
    NAME + FIRST + COMMA + IMM + "\(\s*" + SECOND + "\s*\)\s*" + EOL
  ),
  re.compile(LINEBEGIN + 
    NAME + FIRST + COMMA + LABEL + EOL
  ),
  re.compile(LINEBEGIN + 
    NAME + FIRST + COMMA + IMM + EOL
  ),
  re.compile(LINEBEGIN + 
    NAME + FIRST + EOL
  ),
  re.compile(LINEBEGIN + 
    NAME + LABEL + EOL
  ),
  re.compile(LINEBEGIN + 
    NAME + IMM + EOL
  ),
  re.compile(LINEBEGIN + 
    _NAME + EOL
  )                  
]

rType = {
  "add":     (0x0, 0b100000, ["rd", "rs", "rt"]),
  "addu":    (0x0, 0b100001, ["rd", "rs", "rt"]),
  "and":     (0x0, 0b100100, ["rd", "rs", "rt"]),
  "break":   (0x0, 0b001101, []),
  "div":     (0x0, 0b011010, ["rd", "rs", "rt"]),
  "divu":    (0x0, 0b011011, ["rs", "rt"]),
  "jalr":    (0x0, 0b001001, ["rd", "rs"]),
  "jr":      (0x0, 0b001000, ["rs"]),
  "mfhi":    (0x0, 0b010000, ["rd"]),
  "mflo":    (0x0, 0b010010, ["rd"]),
  "mthi":    (0x0, 0b010001, ["rs"]),
  "mtlo":    (0x0, 0b010011, ["rs"]),
  "mult":    (0x0, 0b011000, ["rs", "rt"]),
  "multu":   (0x0, 0b011001, ["rs", "rt"]),
  "nor":     (0x0, 0b100111, ["rd", "rs", "rt"]),
  "or":      (0x0, 0b100101, ["rd", "rs", "rt"]),
  "sll":     (0x0, 0b000000, ["rd", "rt"]),
  "sllv":    (0x0, 0b000100, ["rd", "rt"]),
  "slt":     (0x0, 0b101010, ["rd", "rs", "rt"]),
  "sltu":    (0x0, 0b101011, ["rd", "rs", "rt"]),
  "sra":     (0x0, 0b000011, ["rd", "rt"]),
  "srav":    (0x0, 0b000111, ["rd", "rt"]),
  "srl":     (0x0, 0b000010, ["rd", "rt"]),
  "srlv":    (0x0, 0b000110, ["rd", "rt", "rs"]),
  "sub":     (0x0, 0b100010, ["rd", "rs", "rt"]),
  "subu":    (0x0, 0b100011, ["rd", "rs", "rt"]),
  "syscall": (0x0, 0b001100, []),
  "xor":     (0x0, 0b100110, ["rd", "rs", "rt"])
}

iType = {
  "addi":  (0b001000, ["rt", "rs"]),
  "addiu": (0b001001, ["rt", "rs"]),
  "andi":  (0b001100, ["rt", "rs"]),
  "beq":   (0b000100, ["rs", "rt"]),
  "bgez":  (0b000001, 0b00001, ["rs"]),
  "bgtz":  (0b000111, 0b00000, ["rs"]),
  "blez":  (0b000110, 0b00000, ["rs"]),
  "bltz":  (0b000001, 0b00000, ["rs"]),
  "bne":   (0b000101, ["rs", "rt"]),
  "lb":    (0b100000, ["rt", "rs"]),
  "lbu":   (0b100100, ["rt", "rs"]),
  "lh":    (0b100001, ["rt", "rs"]),
  "lhu":   (0b100101, ["rt", "rs"]),
  "lui":   (0b001111, ["rt"]),
  "lw":    (0b100011, ["rt", "rs"]),
  "lwc1":  (0b110001, ["rt", "rs"]),
  "ori":   (0b001101, ["rt", "rs"]),
  "sb":    (0b101000, ["rt", "rs"]),
  "slti":  (0b001010, ["rt", "rs"]),
  "sltiu": (0b001011, ["rt", "rs"]),
  "sh":    (0b101001, ["rt", "rs"]),
  "sw":    (0b101011, ["rt", "rs"]),
  "sc":    (0b111000, ["rt", "rs"]),
  "swc1":  (0b111001, ["rt", "rs"]),
  "xori":  (0b001110, ["rt", "rs"])
}

jType = {
  "j":    (0b000010, []),
  "jal":  (0b000011, [])
}

class Command:
  def __init__(self, program, pos, name = None, first = None, 
              second = None, third = None, imm = None, label = None):
    name = name.lower()
    if name not in rType.keys() and \
       name not in iType.keys() and \
       name not in jType.keys():
      raise "'%s' is not a MIPS assembly command." % (name.lower())
    self.program = program
    self.pos = pos
    self.name = name
    
    self.rs = EmptyRegister()
    self.rt = EmptyRegister()
    self.rd = EmptyRegister()
    
    registers = (
      rType[name][-1] if name in rType else \
      iType[name][-1] if name in iType else \
      jType[name][-1]
    )
    
    rList = [x for x in [first, second, third] if x is not None]
    
    if len(registers) != len(rList):
      raise "'%s' requires %d registers." % (name, len(registers))
    
    for _, reg in zip(registers, rList):
      if _ == "rs":
        self.rs = Register(reg)
      if _ == "rd":
        self.rd = Register(reg)
      if _ == "rt":
        self.rt = Register(reg)  
      
    if isinstance(imm, int):
      self.imm = imm
    else:
      self.imm = eval(imm) if imm is not None else 0
    self.label = label
    
    if imm is not None and self.label is not None:
      raise "Label and imm can't both exist."
      
      
  @staticmethod
  def parseLine(program, pos, line):
    global commandTypes
    for m in commandTypes:
      ans = m.match(line)
      if ans is not None:
        group = ans.groupdict()
        return Command(program = program, pos = pos, **group)
    raise "'%s' is not a command." % (line)
    
  def toBin(self):
    if self.name in rType.keys():
      ans = 0                           # opcode
      ans |= (self.rs.binary() << 21)   # rs
      ans |= (self.rt.binary() << 16)   # rt
      ans |= (self.rd.binary() << 11)   # rd
      ans |= (self.imm << 6)            # shamt
      ans |= (rType[self.name][1] << 0) # funct
      return ans
      
    if self.name in iType.keys():
      ans = iType[self.name][0] << 26   # opcode
      ans |= (self.rs.binary() << 21)   # rs
      ans |= (self.rt.binary() << 16)   # rt
      if len(iType[self.name]) > 2:
        ans |= (iType[self.name][1] << 16) # rt adjustment
        
      if self.label is not None:
        if "b" == self.name[0]:
          tmp = self.program.Label(self.label) - self.pos - 1
        else:
          tmp = self.program.Label(self.label)
        ans |= (tmp & 0xFFFF)
      else:
        if "b" == self.name[0]:
          ans |= (self.imm >> 2 & 0xFFFF)
        else:
          ans |= (self.imm & 0xFFFF)
      return ans
      
    if self.name in jType.keys():
      ans = jType[self.name][0] << 26   # opcode
      if self.label is not None:
        ans |= ((self.program.Label(self.label) + \
               self.program.textBase) % (1 << 26))  # label
      else:
        ans |= (self.imm % (1 << 26)) # address
      return ans
      
  def Size(self):
    return 1
    
  def Bytes(self):
    x = self.toBin()
    ans = [
      x >> 24,
      x >> 16 & 0xFF,
      x >> 8 & 0xFF,
      x & 0xFF
    ]
    return ans
    
  def __repr__(self):
    return "Command(%s, %s, %s, %s, %s, %s)" % \
      (self.name, self.rs, self.rt, self.rd, self.imm, self.label)
