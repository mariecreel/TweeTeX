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
    def __init__(self, matchObj):
        self.value = matchObj.
        self.type = None
        self.children = []
    def getValue(self):
        return self.value
    def getType(self):
        return self.type

class Lexer:
    def __init__(self, sourcefile):
        self.filelocation = sourcefile #a filename
        self.commands = ["link", "start", "author", "title"]
        self.tokens = {r'\\ifid\{([\d]+)\}' : "IFID",
                       r'\\passage\{([^\\\{\}])\}\n[\w^"\passage"]*' : "PASSAGE",
                       r'
    def __enter__(self):
        self.sourcecode = open(self.sourcefile, "r")
    def __exit__(self):
        self.soucecode.close()
    def lex(self):
        with self.sourcecode as file:
            for line in self.sourcecode:
                for word in line:
