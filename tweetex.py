"""
tweetex.py


"""

import lexer as lexer
import re
import argparse

def main():
    parser = argparse.ArgumentParser(description="accepts input \ for TweeTex compiler")
    parser.add_argument('file', metavar='f', type=str, nargs=1,
            help='the location of the TweeTex file to compile')
    args = parser.parse_args()
    with open(args.file[0], "r") as file:
        source = file.read()
    mylexer = lexer.Lexer(source)
    mylexer.lex()
    tokens = mylexer.tokens 
    print(tokens)

main()

if __name__ == '__main__':
    import doctest
    doctest.testmod()

