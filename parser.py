"""
parser.py

Simple parsing library for the TweeTeX programming language. The
specification below describes the grammar of the language, and each
item on the left side of the :== has its own function. This parser
follows the framework of a recursive descent parser, where a top level
function repeatedly calls subsequent function until each piece of the
input is matched to a terminal symbol in the grammar.

In the TweeTeX compiler, this parser takes the output of the Lexer library
as input and returns an abstract syntax tree, or AST. The tree is built of
Token objects, which are defined in the Lexer library, and each Token object
is a node in the tree. A branch on the tree terminates when the Token object
has no children. Each of the functions below should create at least one branch
for the tree, and branches are added by subsequent function calls.

spec:

<story> :== <preamble> <passage>+
<preamble> :== "\" <preamblecommand> <argument> {"\" <preamblecommand> <argument>}
<macro> :== "\" <macrocommand>  <argument>*
<preamblecommand> :== "start" | "author" | "title" | "ifid"
<macrocommand> :== "link" ## more soon?
<passage> :== "\passage" { <argument> } <text>
<char> :== [^\\\{\}]
<argument> :== "{" (<char>+ | <macro>) "}"
<text> :== <char>* {<macro>} {<text>}

Nick Creel | Feb 2 2020 | MIT License
"""
import lexer #we need this mostly for the Token object, and testing.

