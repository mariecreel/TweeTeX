"""
lexer.py

general purpose lexer class.
"""
import re
DEBUG = False 

class Token:
    """
    takes two strings as input
    """
    def __init__(self, value, token_type):
        self.value = value
        self.token_type = token_type
        self.children = []
    def __repr__(self):
        return f"<<Token VALUE: {self.value} TYPE: {self.token_type}>>"

class Lexer:
    """
    takes a string as input
    """

    def __init__(self, text):
        self.text = text
        self.tokens = [] 
        self.token_types = { r'(\{)' : "LEFTCURLY",
                             r'(\})':"RIGHTCURLY",
                             r'(\\([a-z]+))':"COMMAND",
                             r'([^\\\{\}]+)': 'CHARACTER'}
    
    def _next_token(self, source):
        ### get string
        ### match string to each regex
        ### if match, return string to lex function
        ### and append token to self.token
        ### else, break
        string = source.lstrip()
        if DEBUG:
            print(f"string is {string}\n")
        for token in self.token_types:
            if DEBUG:
                print(f"token is {token}")
            match = re.match(token, string)
            if match and len(match.groups())>1:
                tokenobj = Token(match.group(2),self.token_types[token])
                self.tokens.append(tokenobj)
                if DEBUG:
                    print(string[len(match.group(1)):])
                result = string[len(match.group(1)):]
                return result
            elif match and len(match.groups()) is 1:
                tokenobj = Token(match.group(1), self.token_types[token])
                self.tokens.append(tokenobj)
                result = string[len(match.group(1)):]
                return result
        return False
    
    def lex(self):
        source = self.text
        if DEBUG:
            print(f"source is {source}\n")
        while len(source) != 0:
            chunk = self._next_token(source)
            if DEBUG:
                print(f"chunk is {chunk}\n")
            if chunk != False:
                source = chunk
                continue
            else:
                return False
            
