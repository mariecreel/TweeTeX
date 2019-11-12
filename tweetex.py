"""
tweetex.py

nick creel | nov 12 2019 | mit license
"""

from lexer import Lexer
import re
import argparse

def getfile():
    parser = argparse.ArgumentParser(description="accepts input \ for TweeTex compiler")
    parser.add_argument('file', metavar='filename', type=str, nargs=1,
            help='the location of the TweeTex file to compile')
    args = parser.parse_args()
    with open(args.file[0], "r") as file:
        source = file.read()
    return source

def main():
    source = getfile()
    mylexer = Lexer(source)
    mylexer.lex()
    tokens = mylexer.tokens 
    print(tokens)
main()
