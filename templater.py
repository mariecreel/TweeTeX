"""
templater.py - This is a simple template library which takes Token objects from the
TweeTeX parser and creates an equivalent document in Twee3 syntax using the sugarcube
story format.

Twee3 Specification:
https://github.com/iftechfoundation/twine-specs/blob/master/twee-3-specification.md
Sugarcube documentation:
https://www.motoslave.net/sugarcube/2/

Nick Creel - Feb 7 2020 - MIT License
"""

import lexer
TOPTOKENS = ["STORY", "PASSAGE", "TEXT", "MACRO", "PREAMBLEMACRO"]
def visitTokens(parent):
	result = ""
	for child in parent.children:
		if child.token_type == "PREAMBLE":
			result += ":: StoryData \n {"
			result += visitChildren(child)
			result += "}"
			return result
		elif child.token_type in TOPTOKENS:
			result += visitChildren(child)
			return result
		elif child.token_type == "PREAMBLECOMMAND":
			result += f'"{child.value}": '
		elif child.token_type == "MACROCOMMAND":
			if child.value == "link":
				if len(child.children) == 1:
					link = f"[[{arg1}]]"
				result += visitChildren(child)
				return result
			else:
		elif child.token_type == "ARGUMENT":
			if parent.token_type == "PREAMBLEMACRO":
				result += f'"{child.value}", \n'


def makeSugarcubeFile(filename, story):
	file = open(filename, "w")
