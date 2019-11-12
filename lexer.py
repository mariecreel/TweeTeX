"""
lexer.py

general purpose lexer class.

nick creel | nov 12 2019 | mit license
"""
import re

class Token:
    """
    A token is an object with four attributes:

    Value = the value used when evaluating an input
    Token Type = The token assigned to that value during lexing.
        There are four valid types: LEFTCURLY, RIGHTCURLY, COMMAND,
        and CHARACTER.
    Match = the exact string which matched to the token type 
            during lexing
    Children = assigned during parsing, the tokens which recursively
               follow from the current token based on the grammar
               (eg COMMAND -> PASSAGE -> TEXT)

    Technically, a token may take any three strings as input,
    but if the input falls out of the grammar specified,
    then there will be errors during parsing. Generally,
    these should only be created by the lexer object to avoid
    problems in parsing. 

    >>> Token('{', 'LEFTCURLY', '{')
    Token('{', 'LEFTCURLY', '{')
    >>> Token('}', 'RIGHTCURLY', '}')
    Token('}', 'RIGHTCURLY', '}')
    >>> Token('hello', 'COMMAND', '\hello')
    Token('hello', 'COMMAND', '\hello')
    >>> Token('hello', 'CHARACTER', 'hello')
    Token('hello', 'CHARACTER', 'hello')
    """

    def __init__(self, value, token_type, match):
        self.value = value
        self.token_type = token_type
        self.children = []
        self.match = match

    def __repr__(self):
        return f"Token('{self.value}', '{self.token_type}', '{self.match}')"

class Lexer:
    """
    Lexer is an object which takes the contents of a source file as
    input and tokenizes the input based on the TweeTeX specification.
    Note: A lexer must be initialized with its source file as an 
    input, then the lex method may be called.

    A lexer object has three attributes:
    text = the source file contents
    tokens = list of tokens generated during lexing
    token_types = legal set of tokens which can be recognized, and 
                  corresponding regular expressions
    >>> mylexer = Lexer("hello")
    >>> mylexer.lex()
    >>> mylexer.tokens
    [Token('hello', 'CHARACTER', 'hello')]
    >>> mylexer = Lexer("\hello")
    >>> mylexer.lex()
    >>> mylexer.tokens
    [Token('hello', 'COMMAND', '\hello')]
    """

    def __init__(self, text):
        self.text = text
        self.tokens = [] 
        self.token_types = { r'(\{)' : "LEFTCURLY",
                             r'(\})':"RIGHTCURLY",
                             r'(\\([a-z]+))':"COMMAND",
                             r'([^\\\{\}]+)': 'CHARACTER'}
    
    def _next_token(self, source):
        string = source.lstrip()
        for token in self.token_types:
            match = re.match(token, string)
            if match and len(match.groups())==2:
                tokenobj = Token(match.group(2),self.token_types[token], match.group(1))
                self.tokens.append(tokenobj)
                result = string[len(match.group(1)):]
                return result
            elif match and len(match.groups()) is 1:
                tokenobj = Token(match.group(1), self.token_types[token], match.group(1))
                self.tokens.append(tokenobj)
                result = string[len(match.group(1)):]
                return result
        return False
    
    def lex(self):
        source = self.text
        while len(source) != 0:
            chunk = self._next_token(source)
            if chunk != False:
                source = chunk
                continue
            else:
                return False

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose = True)
