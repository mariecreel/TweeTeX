"""
tweetex.py

nick creel | nov 12 2019 | mit license
"""

from lexer import Lexer
import parser
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

def printchildren(token):
    #this is depth first, just a test.
    if type(token.children) != list:
        print(token.children)
        printchildren(token.children)
    else:
        for atoken in token.children:
            if len(token.children) > 0:
                print(atoken)
                printchildren(atoken)
            else:
                print(atoken)

def main():
    source = getfile()
    mylexer = Lexer(source)
    mylexer.lex()
    tokens = mylexer.tokens
    print("-------printing tokens produced by lexer")
    for i in tokens.queue:
        print(i)

    print("\n--------beginning parse routine")
    ast = parser.parse(tokenQueue = tokens)
    print(ast)
    printchildren(ast)
main()
