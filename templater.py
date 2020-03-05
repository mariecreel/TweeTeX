"""
templater.py - This is a simple template library which takes Token objects from the
TweeTeX parser and creates an equivalent document in Twee3 syntax using the sugarcube
story format.

Twee3 Specification:
https://github.com/iftechfoundation/twine-specs/blob/master/twee-3-specification.md
Sugarcube documentation:
https://www.motoslave.net/sugarcube/2/

Nick Creel - Mar 4 2020 - MIT License
"""
import lexer

TEMPLATES = {
	"link": "f'[[{text}|{link}]]'",
	#"MACROCOMMAND": "f'<<{command} '", THIS CAN BE DONE LATER
	#"MACROEND": '>>',
	"PREAMBLEMACRO": r"f'\"{name}\": \"{value}\",\n'",
	"TEXT" : '\n'
}


def visitTokens(parent):
	"""
	visitTokens takes a parent token as input and returns a string. Call recursively
	on token children to parse the entire AST.
	"""
	result = ""
	if parent.token_type in ["ARGUMENT", "STORY"]:
		for child in parent.children:
			result += visitTokens(child)
	else:
		if parent.token_type == "PREAMBLE":
			preambledata = ""
			for child in parent.children:
				if child.children[0].value == "title":
					title = ":: StoryTitle \n"
					title += (child.children[1].children[0].value)  # FIX THIS-- may cause problems in the future because it's too hardcoded.
					title += '\n'
				else:
					preambledata += "    " + visitTokens(child)
			preamble = (':: StoryData \n{ \n' +
						preambledata + '    "format": "SugarCube"\n}\n')
			result += preamble
			result += title

		elif parent.token_type =="MACRO":
			if parent.children[0].value == "link":
				print('evaluating link')
				print(f'text is {parent.children[1].children[0]}, link is {parent.children[2].children[0]}')
				formatdict = {'text': parent.children[1].children[0].value, 'link': parent.children[2].children[1].value}
				result += eval(TEMPLATES['link'], formatdict)
			else:
				print("this shouldn't happen!!")

		elif parent.token_type == "PASSAGE":
			result += '\n'
			title = ":: "
			title += visitTokens(parent.children[1])
			result += title
			for child in parent.children:
				if child.token_type in ["TEXT"]:
					result += visitTokens(child)

		elif parent.token_type in TEMPLATES:
			print(f"token type is {parent.token_type}")
			print("token type is in templates")
			if parent.token_type == "TEXT":
				result += TEMPLATES["TEXT"]
				for child in parent.children:
					result += visitTokens(child)
			elif parent.token_type == "PREAMBLEMACRO":
				formatdict = {}
				for child in parent.children:
					if child.token_type == "PREAMBLECOMMAND":
						formatdict['name'] = child.value
					else:
						formatdict['value'] = visitTokens(child)
				result += eval(TEMPLATES["PREAMBLEMACRO"], formatdict)

			else:
				formatdict = {'value' : parent.value}
				result += eval(TEMPLATES[parent.token_type], formatdict)
		else: # should be CHARACTER
			print(f"value is {parent.value}, token_type is {parent.token_type}")
			result += parent.value
	print("result is", result)
	return result

def makeNewFile(filename, story):
	tweestory = visitTokens(story)
	with open(filename, 'w') as file:
		file.write(tweestory)
	print("successfully wrote story to file")
	return tweestory