def make_test_queue(kind):
	"""
	Makes a test tokenQueue to be used in doctests depending on the
	function in question.
	Acceptable input: "passage", "preamble", "macro", "argument", or "text".

	>>> make_test_queue("passage")
	[Token('passage', 'PASSAGECOMMAND', '\passage'), Token('{', 'LEFTCURLY', '{'), Token('test', 'CHARACTER', 'test'), Token('}', 'RIGHTCURLY', '}'), Token('This is some text in a passage. ', 'CHARACTER', 'This is some text in a passage. '), Token('link', 'MACROCOMMAND', '\link'), Token('{', 'LEFTCURLY', '{'), Token('link test', 'CHARACTER', 'link test'), Token('}', 'RIGHTCURLY', '}')]

	We should also test for a passage followed by another passage.
	>>> make_test_queue("passage2")
	[Token('passage', 'PASSAGECOMMAND', '\passage'), Token('{', 'LEFTCURLY', '{'), Token('first', 'CHARACTER', 'first'), Token('}', 'RIGHTCURLY', '}'), Token('This is some text in a passage. ', 'CHARACTER', 'This is some text in a passage. '), Token('link', 'MACROCOMMAND', '\link'), Token('{', 'LEFTCURLY', '{'), Token('link test', 'CHARACTER', 'link test'), Token('}', 'RIGHTCURLY', '}'), Token('passage', 'PASSAGECOMMAND', '\passage'), Token('{', 'LEFTCURLY', '{'), Token('second', 'CHARACTER', 'second'), Token('}', 'RIGHTCURLY', '}')]

	>>> make_test_queue("preamblepass")
	[Token('author', 'PREAMBLECOMMAND', '\author'), Token('{', 'LEFTCURLY', '{'), Token('author', 'CHARACTER', 'author'), Token('}', 'RIGHTCURLY', '}'), Token('title', 'PREAMBLECOMMAND', '\title'), Token('{', 'LEFTCURLY', '{'), Token('title', 'CHARACTER', 'title'), Token('}', 'RIGHTCURLY', '}'), Token('ifid', 'PREAMBLECOMMAND', '\ifid'), Token('{', 'LEFTCURLY', '{'), Token('ifid', 'CHARACTER', 'ifid'), Token('}', 'RIGHTCURLY', '}'), Token('start', 'PREAMBLECOMMAND', '\start'), Token('{', 'LEFTCURLY', '{'), Token('start', 'CHARACTER', 'start'), Token('}', 'RIGHTCURLY', '}')]

	>>> make_test_queue("preamblefail")
	[Token('author', 'PREAMBLECOMMAND', '\author'), Token('{', 'LEFTCURLY', '{'), Token('author', 'CHARACTER', 'author'), Token('}', 'RIGHTCURLY', '}'), Token('title', 'PREAMBLECOMMAND', '\title'), Token('{', 'LEFTCURLY', '{'), Token('title', 'CHARACTER', 'title'), Token('}', 'RIGHTCURLY', '}'), Token('ifid', 'PREAMBLECOMMAND', '\ifid'), Token('{', 'LEFTCURLY', '{'), Token('ifid', 'CHARACTER', 'ifid'), Token('}', 'RIGHTCURLY', '}')]

	>>> make_test_queue("macropass")
	[Token('link', 'MACROCOMMAND', '\link'), Token('{', 'LEFTCURLY', '{'), Token('link_text', 'CHARACTER', 'link_text'), Token('}', 'RIGHTCURLY', '}')]

	>>> make_test_queue("macrofail")
	[Token('link', 'CHARACTER', 'link'), Token('{', 'LEFTCURLY', '{'), Token('link_text', 'CHARACTER', 'link_text'), Token('}', 'RIGHTCURLY', '}')]

	>>> make_test_queue("argumentpass")
	[Token('{', 'LEFTCURLY', '{'), Token('argument', 'CHARACTER', 'argument'), Token('}', 'RIGHTCURLY', '}')]

	>>> make_test_queue("arguentfail")
	[Token('argument', 'CHARACTER', 'argument'), Token('}', 'RIGHTCURLY', '}')]

	>>> make_test_queue("textpass")
	[Token('This is some text in a passsage. ', 'CHARACTER', 'This is some text in a passsage. '), Token('link', 'MACROCOMMAND', '\link'), Token('{', 'LEFTCURLY', '{'), Token('this is a link in a passage', 'CHARACTER', 'this is a link in a passage'), Token('}', 'RIGHTCURLY', '}'), Token('passage', 'PASSAGECOMMAND', '\passage'), Token('{', 'LEFTCURLY', '{'), Token('next passage', 'CHARACTER', 'next passage'), Token('}', 'RIGHTCURLY', '}')]

	>>> make_test_queue("textfail")
	[Token('This is some text in a passsage. ', 'CHARACTER', 'This is some text in a passsage. '), Token('start', 'PREAMBLECOMMAND', '\start'), Token('{', 'LEFTCURLY', '{'), Token('this is a preamble command', 'CHARACTER', 'this is a preamble command'), Token('}', 'RIGHTCURLY', '}'), Token('passage', 'PASSAGECOMMAND', '\passage'), Token('{', 'LEFTCURLY', '{'), Token('next passage', 'CHARACTER', 'next passage'), Token('}', 'RIGHTCURLY', '}')]

	>>> make_test_queue("anything else")
	Sorry, that's not an acceptable input for make_test_queue.
	"""

	if kind == "passage":
		teststory = r"\passage{test} This is some text in a passage. \link{link test}"
	elif kind == "passage2":
		teststory = r"\passage{first} This is some text in a passage. \link{link test} \passage{second}"
	elif kind == "preamblepass":
		teststory = r"\author{author} \title{title} \ifid{ifid} \start{start}"
	elif kind == "preamblefail":
		#preamble should fail if one of the macros is missing.
		teststory = r"\author{author} \title{title} \ifid{ifid}"
	elif kind == "macropass":
		teststory = r"\link{link_text}"
	elif kind == "macrofail":
		teststory = r"link{link_text}"
	elif kind == "argumentpass":
		teststory = r"{argument}"
	elif kind == "argumentfail":
		teststory = "argument}"
	elif kind == "textpass":
		teststory = r"This is some text in a passsage. \link{this is a link in a passage} \passage{next passage}"
	elif kind == "textfail":
		teststory = r"This is some text in a passsage. \start{this is a preamble command} \passage{next passage}"
	elif kind ="preamblemacropass":
		teststory = r"\start{start passage}"
	elif kind = "preamblemacrofail":
		teststory = r"start{startpassage}"
	else:
		print("Sorry, that's not an acceptble input for make_test_queue.")
		return None
	testlex = lexer.Lexer(teststory)
	testlex.lex()
	return testlex.tokens

