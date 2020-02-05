"""
lexer.py

general purpose lexer class.

Nick Creel | Feb 5 2020 | MIT License
"""
import re
## TODO: make some simple test story function that makes a simple story for testing...

class Queue:
	""" Mostly a standard FIFO queue, with the option of put()ting something in 0th
		position like a stack."""
	def __init__(self):
		self.queue = []
	def __repr__(self):
		return f"{self.queue}"
	def enqueue(self, something):
		self.queue.append(something)
	def dequeue(self):
		return self.queue.pop(0)
	def put(self, something):
		self.queue.insert(0, something)
	def isEmpty(self):
		if self.queue:
			return False
		else:
			return True

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
    >>> Token('link', 'MACROCOMMAND', '\link')
    Token('link', 'MACROCOMMAND', '\link')
    >>> Token('start', 'PREAMBLECOMMAND', '\start')
    Token('start', 'PREAMBLECOMMAND', '\start')
    >>> Token('\passage', 'PASSAGECOMMAND', '\passage')
    Token('\passage', 'PASSAGECOMMAND', '\passage')
    >>> Token('hello', 'CHARACTER', 'hello')
    Token('hello', 'CHARACTER', 'hello')
    """

    def __init__(self, value = None, token_type = None, match = None):
        # i just made these all none because I didn't want to rearrange
        # all my examples...
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
    >>> mylexer = Lexer("\link")
    >>> mylexer.lex()
    >>> mylexer.tokens
    [Token('link', 'MACROCOMMAND', '\link')]
    """
    # MACROCOMMANDS = ["link"]
    # PREAMBLECOMMANDS = ["author", "title", "start", "ifid"]
    # there's probably some way to insert a list of strings into a regular expression...

    def __init__(self, text):
        self.text = text
        self.tokens = Queue()
        self.token_types = { r'(\{)' : "LEFTCURLY",
                             r'(\})':"RIGHTCURLY",
                             r'(\\(link))':"MACROCOMMAND",
                             r'(\\(author|title|ifid|start))':"PREAMBLECOMMAND",
                             r'(\\(passage))':"PASSAGECOMMAND",
                             r'([^\\\{\}]+)': 'CHARACTER'}

    def _next_token(self, source):
        string = source.lstrip()
        for token in self.token_types:
            match = re.match(token, string)
            if match and len(match.groups())==2:
                tokenobj = Token(match.group(2),self.token_types[token], match.group(1))
                self.tokens.enqueue(tokenobj)
                result = string[len(match.group(1)):]
                return result
            elif match and len(match.groups()) is 1:
                tokenobj = Token(match.group(1), self.token_types[token], match.group(1))
                self.tokens.enqueue(tokenobj)
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
