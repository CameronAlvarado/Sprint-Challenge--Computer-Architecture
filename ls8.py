#!/usr/bin/env python3

"""Main."""

import os
import sys
from cpu import *

cpu = CPU()

path = sys.argv[1]

cpu.load(path)
cpu.run()
