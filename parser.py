"""
parser.py

simple parsing library

spec:

<story> :== <preamble> <passage>+
<preamble> :== <macro>+ !-- this has to have IFID at least --!
<macro> :== "\" <command>  <argument>*
<command> :== "link" | "start" | "author" | "title" | "ifid"
<passage> :== "\passage" { <argument> } <text>
<char> :== [^\\\{\}]
<argument> :== "{" (<char>+ | <macro>) "}"
<text> :== <char>* {<macro>} {<text>}

nick creel | nov 26 2019 | mit license

"""
import lexer
MACRO_COMMANDS = ["ifid", "title", "start", "author", "link"]
PREAMBLE_COMMANDS = MACRO_COMMANDS[0:4]

def next_token(tokenQueue):
	print(f"tokens remaining == {len(tokenQueue.queue)}")
	if tokenQueue.isEmpty():
		return lexer.Token(value = "EOF")
	if tokenQueue != None:
		token = tokenQueue.dequeue()
		print(f"in tokenqueue, token is {token}")
		return token
	raise Exception("Token queue is None, parsing error.")
	
def parse(tokenQueue):
	ast = story(tokenQueue)
	if ast:
		return ast
	else:
		return False

def story(tokenQueue):
	story = lexer.Token(token_type = "STORY")
	_preamble = None
	#print("in story before preamble")
	_preamble, tokenQueue = preamble(tokenQueue)
	print(tokenQueue)
	
	#-- debug
	#print("printing preamble children")
	#for i in _preamble.children:
	#	print(i.token_type)
	#	for j in i.children:
	#		print(j)
		
	#print("in story after preamble")
	if _preamble != False:
		story.children.append(_preamble)
		passages = []
		#print(tokenQueue.isEmpty())
		while tokenQueue.isEmpty() == False:
			_passage, tokenQueue = passage(tokenQueue)
			print("passage is", _passage)
			passages.append(_passage)
	else:
		return False
	print("in story before passages")
	for pas in passages:
		print(pas)
		story.children.append(pas)
	return story

def preamble(tokenQueue):
	_preamble = lexer.Token(token_type = "PREAMBLE")
	_pretest = True
	token = next_token(tokenQueue)
	while token.value in PREAMBLE_COMMANDS and token.token_type == "COMMAND":
		#print(f"in while loop of preamble, token.value is {token.value}")
		_macro, tokenQueue = macro(token, tokenQueue)
		#print(f"in while loop, _macro is {_macro}")
		if _macro != False:
			_preamble.children.append(_macro)
		else:
			return(False, None)
		token = next_token(tokenQueue)
		#print(f"after next token in preamble, token.value is {token.value}")
		print(PREAMBLE_COMMANDS)
		#print(f"is token value in PREAMBLE_COMMANDS? {token.value in PREAMBLE_COMMANDS}")
		#print(f"is token type COMMAND? {token.token_type == 'COMMAND'}")
	if token.value == "passage":
		tokenQueue.put(token)
	return(_preamble, tokenQueue)
	
def passage(tokenQueue):
	token = next_token(tokenQueue)
	print(f"in passage, token value is {token.value}, type is {token.token_type}")
	while token.value != "EOF":
		if token.value == "passage":
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
				if token.value == "passage":
					tokenQueue.put(token)
				
			return (_passage, tokenQueue)
	else:
		return (_passage, tokenQueue)

def macro(token, tokenQueue): 
	_macro = lexer.Token(token_type =  "MACRO")
	if token.token_type != "COMMAND" and token.value not in MACRO_COMMANDS:
		print("Parsing error: macro token not of type COMMAND")
		return (False, None)
	elif token.token_type == "COMMAND" and token.value in MACRO_COMMANDS:
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
	>>> token = lexer.Token("hello", "CHARACTER", "hello")
	>>> queue = lexer.Queue
	>>> queue.enqueue(token)
	>>> arg = argument(queue)
	>>> print(arg)
	
	"""
	
	# what does this look like? tuple of token and queue object. 
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
		elif anothertoken.token_type == "COMMAND":
			print(f"running MACRO, token.value is {token.value}")
			_macro, tokenQueue = macro(token, tokenQueue)
			print(_macro.children)
			_argument.children.append(_macro)
			if _argument:
				return(_argument, tokenQueue)
	tokenQueue.put(token)
	return(arguments, tokenQueue)
	#print("here there be dragons")
	
def text(tokenQueue):
	_text = lexer.Token(token_type = "TEXT")
	token = next_token(tokenQueue)
	while token.value != "passage":
		if token.token_type == "CHARACTER":
			print("appending text to _text")
			_text.children.append(token)
			token = next_token(tokenQueue)
		elif token.token_type == "COMMAND":
			print("running macro for _macro in text")
			_macro, tokenQueue = macro(token, tokenQueue)
			if _macro:
				_text.children.append(_macro)
				token = next_token(tokenQueue)
	tokenQueue.put(token)
	print("done with text")
	return(_text, tokenQueue)
	
		


