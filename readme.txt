TweeTeX is a programming language that borrows syntax from the LaTeX typesetting language while retaining the capabilities of the hypertext literature languages twee3 and SugarCube. TweeTeX is not a LaTeX library or a Twine story format; TweeTeX is meant to give twee the syntactical clarity of LaTeX and remove the burden of choosing a story format from the user. The source code may be accessed here: https://github.com/ncreel/TweeTeX. The specification and code are licensed under the MIT License. 

I wrote the specification for TweeTeX based on the specification for twee 3 written by Thomas M. Edwards and Dan Cox , in addition to the documentation of LaTeX as maintained by the LaTeX Team.  The TweeTeX compiler was built using Python 3.7.4, with no external libraries. 


Installation and Use
To install TweeTeX, download the contents of the TweeTeX github repository (https://github.com/ncreel/TweeTeX) to a directory of your choice. Note: You must have Python 3.x installed for TweeTeX to run on your system!
Once you’ve installed TweeTeX (and Python, if necessary), you may now test if TweeTeX is working properly. To test if TweeTeX is working correctly on your machine, create a file called test.twx in the same directory where you installed TweeTeX. Copy the following contents to that file:
\title{My Story}

\author{Nick Creel}

\ifid{0CA8C7C5-F219-4B1B-A3A8-45710F389818}

\start{Starting Passage}



\passage{Starting Passage}

This is some text in the first passage

\link{This link goes to the second passage}{Second Passage}



\passage{Second Passage}

This is some text in the second passage.

Once you’ve copied that text into your test file, be sure to save the file. Once you’ve saved the file, you can test TweeTeX by running the following command in your terminal on Linux or MacOS (be sure that you are in the same directory as the tweetex.py file!):
python3 tweetex.py test.twx
	Once the program has run, you should have a file named test.tw in the same directory, and the compiler should print “successfully wrote story to file.” This file should contain the following twee code, which may be compiled using a twee compiler, such as tweego:
:: StoryData 
{ 
    "author": "Nick Creel",
    "ifid": "0CA8C7C5-F219-4B1B-A3A8-45710F389818",
    "start": "Starting Passage",
    "format": "SugarCube"
}
:: StoryTitle 
My Story

:: Starting Passage
This is some text in the first passage
[[This link goes to the second passage|Second Passage]]
:: Second Passage
This is some text in the second passage.
Saving and Editing Files
TweeTeX source code should be saved using a .twx file and may be edited in any text editor. 
Macros
All macros must begin with a backslash ( \ ), and must also feature a command that is supported by TweeTeX. Currently supported commands:
1.	passage
2.	author
3.	title
4.	start
5.	ifid
6.	link

All arguments passed to macros must be wrapped in curly braces ( { <argument> } ) that are directly adjacent to the command, no spaces.

\link{This link goes to the second passage}{Second Passage}

A correctly formatted link macro.
Preamble 

A TweeTeX file must contain a preamble, which contains various metadata about the story. The preamble must contain four preamble macros: 

1.	\title: This macro takes one argument, which is the title of the story. Titles can be any combination of alphanumeric characters, excluding curly braces ({}) and backslashes (\).
2.	\author: This macro takes one argument, which is the author of the story. The author’s name may be written using a combination of alphanumeric characters, excluding curly 
braces({}) and backslashes (\)
3.	\ifid: This macro takes one argument, which is the Interactive Fiction IDentifier, or IFID. TweeTeX does not currently generate IFIDs, but an IFID may be generated using this resource provided by the creators of TADS: http://www.tads.org/ifidgen/ifidgen. The specification for the IFID was developed and published via the Treaty of Babel, which provides a standard for publishing and cataloguing interactive literature.
4.	\start: This macro takes one argument, which should be the name of a passage as that exists in the TweeTeX file. If the passage does not exist, the story will not compile correctly. This simply defines which passage will appear first when the player starts the story. 
\title{My Story}
\author{Nick Creel}
\ifid{0CA8C7C5-F219-4B1B-A3A8-45710F389818}
\start{Starting Passage}

An example preamble.
Passage

A passage is created with the \passage macro, and a passage macro takes one argument, the title of the passage.

\passage{My Passage}


Any text following the passage declaration is considered to be the text of that passage. A passage ends when a new passage is declared, or the document reaches end of file. 
Links

Links in TweeTeX function as hyperlinks between passages. Rather than using HTML to create a link, TweeTeX uses the following syntax. 

\link{<text of link>}{<passage to link to>}


The first argument is the text that will be displayed in the story as part of the link, and the second argument is the title of the passage that the link will navigate to. Note that the link macro works ONLY for linking passages within a story. If you want to add links to external content on the web, you must use HTML format. 
