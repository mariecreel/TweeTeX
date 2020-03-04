"""
tweetex.py

Nick Creel | Feb 5 2020 | MIT License
"""

from lexer import Lexer # my lexer
import argparse  		# external library for handling input from command line
import parser 			# parser
import templater 		# code generator
import re		 		# for regular expressions


def getfile():
    parser = argparse.ArgumentParser(description="accepts input \ for TweeTex compiler")
    parser.add_argument('file', metavar='filename', type=str, nargs=1,
            help='the location of the TweeTex file to compile')
    args = parser.parse_args()
    with open(args.file[0], "r") as file:
        source = file.read()
    return (source, args.file[0])

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
    source, sourceName = getfile()
    sourceName = sourceName[:-3] + 'tw' #change to Twee extension
    mylexer = Lexer(source)
    mylexer.lex()
    tokens = mylexer.tokens
    print("-------printing tokens produced by lexer")
    for i in tokens.queue:
        print(i)
    print("\n--------beginning parse routine")
    ast = parser.parse(tokenQueue = tokens) #this is NOT the same as argparse
    print(ast)
    printchildren(ast)
    print("\n--------beginning code generation")
    result = templater.makeNewFile(sourceName,ast)

main()
