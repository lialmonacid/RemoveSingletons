#!/usr/bin/env python

import sys
import os
import getopt
from Bio import SeqIO

OPT_INPUT_FILE=""
OPT_OUTPUT_FILE=False
OPT_MIN_FREQ=1

def Usage():
    print "\nRemoveSingletons.py is a program that read a FASTA file and filter the sequences according to their frequency value. The frequency is calculated by the \"fastx_collapser\" software of the FASTX toolkit suite.\n"
    print "Usage:"
    print "\tRemoveSingletons.py -i [FASTA file] -n [Frequency value]\n"
    print "\nMandatory options:"
    print "\t-i, --input=FILE"
    print "\t\tThe input FASTA file to be filtered. "
    print "\t-n, --frequency=THRESHOLD"
    print "\t\tThis option set the minimum frequency that a sequence must have."
    print "\nOther options:"
    print "\t-h, --help"
    print "\t\tShow the options of the program."
    print "\t-o, --output=FILE"
    print "\t\tWrite the output to the given file in FASTA format. By default this option is not set and the ouput is written to the STDOUT."
    print "\n"
    sys.exit(1)

# Function that read and parse the command line arguments.
def SetOptions(argv):
    if len(argv) == 0:
        Usage()
    options, remaining = getopt.getopt(argv, 'i:n:o:h', ['input=','frequency=','output=','help'])
    opt_flag = {'i': False, 'n':False, 'o':False}
    global OPT_INPUT_FILE, OPT_OUTPUT_FILE, OPT_MIN_FREQ
    for opt, argu in options:
        if opt in ('-i', '--input'):
            if not opt_flag['i']:
                if os.path.exists(argu):
                    OPT_INPUT_FILE = argu
                    opt_flag['i'] = True
                else:
                    print >> sys.stderr , "\n[ERROR]: File or path of the input file does not exist. ", argu, "\n"
                    sys.exit(1)
            else:
                print >> sys.stderr , "\n[ERROR]: Trying to redefine the input file. Option -i / --input was already set.\n"
                sys.exit(1)
        elif opt in ('-o', '--output'):
            if not opt_flag['o']:
                if not os.path.dirname(argu): # Empty path means the current directory.
                    OPT_OUTPUT_FILE = argu
                    opt_flag['o'] = True
                else:
                    if os.path.exists(os.path.dirname(argu)):
                        OPT_OUTPUT_FILE = argu
                        opt_flag['o'] = True
                    else:
                        print >> sys.stderr , "\n[ERROR]: Path to write the output does not exist. ", os.path.dirname(argu), "\n"
                        sys.exit(1)
            else:
                print >> sys.stderr , "\n[ERROR]: Trying to redefine the output file. Option -o / --output was already set.\n"
                sys.exit(1)
        elif opt in ('-h', '--help'):
            Usage()
        elif opt in ('-n', '--frequency'):
            if not opt_flag['n']:
                OPT_MIN_FREQ = int(argu)
                opt_flag['n'] = True
                if OPT_MIN_FREQ < 1:
                    print >> sys.stderr , "\n[ERROR]: The minimum sequence frequency must be an integer greater or equal than 1. See option -n / --frequency.\n"
                    sys.exit(1)
            else:
                print >> sys.stderr , "\n[ERROR]: Trying to redefine the minimum sequence frequency. Option -n / --frequency was already set.\n"
                sys.exit(1)
    if not opt_flag['i']:
        print >> sys.stderr , "\n[ERROR]: Input file not defined. Option -i / --input.\n"
        sys.exit(1)
    if not opt_flag['n']:
        print >> sys.stderr , "\n[ERROR]: Sequence frequency threshold was not defined. Option -n / --frequency.\n"
        sys.exit(1)

def GetSequenceFrequency(header):
    if not header:
        print >> sys.stderr , "\n[ERROR]: No ID for some sequence in the FASTA file\n"
        sys.exit(1)
    return int(header.split("-")[-1])

# Parse command line
SetOptions(sys.argv[1:])

# Setting the output
if OPT_OUTPUT_FILE:
    OPT_OUTPUT_FILE=open(OPT_OUTPUT_FILE,"w")
else:
    OPT_OUTPUT_FILE=sys.stdout

# Reading the FASTA.
for record in SeqIO.parse(open(OPT_INPUT_FILE, "rU"), "fasta"):
    if GetSequenceFrequency(record.description) >= OPT_MIN_FREQ:
        print >> OPT_OUTPUT_FILE , ">"+record.description
        print >> OPT_OUTPUT_FILE , record.seq

