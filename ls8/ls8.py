#!/usr/bin/env python3
"""Main."""
import sys
from cpu import *
# Check the file is enter from command line
if len(sys.argv) != 2:
    print("Enter file name.")
    exit(1)
cpu = CPU()
# Get file name from command line arguments
cpu.load(sys.argv[1])
cpu.run()

# Run
# ls8>python ls8.py examples/sctest.ls8