def next_token(tokenQueue):
	"""
	This function takes a queue of tokens as input and dequeues a token from
	that queue if there is a token available. Once the token has been dequeued,
	the function returns that token. If there is no token to dequeue, then
	a special token with the value 'EOF' is returned. If there is some error
	in parsing and the token queue is a None object, then an exception is raised.
	The tokenQueue is not returned.
	"""
	print(f"tokens remaining == {len(tokenQueue.queue)}")
	if tokenQueue.isEmpty():
		return lexer.Token(value = "EOF")
	if tokenQueue != None:
		token = tokenQueue.dequeue()
		print(f"in tokenqueue, token is {token}")
		return token
	raise Exception("Token queue is None, parsing error.")

def parse(tokenQueue):
	"""
	This function creates the abstract syntax tree by calling the story function.
	If the story is parsed successfully, then ast evaluates to True and the ast
	is returned. Otherwise, parse returns False.
	"""
	ast = story(tokenQueue)
	if ast:
		return ast
	else:
		return False

def story(tokenQueue):
	"""
	The story function takes a token queue as input and returns a token if parsing
	is successful or False otherwise.
	"""
	story = lexer.Token(token_type = "STORY")
	_preamble, tokenQueue = preamble(tokenQueue) #get the preamble
	#debug... print(tokenQueue)

	if _preamble == False: 	# if the preamble is NOT correctly formatted...
		#stop right here!
		print("Parsing Error: Preamble not formatted correctly.")
		return False
	else:										# if preamble is correctly formatted,
		story.children.append(_preamble)        # append the preamble to the story tree.
		passages = []							# used to store all passages
		while tokenQueue.isEmpty() == False:    # While we haven't reached EOF...
			_passage, tokenQueue = passage(tokenQueue)    # get passage
			passages.append(_passage)		    # add passage to passage list
		for pas in passages:					# for each passage...
			story.children.append(pas)			# append passage to story tree
		return story

def preamble(tokenQueue):
	"""
	The preamble function takes a token queue as input and returns a tuple containing a
	token and a token queue if parsing is successful. Otherwise, returns the tuple
	(False, None).

	>>> _preamble, tokenQueue = preamble(make_test_queue("preamble"))

	>>> tokenQueue
	[]

	>>> _preamble
	Token('None', 'PREAMBLE', 'None')

	>>> _preamble.children[0]
	Token('None', 'MACRO', 'None')

	Recall that the test macro made by make_test_queue is an author command.
	>>> _preamble.children[0].children[0]
	Token('author', 'PREAMBLECOMMAND', '\author')
	"""
	# right now, the order of preamble commands does not affect parsing.
	# spec only says at least one macro is present, need to make clear that
	# specific macros are necessary to include in the preamble, without
	# enforcing order...
	# I don't think the order should matter really, as the preamble is mostly
	# metadata about the story, and not establishing any new scope where
	# any order of operations matters.
	preamble_commands = ["title", "author", "ifid", "start"]
	_preamble = lexer.Token(token_type = "PREAMBLE") 	# make preamble token
	while True:											# break this loop with returns
		token = next_token(tokenQueue)				 	# grab a token
		if token.token_type == "PREAMBLECOMMAND" and preamble_commands == []:
			#this should only execute if all preamble macros found...
			tokenQueue.put(token)
			return(_preamble, tokenQueue)
		elif token.token_type == "PASSAGECOMMAND" and preamble_commands != []:
			#if we reach a passage before we have all the required preamble commands...
			return(False, None)
		elif token.value not in PREAMBLE_COMMANDS and token.token_type != "PREAMBLECOMMAND":
			#if there's some input that doesn't make sense...
			return(False, None)
		else:
			#if everything is kosher so far...
			_premacro, tokenQueue = preamblemacro(token, tokenQueue)
			if _premacro == False:
				return(False, None)
			elif _premacro.value == in preamble_commands:
				preamble_commands.pop(preamble_commands.index(_premacro.value))
				_preamble.children.append(_macro)

