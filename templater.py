"""
templater.py - This is a simple template library which takes Token objects from the
TweeTeX parser and creates an equivalent document in Twee3 syntax.

Nick Creel - Feb 7 2020 - MIT License
"""

import lexer

def template(token):
	"""
	This function takes a token object as input and returns a string.
	"""
	templates = {"PASSAGE": f":: ",
				 "PREAMBLEMACRO": None,
				 ""
		}
	if len(token.children) < 1:

	elif len(token.children) == 1:

	else:

def make_twee3_file(filename, story):
	file = open(filename, "w")
