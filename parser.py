"""
parser.py

simple parsing library

nick creel | nov 19 2019 | mit license
"""
from lexer import Token

class Parser:
    '''
    A parser is an object that takes a list of Token objects as input
    and parses input according to the TweeTeX grammar.
    '''
    # TODO put some doctests here

    def __init__(self, list_of_tokens):
        self.tokens = list_of_tokens
        self.ast = None 
        self.preamble_commands = ["ifid", "title", "story", "author"]
        self.macro_commands = ["link"] 
        self.current = None 
        self.next = None
    

    def next_token(self):
        try:
            token1 = self.tokens.pop(0)
        except IndexError:
            token1 = None # this should only happen once 
                          # list is exhausted
        if self.current == None and self.next == None:
            # initializing current and next
            token2 = self.tokens.pop(0)
            self.current = token1
            self.next = token2
        elif self.current != None:
            # swapping current and next
            self.current = self.next
            self.next = token1

    def parse(self):
        self.next_token() # init
        self.ast = self.story() # call top level func.
        return self.ast

    def story(self):
        story = Token(, "STORY", )
        if self.current.value in self.preamble_commands:
            story.children  = self.preamble()
        elif self.current.value not in self.preamble_commands:
            # might be unecessary but just to be sure,
            # I'm verifying that all the required components
            # are there, as the preamble function does not.
            # this could possibly be moved to the preamble
            # function but right now it makes sense for it
            # to be here. 
            preamble_check = {
                    "ifid": False,
                    "author":False,
                    "title":False,
                    "start":False
                    }
            for token in story.children:
                if token.value in self.preamble_commands:
                    preamble_check[token.value] = True
            if all(value == True for value in preamble_check):
                # we can only start on passages once 
                # preamble is done. SO preamble
                # must always be at the top. 
                story = self.passage()
            else:
                raise Exception("Parse error: Preamble is missing required components.")
        return story

    def preamble(self):
        '''
        preamble: iterates through token list to find all
        of the preamble macros and store their values as 
        children of the story object.
        
        '''
        preamble = Token(, "PREAMBLE", )
        isdone = False
        while isdone == False:
            if (self.current.token_type is "COMMAND" and
            self.current.value in self.preamble_comands):
                macro = Token(,"MACRO",)
                command = self.current_token
                self.new_token() 
                #should make current.token_type  LEFTCURLY
                arg = self.argument()
                macro.children.append(command)
                macro.children.append(arg)
                preamble.children.append(macro)
            else:
                isdone = True
        return preamble

    def passage(self):
        # TODO put in descriptions and doctests
        if (self.token_type == "COMMAND" and 
        self.current.value == "passage"):
            passage = Token(, "PASSAGE", )
            self.next_token()
            while self.current.value != "passage":
                # go until we reach the next passage
                if self.current.token_type == "LEFTCURLY":
                    arg = self.argument()
                    passage.children.append(arg)
                    continue
                elif self.current.token_type == "COMMAND":
                    macro = self.macro()
                    passage.children.append(arg)
                    continue
                elif self.current.token_type == "CHARACTER":
                    # this is essentially terminal so I'm
                    # handling it here rather than making
                    # another f(x)n. 
                    text = Token(self.current.value, "TEXT", )
                    passage.children.append(text)
                    continue
                elif self.current = None:
                    # we've reached the end of the document
                    # this is a valid way to end a passage...
                    # in fact, one of the passages will 
                    # always end this way.
                    break
                else:
                    raise Exception("Parsing error:") #not sure

        return passage

    def macro(self):
        # TODO add doctests. should be simple.
        macro = Token(, "MACRO", )
        if self.current.value in self.macro_commands:
            # is this a macro we know?
            macro.children.append(self.current)
            self.next_token()
            while self.current.token_type != "CHARACTER":
                # characters should never be encountered
                # on their own out here if they are passed
                # as an argument. Otherwise, we've reached
                # the text of the passage.
                if self.current.token_type == "LEFTCURLY":
                    arg = self.argument()
                    macro.children.append(arg)
                    continue
                else:
                    raise Exception("Parsing error: Macro provided without at least one argument."
        else:
            raise Exception("Parsing error: reference to unsupported macro.")
        return macro   

    def arg(self):
        # TODO add doctests
        arg = Token(, "ARGUMENT", )
        self.next_token() # makes current token the text of arg
        if self.current.token_type == "COMMAND":
            macro = self.macro()
            arg.children.append(macro)
        else:    
            arg.children.append(self.current)

        if self.next.token_type == "RIGHTCURLY":
            self.next_token()

        else:
            raise Exception("Parsing error: Mismatched Curly Braces")
        return arg

