"""
tweetex.py


"""

import lexer as Lexer
import re
import argparse
import yaml

def main():
    parser = argparse.ArgumentParser(description="accepts input \ for TweeTex compiler")
    parser.add_argument('file', metavar='f', type=str, nargs=1,
            help='the location of the TweeTex file to compile')
    args = parser.parse_args()
    with open(args.input[0], "r") as file:
        source = file.read()
    lexer = Lexer.lexer(source)
    tokens = lexer.lex()
    print(tokens)

if __name__ == '__main__':
    import doctest
    doctest.testmod()

