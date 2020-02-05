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

	>>> make_test_queue("storypass")
	[Token('author', 'PREAMBLECOMMAND', '\\author'), Token('{', 'LEFTCURLY', '{'), Token('author', 'CHARACTER', 'author'), Token('}', 'RIGHTCURLY', '}'), Token('title', 'PREAMBLECOMMAND', '\\title'), Token('{', 'LEFTCURLY', '{'), Token('title', 'CHARACTER', 'title'), Token('}', 'RIGHTCURLY', '}'), Token('ifid', 'PREAMBLECOMMAND', '\\ifid'), Token('{', 'LEFTCURLY', '{'), Token('ifid', 'CHARACTER', 'ifid'), Token('}', 'RIGHTCURLY', '}'), Token('start', 'PREAMBLECOMMAND', '\\start'), Token('{', 'LEFTCURLY', '{'), Token('first', 'CHARACTER', 'first'), Token('}', 'RIGHTCURLY', '}'), Token('passage', 'PASSAGECOMMAND', '\\passage'), Token('{', 'LEFTCURLY', '{'), Token('first', 'CHARACTER', 'first'), Token('}', 'RIGHTCURLY', '}'), Token('This is some text in a passage. ', 'CHARACTER', 'This is some text in a passage. '), Token('link', 'MACROCOMMAND', '\\link'), Token('{', 'LEFTCURLY', '{'), Token('second', 'CHARACTER', 'second'), Token('}', 'RIGHTCURLY', '}'), Token('passage', 'PASSAGECOMMAND', '\\passage'), Token('{', 'LEFTCURLY', '{'), Token('second', 'CHARACTER', 'second'), Token('}', 'RIGHTCURLY', '}'), Token('This is another passage.', 'CHARACTER', 'This is another passage.')]

	>>> make_test_queue("passage")
	[Token('passage', 'PASSAGECOMMAND', '\\passage'), Token('{', 'LEFTCURLY', '{'), Token('test', 'CHARACTER', 'test'), Token('}', 'RIGHTCURLY', '}'), Token('This is some text in a passage. ', 'CHARACTER', 'This is some text in a passage. '), Token('link', 'MACROCOMMAND', '\\link'), Token('{', 'LEFTCURLY', '{'), Token('link test', 'CHARACTER', 'link test'), Token('}', 'RIGHTCURLY', '}')]

	We should also test for a passage followed by another passage.
	>>> make_test_queue("passage2")
	[Token('passage', 'PASSAGECOMMAND', '\\passage'), Token('{', 'LEFTCURLY', '{'), Token('first', 'CHARACTER', 'first'), Token('}', 'RIGHTCURLY', '}'), Token('This is some text in a passage. ', 'CHARACTER', 'This is some text in a passage. '), Token('link', 'MACROCOMMAND', '\\link'), Token('{', 'LEFTCURLY', '{'), Token('link test', 'CHARACTER', 'link test'), Token('}', 'RIGHTCURLY', '}'), Token('passage', 'PASSAGECOMMAND', '\\passage'), Token('{', 'LEFTCURLY', '{'), Token('second', 'CHARACTER', 'second'), Token('}', 'RIGHTCURLY', '}')]

	>>> make_test_queue("preamblepass")
	[Token('author', 'PREAMBLECOMMAND', '\\author'), Token('{', 'LEFTCURLY', '{'), Token('author', 'CHARACTER', 'author'), Token('}', 'RIGHTCURLY', '}'), Token('title', 'PREAMBLECOMMAND', '\\title'), Token('{', 'LEFTCURLY', '{'), Token('title', 'CHARACTER', 'title'), Token('}', 'RIGHTCURLY', '}'), Token('ifid', 'PREAMBLECOMMAND', '\\ifid'), Token('{', 'LEFTCURLY', '{'), Token('ifid', 'CHARACTER', 'ifid'), Token('}', 'RIGHTCURLY', '}'), Token('start', 'PREAMBLECOMMAND', '\\start'), Token('{', 'LEFTCURLY', '{'), Token('start', 'CHARACTER', 'start'), Token('}', 'RIGHTCURLY', '}'), Token('passage', 'PASSAGECOMMAND', '\\passage'), Token('{', 'LEFTCURLY', '{'), Token('start', 'CHARACTER', 'start'), Token('}', 'RIGHTCURLY', '}')]
	>>> make_test_queue("preamblefail")
	[Token('author', 'PREAMBLECOMMAND', '\\author'), Token('{', 'LEFTCURLY', '{'), Token('author', 'CHARACTER', 'author'), Token('}', 'RIGHTCURLY', '}'), Token('title', 'PREAMBLECOMMAND', '\\title'), Token('{', 'LEFTCURLY', '{'), Token('title', 'CHARACTER', 'title'), Token('}', 'RIGHTCURLY', '}'), Token('ifid', 'PREAMBLECOMMAND', '\\ifid'), Token('{', 'LEFTCURLY', '{'), Token('ifid', 'CHARACTER', 'ifid'), Token('}', 'RIGHTCURLY', '}'), Token('passage', 'PASSAGECOMMAND', '\\passage'), Token('{', 'LEFTCURLY', '{'), Token('start', 'CHARACTER', 'start'), Token('}', 'RIGHTCURLY', '}')]
	>>> make_test_queue("macropass")
	[Token('link', 'MACROCOMMAND', '\\link'), Token('{', 'LEFTCURLY', '{'), Token('link_text', 'CHARACTER', 'link_text'), Token('}', 'RIGHTCURLY', '}')]

	>>> make_test_queue("macrofail")
	[Token('link', 'CHARACTER', 'link'), Token('{', 'LEFTCURLY', '{'), Token('link_text', 'CHARACTER', 'link_text'), Token('}', 'RIGHTCURLY', '}')]

	>>> make_test_queue("argumentpass")
	[Token('{', 'LEFTCURLY', '{'), Token('argument', 'CHARACTER', 'argument'), Token('}', 'RIGHTCURLY', '}')]

	>>> make_test_queue("argumentfail")
	[Token('{', 'LEFTCURLY', '{'), Token('start', 'PREAMBLECOMMAND', '\\start'), Token('{', 'LEFTCURLY', '{'), Token('start', 'CHARACTER', 'start'), Token('}', 'RIGHTCURLY', '}'), Token('}', 'RIGHTCURLY', '}')]

	>>> make_test_queue("textpass")
	[Token('This is some text in a passsage. ', 'CHARACTER', 'This is some text in a passsage. '), Token('link', 'MACROCOMMAND', '\\link'), Token('{', 'LEFTCURLY', '{'), Token('this is a link in a passage', 'CHARACTER', 'this is a link in a passage'), Token('}', 'RIGHTCURLY', '}'), Token('passage', 'PASSAGECOMMAND', '\\passage'), Token('{', 'LEFTCURLY', '{'), Token('next passage', 'CHARACTER', 'next passage'), Token('}', 'RIGHTCURLY', '}')]

	>>> make_test_queue("textfail")
	[Token('This is some text in a passsage. ', 'CHARACTER', 'This is some text in a passsage. '), Token('start', 'PREAMBLECOMMAND', '\\start'), Token('{', 'LEFTCURLY', '{'), Token('this is a preamble command', 'CHARACTER', 'this is a preamble command'), Token('}', 'RIGHTCURLY', '}'), Token('passage', 'PASSAGECOMMAND', '\\passage'), Token('{', 'LEFTCURLY', '{'), Token('next passage', 'CHARACTER', 'next passage'), Token('}', 'RIGHTCURLY', '}')]

	>>> make_test_queue("anything else")
	Sorry, that's not an acceptable input for make_test_queue.
	"""

	if kind == "passage":
		teststory = r"\passage{test} This is some text in a passage. \link{link test}"
	elif kind == "passage2":
		teststory = r"\passage{first} This is some text in a passage. \link{link test} \passage{second}"
	elif kind == "preamblepass":
		teststory = r"\author{author} \title{title} \ifid{ifid} \start{start} \passage{start}"
	elif kind == "preamblefail":
		#preamble should fail if one of the macros is missing.
		teststory = r"\author{author} \title{title} \ifid{ifid} \passage{start}"
	elif kind == "macropass":
		teststory = r"\link{link_text}"
	elif kind == "macrofail":
		teststory = r"link{link_text}"
	elif kind == "argumentpass":
		teststory = r"{argument}"
	elif kind == "argumentfail":
		teststory = "{\start{start}}"
	elif kind == "textpass":
		teststory = r"This is some text in a passsage. \link{this is a link in a passage} \passage{next passage}"
	elif kind == "textfail":
		teststory = r"This is some text in a passsage. \start{this is a preamble command} \passage{next passage}"
	elif kind == "preamblemacropass":
		teststory = r"\start{start passage}"
	elif kind == "preamblemacrofail":
		teststory = r"start{startpassage}"
	elif kind == "storypass":
		teststory = r"\author{author} \title{title} \ifid{ifid} \start{first} \passage{first} This is some text in a passage. \link{second} \passage{second} This is another passage."
	else:
		print("Sorry, that's not an acceptable input for make_test_queue.")
		return None
	testlex = lexer.Lexer(teststory)
	testlex.lex()
	return testlex.tokens

def next_token(tokenQueue):
	"""
	This function takes a queue of tokens as input and returns either a token if there is
	one in the queue, 'EOF' if there is not a token in the queue, or raises an exception
	if the token queue has become a None object (this happens whenever a function fails
	in the recursive calls).

	>>> queue = lexer.Queue()
	>>> next_token(queue)
	Token('EOF', 'EOF', 'None')

	>>> newqueue = lexer.Queue()
	>>> newqueue.enqueue(lexer.Token(token_type = "token"))
	>>> next_token(newqueue)
	Token('None', 'token', 'None')
	"""
	if tokenQueue.isEmpty():
		return lexer.Token(value = "EOF", token_type = "EOF")
	if tokenQueue != None:
		token = tokenQueue.dequeue()
		return token
	else:
		raise Exception("Token queue is None, parsing error.")

def parse(tokenQueue):
	"""
	This function creates the abstract syntax tree by calling the story function.
	If the story is parsed successfully, then ast evaluates to True and the ast
	is returned. Otherwise, parse returns False.
	"""
	ast = story(tokenQueue)
	if ast != False:
		print("Parsing complete")
		return ast
	else:
		print("Parsing failed")
		return False

def story(tokenQueue):
	"""
	The story function takes a token queue as input and returns a token if parsing
	is successful or False otherwise.
	>>> tokenQueue = make_test_queue("storypass")
	>>> _story = story(tokenQueue)
	>>> _story
	Token('None', 'STORY', 'None')

	"""
	_story = lexer.Token(token_type = "STORY")
	_preamble, tokenQueue = preamble(tokenQueue) #get the preamble
	#debug... print(tokenQueue)

	if _preamble == False: 	# if the preamble is NOT correctly formatted...
		#stop right here!
		print("Parsing Error: Preamble not formatted correctly.")
		return False
	else:										# if preamble is correctly formatted,
		_story.children.append(_preamble)        # append the preamble to the story tree.
		passages = []							# used to store all passages
		while tokenQueue.queue[0].token_type != "EOF":
			_passage, tokenQueue = passage(tokenQueue)    # get passage
			passages.append(_passage)		    # add passage to passage list
		for pas in passages:					# for each passage...
			_story.children.append(pas)			# append passage to story tree
	return _story

def preamble(tokenQueue):
	"""
	The preamble function takes a token queue as input and returns a tuple containing a
	token and a token queue if parsing is successful. Otherwise, returns the tuple
	(False, None).

    >>> _preamble, tokenQueue = preamble(make_test_queue("preamblepass"))
	>>> tokenQueue
	[Token('passage', 'PASSAGECOMMAND', '\passage'), Token('{', 'LEFTCURLY', '{'), Token('start', 'CHARACTER', 'start'), Token('}', 'RIGHTCURLY', '}')]
	>>> _preamble
	Token('None', 'PREAMBLE', 'None')
	>>> _preamble.children[0]
	Token('None', 'PREAMBLEMACRO', 'None')
	>>> _preamble.children[0].children[0]
	Token('author', 'PREAMBLECOMMAND', '\\author')
	"""

	preamble_commands = ["title", "author", "ifid", "start"]
	_preamble = lexer.Token(token_type = "PREAMBLE") 	# make preamble token
	while True:											# break this loop with returns
		token = next_token(tokenQueue)				 	# grab a token
		#print(f"in preamble, token type is {token.token_type} and value is {token.value}")
		if token.token_type == "PASSAGECOMMAND" and preamble_commands == []:
			#this should only execute if all preamble macros found...
			tokenQueue.put(token)
			#print(f"preamble is {_preamble}")
			return(_preamble, tokenQueue)
		elif token.token_type == "PASSAGECOMMAND" and preamble_commands != []:
			#if we reach a passage before we have all the required preamble commands...
			#print(f"preamble commands left: {preamble_commands}")
			#print("preamble_commands not empty, returning false in preamble")
			return(False, None)
		elif token.value not in preamble_commands or token.token_type != "PREAMBLECOMMAND":
			#if there's some input that doesn't make sense...
		#	print("input doesn't make sense, returning false in preamble")
			return(False, None)
		else:
			#if everything is kosher so far...
			#print("good so far")
			preamble_commands.pop(preamble_commands.index(token.value))
			#print(preamble_commands)
			_premacro, tokenQueue = preamblemacro(token, tokenQueue)
			if _premacro == False:
				return(False, None)
			else:
				_preamble.children.append(_premacro)

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
	Token('start', 'PREAMBLECOMMAND', '\start')

	>>> testqueue = make_test_queue("preamblemacrofail")
	>>> token = next_token(testqueue)
	>>> _premacro, tokenQueue = preamblemacro(token, testqueue)
	Parsing error: macro token not of type PREAMBLECOMMAND
	>>> _premacro
	False

	Preamblemacro cannot handle plain macros.
	>>> testqueue = make_test_queue('macropass')
	>>> token = next_token(testqueue)
	>>> _premacro, tokenQueue = preamblemacro(token, testqueue)
	Parsing error: macro token not of type PREAMBLECOMMAND
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
		#print("argument is ",_argument[0].children[0])
		if len(_argument) == 1:
			#preamble macro should only have one argument
			_preamblemacro.children.append(_argument[0])
		else:
			print("Parsing error: argument for preamble macro not formatted correctly")
			return(False, None)
	#print("returning preamble macro")
	#print(f"_preamblemacro is {_preamblemacro}")
	return(_preamblemacro, tokenQueue)

def passage(tokenQueue):
	"""
	This function takes a token queue as input and returns a tuple containing
	a token and a token queue.
	>>> tokenQueue = make_test_queue("passage")
	>>> _passage, tokenQueue = passage(tokenQueue)
	>>> tokenQueue
	[Token('EOF', 'EOF', 'None')]
	>>> _passage
	Token('None', 'PASSAGE', 'None')

	Recall that the first component of a passage is the passage command.
	>>> _passage.children[0]
	Token('passage', 'PASSAGECOMMAND', '\passage')

	Passages can be followed by other passages.
	>>> tokenQueue = make_test_queue("passage2")
	>>> _passage, tokenQueue = passage(tokenQueue)

	Second passage should remain in tokenQueue, looping happens in story function.
	>>> tokenQueue
	[Token('passage', 'PASSAGECOMMAND', '\passage'), Token('{', 'LEFTCURLY', '{'), Token('second', 'CHARACTER', 'second'), Token('}', 'RIGHTCURLY', '}')]
	>>> _passage
	Token('None', 'PASSAGE', 'None')
	"""
	token = next_token(tokenQueue)
	_passage = lexer.Token(token_type = "PASSAGE")
	_passage.children.append(token)
	#print(tokenQueue.queue)
	_argument, tokenQueue = argument(tokenQueue) #get arguments (right now just psgtitle)
	print("after return, tokenQueue is",tokenQueue)
	print("after return, _argument is",_argument)
	if _argument == False:
		print("_argument is false")
		return(False, None)
	elif len(_argument) == 1:
		_passage.children.append(_argument[0])
		token = next_token(tokenQueue)
		print("arg is len 1")
	elif len(_argument) > 1:
		for i in _argument:
			_passage.children.append(i)
		token = next_token(tokenQueue)
	print("outside of argument if statement")
	while token.token_type != "EOF" and token.token_type !="PASSAGECOMMAND":
			print("grabbing text")
			_text, tokenQueue = text(tokenQueue)
			print(f"text is {_text}")
			if _text:
				_passage.children.append(_text)
				print("appending text to passage")
				token = next_token(tokenQueue)
				print(token)
			elif _text == False:
				print("Parsing error: text in passage not correctly formatted")
				return (False, None)
			elif _text == None:
				return (_passage, tokenQueue)
	print("outside of while loop")
	print(token)
	tokenQueue.put(token)
	return (_passage, tokenQueue)

def macro(token, tokenQueue):
	"""
	This function takes a token and a token queue as input and returns a tuple containing
	a token queue and a token input.

	>>> _token = None
	>>> _macro = None
	>>> tokenQueue = None
    >>> tokenQueue = make_test_queue("macropass")
	>>> _token = next_token(tokenQueue)
	>>> _macro, tokenQueue = macro(_token, tokenQueue)
	>>> _macro
	Token('None', 'MACRO', 'None')

	>>> tokenQueue
	[Token('EOF', 'EOF', 'None')]

	Recall that the test macro is the link macro.
	>>> _macro.children[0]
	Token('link', 'MACROCOMMAND', '\link')

	Macro cannot handle a preamblemacro.
    >>>	tokenQueue = make_test_queue("preamblemacropass")
	>>> _token = next_token(tokenQueue)
	>>> _macro, tokenQueue = macro(_token, tokenQueue)
	Parsing error: macro token not of type MACROCOMMAND
	"""
	_macro = lexer.Token(token_type =  "MACRO")
	if token.token_type != "MACROCOMMAND":
		print("Parsing error: macro token not of type MACROCOMMAND")
		return (False, None)
	else:
		_macro.children.append(token)
		_argument, tokenQueue = argument(tokenQueue)
		if len(_argument) == 1:
			_macro.children.append(_argument[0])
		elif len(_argument) > 1:
			for i in _argument:
				_macro.children.append(i)
		else:
			print("Parsing error: argument for macro not formatted correctly")
			return(False, None)
	return(_macro, tokenQueue)

def argument(tokenQueue):
	"""
	This function takes a token queue as input and returns a tuple containing a list of
	tokens (which may be length 1) and a token queue.

	>>> _argument, tokenQueue = argument(make_test_queue("argumentpass"))
	>>> _argument
	[Token('None', 'ARGUMENT', 'None')]

	>>> tokenQueue
	[Token('EOF', 'EOF', 'None')]

	The list _argument contains a list of the ARGUMENT type tokens.
	>>> _argument[0]
	Token('None', 'ARGUMENT', 'None')

	Each token in this list should have children, which are the actual arguments
	contained in curly braces.
	>>> _argument[0].children[0]
	Token('argument', 'CHARACTER', 'argument')

	A preamble macro cannot be an argument.
	>>> _argument, tokenQueue = argument(make_test_queue("argumentfail"))
	Parsing Error: argument provided is not a valid argument type.
	"""

	_argument = lexer.Token(token_type = "ARGUMENT")
	token = next_token(tokenQueue)
	arguments = []

	if token.token_type == "LEFTCURLY":
		print("token is leftcurly")
		pass
	else:
		return(False, None)

	while token.token_type == "LEFTCURLY":
		anothertoken = next_token(tokenQueue)
		if anothertoken.token_type == "CHARACTER":
			_argument.children.append(anothertoken)
			anothertoken = next_token(tokenQueue)
			print("another token is",anothertoken)
			if anothertoken.token_type == "RIGHTCURLY":
				arguments.append(_argument)
				token = next_token(tokenQueue)
				print(f"token is {token}")
			else:
				print("mismatched curly braces")
				return (False, None)
		elif anothertoken.token_type == "MACROCOMMAND":
			_macro, tokenQueue = macro(token, tokenQueue)
			print(_macro.children)
			_argument.children.append(_macro)
			if _argument:
				return(_argument, tokenQueue)
		else:
			print("Parsing Error: argument provided is not a valid argument type.")
			return(False, None)
	print("outside while loop")
	print("before return, arguments is",arguments)
	tokenQueue.put(token)
	print("before return, tokenQueue is", tokenQueue.queue)
	return(arguments, tokenQueue)

def text(tokenQueue):
	"""
	Takes a tokenQueue as input. If next token is a character or a command, then
	returns a tuple with a 'TEXT' token and the original token queue. Processes all of
	the text in a passage until a new passage is reached, or until EOF.

	>>> _text, tokenQueue = text(make_test_queue("textpass"))
	>>> _text
	Token('None', 'TEXT', 'None')

	Recall that make_test_queue makes the first token a character string.
	>>> _text.children[0]
	Token('This is some text in a passsage. ', 'CHARACTER', 'This is some text in a passsage. ')

	Text cannot contain preamble macros.
	>>> _text, tokenQueue = text(make_test_queue("textfail"))
	Parsing failed: preamble command in passage text
	>>> _text
	False
	"""
	_text = lexer.Token(token_type = "TEXT")
	token = next_token(tokenQueue)
	while token.token_type != "PASSAGECOMAMAND" and token.token_type != "EOF":
		if token.token_type == "CHARACTER":
			_text.children.append(token)
		elif token.token_type == "MACROCOMMAND":
			_macro, tokenQueue = macro(token, tokenQueue)
			#print(f"_macro is {_macro}")
			if _macro != False:
				_text.children.append(_macro)
			else:
				print("macro failed")
				return(False, None)
		elif token.token_type == "PREAMBLECOMMAND":
			print("Parsing failed: preamble command in passage text")
			return(False, None)
		else:
			tokenQueue.put(token)
			return(_text, tokenQueue)
		token = next_token(tokenQueue)
	tokenQueue.put(token)
	return(_text, tokenQueue)


if __name__ == "__main__":
	import doctest
	doctest.testmod()