def preamblemacro(token, tokenQueue):
	"""
	takes a token and a token queue as input, returns a tuple containing a token and a
	token queue.
	>>> testqueue = make_test_queue('preamblemacropass')
	>>> token = next_token(testqueue)
	>>> _premacro, tokenQueue = preamblemacro(token, testqueue)
	>>> _premacro
	Token('None', 'PREAMBLEMACRO', 'None')
	>>> _premacro.children[0]
	Token('preamble', 'PREAMBLECOMMAND', '\preamble')

	>>> testqueue = make_test_queue("preamblemacrofail")
	>>> token = next_token(testqueue)
	>>> _premacro, tokenQueue = preamblemacro(token, testqueue)
	>>> _premacro
	False

	>>> testqueue = make_test_queue('macropass')
	>>> token = next_token(testqueue)
	>>> _premacro, tokenQueue = preamblemacro(token, testqueue)
	>>> _premacro
	False
	"""
	_preamblemacro = lexer.Token(token_type =  "PREAMBLEMACRO")
	if token.token_type != "PREAMBLECOMMAND":
		print("Parsing error: macro token not of type PREAMBLECOMMAND")
		return (False, None)
	else:
		_preamblemacro.children.append(token)
		_argument, tokenQueue = argument(tokenQueue)
		print("argument is ",_argument)
		if len(_argument) == 1:
			#preamble macro should only have one argument
			_macro.children.append(_argument[0])
		else:
			print("argument for preamble macro not formatted correctly")
			return(False, None)
	print("returning preamble macro")
	return(_preamblemacro, tokenQueue)
def passage(tokenQueue):
	"""
	This function takes a token queue as input and returns a tuple containing
	a token and a token queue.

	>>> _passage, tokenQueue = passage(make_test_queue("passage"))
	>>> tokenQueue
	[]
	>>> _passage
	Token('None', 'PASSAGE', 'None')

	Recall that the first component of a passage is the passage command.
	>>> _passage.children[0]
	Token('passage', 'PASSAGECOMMAND', '\passage')

	Passages can be followed by other passages.
	>>> _passage, tokenQueue = passage(make_test_queue("passage2"))

	Second passage should remain in tokenQueue, looping happens in story function.
	>>> tokenQueue
	[Token('passage', 'PASSAGECOMMAND', 'passage'), Token('{', 'LEFTCURLY', '{'), Token('second', 'CHARACTER', 'second', Token('}', 'RIGHTCURLY', '}')]

	>>> _passage
	Token('None', 'PASSAGE', 'None')

	"""
	token = next_token(tokenQueue)
	#debug print(f"in passage, token value is {token.value}, type is {token.token_type}")
	while token.value != "EOF":
		if token.token_type == "PASSAGECOMMAND":
			_passage = lexer.Token(token_type = "PASSAGE")
			while token.token_type != "CHARACTER": # handle arguments
				print("in passage while loop, ", token, token.token_type)
				_argument, tokenQueue = argument(tokenQueue)
				if len(_argument) == 1:
					_passage.children.append(_argument[0])
					token = next_token(tokenQueue)
				elif len(_argument) > 1:
					for i in _argument:
						_passage.children.append(i)
					token = next_token(tokenQueue)
				else:
					print("Parsing error: passage argument not correctly formatted")
					return (False, None)
			while token.value != ("passage" or "EOF"): # grab text
				_text, tokenQueue = text(tokenQueue)
				if _text:
					_passage.children.append(_text)
					token = next_token(tokenQueue)
					print("if _text, ", token.value)
				elif _text == False:
					print("Parsing error: text in passage not correctly formatted")
					return (False, None)
				elif _text == None:
					return (_passage, tokenQueue)
			else:
				print("in else statement of grab text")
				if token.token_type == "PASSAGECOMMAND":
					tokenQueue.put(token)

			return (_passage, tokenQueue)
	else:
		return (_passage, tokenQueue)

