"""
basictweetexlexer.py

This lexer is written to recognize basic tweetex syntax elements.
Here's a grammar of what it's meant to recognize.

Note: in EBNF, { anything in curly braces repeats,} so I've put parenthesis
around curly braces that I want to actually see in the source code.
This grammar was revised with great help from Jim.

<story> :== <preamble> <passage>+
<preamble> :== <id> <macro>*
<id> := "\ifid{" [\w]+ "}"
<macro> :== "\" <command> [ "{" <argument> "}" ]*
<command> :== "link" | "start" | "author" | "title"
<passage> :== "\passage" { "{" <argument> "}" } <text>
<char> :== [^\\\{\}]
<argument> :== <char>+ | <macro>
<text> :== <char>* {<macro>} {<text>}


    -- lexer --
    COMMAND     (including backslash)
    LEFTCURLY
    RIGHTCURLY
    CHARACTERS

    --- parser ---
    ... recursive stuff ...


And here's an example of a correctly written tweetex document.

\title{My Story}
\author{Nick Creel}
\ifid{0CA8C7C5-F219-4B1B-A3A8-45710F389818}
\start{Starting Passage}

\passage{Starting Passage}
This is some text in the first passage
\link{Second Passage}{This link goes to the second passage}

\passage{Second Passage}
This is some text in the second passage.

"""

class Token:
    """ tokens need to have a value for evaluation, and a type for parsing.
        the value should come directly from the string of input. the type
        should come from the name of the regular expression used to match.
        (they are written in a way that the regex names match the type names)"""
    def __init__(self, matchObj, type):
        self.value = matchObj
        self.type = None
        self.children = []
    def getValue(self):
        return self.value
    def getType(self):
        return self.type

class Lexer:
    def __init__(self, filelocation):
        self.filelocation = filelocation #a filename
        self.commands = ["link", "start", "author", "title", "ifid"]
        self.tokens = {r'\{'                : "LEFTCURLY",
                       r'\}'                : "RIGHTCURLY",
                       r'\\[a-z]+'          : "COMMAND", #one slash and some text
                       r'[^\\\{\}]'         : "CHARACTERS"} #anything that isn't a delimiter
                                                            #or a command
    def __enter__(self):
        self.sourcecode = open(self.filelocation, "r")

    def __exit__(self):
        self.soucecode.close()

    def lex(self):
        result = []
        with self.sourcecode as file:
            for line in self.sourcecode:
                for word in line:
                    for key, val in self.tokens:
                        match = re.match(key, word)
                        if match:
                            token = Token(match, val)
                            result.append(token)
                        else:
                            print("Lexical Error: The input provided does not fit\
                                  the syntactical specification of TweeTeX.\n\n")
                            return None
        return result

def main():
    filename =

if __name__ == "__main__":
    import doctest
