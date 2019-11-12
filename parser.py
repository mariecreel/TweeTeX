"""
parser.py
simple parsing library
"""

class Parser:
    '''
    takes a list of tokens as input, 
    returns abstract syntax tree
    '''
    def __init__(self, list_of_tokens):
        self.tokens = list_of_tokens
        self.ast = []
        self.rules = {}