def macro(token, tokenQueue):
	"""
	This function takes a token and a token queue as input and returns a tuple containing
	a token queue and a token input.

	>>>	tokenQueue = make_test_queue("macro")

	>>> _token = next_token(tokenQueue)

	>>> _macro, tokenQueue = macro(_token, tokenQueue)

	>>> _macro
	Token('None', 'MACRO', 'None')

	>>> tokenQueue
	[]

	Recall that the test macro is the link macro.
	>>> _macro.children[0]
	Token('link', 'MACROCOMMAND', '\link')
	"""
	_macro = lexer.Token(token_type =  "MACRO")
	if token.token_type != "MACROCOMMAND":
		print("Parsing error: macro token not of type MACROCOMMAND")
		return (False, None)
	else:
		_macro.children.append(token)
		_argument, tokenQueue = argument(tokenQueue)
		print("argument is ",_argument)
		if len(_argument) == 1:
			_macro.children.append(_argument[0])
		elif len(_argument) > 1:
			for i in _argument:
				_macro.children.append(i)
		else:
			print("argument for macro not formatted correctly")
			return(False, None)
	print("returning macro")
	return(_macro, tokenQueue)

def argument(tokenQueue):
	"""
	This function takes a token queue as input and returns a tuple containing a token
	and a token queue.

	>>> _argument, tokenQueue = argument(make_test_queue("argument"))
	>>> _argument
	Token('None', 'ARGUMENT', 'None')

	>>> tokenQueue
	[]

	Recall that the first component of an argument is a left curly brace.
	>>> _argument.children[0]
	Token('{', 'LEFTCURLY', '}')

	"""

	_argument = lexer.Token(token_type = "ARGUMENT")
	token = next_token(tokenQueue)
	print(f"in arg after next token, token.token_type is {token.token_type}")
	print(f"token.value is {token.value}")
	arguments = []

	if token.token_type == "LEFTCURLY":
		pass
	else:
		return(False, None)

	while token.token_type == "LEFTCURLY":
		anothertoken = next_token(tokenQueue)
		if anothertoken.token_type == "CHARACTER":
			print(f"appending text to argument.children, value is {anothertoken.value}")
			_argument.children.append(anothertoken)
			anothertoken = next_token(tokenQueue)
			print(f"looking for right curly, token type is {anothertoken.token_type}")
			if anothertoken.token_type == "RIGHTCURLY":
				print(_argument, _argument.children)
				arguments.append(_argument)
				token = next_token(tokenQueue)
			else:
				print("no right curly")
				return (False, None)
		elif anothertoken.token_type == "MACROCOMMAND":
			print(f"running MACRO, token.value is {token.value}")
			_macro, tokenQueue = macro(token, tokenQueue)
			print(_macro.children)
			_argument.children.append(_macro)
			if _argument:
				return(_argument, tokenQueue)
	tokenQueue.put(token)
	return(arguments, tokenQueue)

def text(tokenQueue):
	"""
	Takes a tokenQueue as input. If next token is a character or a command, then
	returns a tuple with a 'TEXT' token and the original token queue. Processes all of
	the text in a passage until a new passage is reached, or until EOF.


	"""
	_text = lexer.Token(token_type = "TEXT")
	token = next_token(tokenQueue)
	while token.value != "passage" or token.value != "EOF":
		if token.token_type == "CHARACTER":
			print("appending text to _text")
			_text.children.append(token)
			token = next_token(tokenQueue)
		elif token.token_type == "MACROCOMMAND":
			print("running macro for _macro in text")
			_macro, tokenQueue = macro(token, tokenQueue)
			if _macro:
				_text.children.append(_macro)
				token = next_token(tokenQueue)
	tokenQueue.put(token)
	print("done with text")
	return(_text, tokenQueue)




