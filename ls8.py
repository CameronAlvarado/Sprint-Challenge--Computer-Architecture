#!/usr/bin/env python3

"""Main."""

import os
import sys
from cpu import *

cpu = CPU()

path = sys.argv[1]
# Checks if file exists
# try:
#     with open(path, 'r') as f:
#         contents = f.read()
#         cpu.load(contents)
#         print("contents", contents)
# except:
#     print("No such file '{}'".format(path), file=sys.stderr)

# print(sys.argv)
# path = sys.argv[1]
# if os.path.exists(path):
#     with open(sys.argv[1], 'r') as f:
#         contents = f.read()
#         cpu.load(contents)
#         # print(contents)
# else:
#     print("No such file '{}'".format(path), file=sys.stderr)

# program = open("examples/mult.ls8", "r")
# if program.mode == 'r':
#     contents = program.read()
#     print(contents)

cpu.load(path)
cpu.run()
