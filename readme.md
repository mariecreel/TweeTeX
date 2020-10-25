Introduction
TweeTeX is a programming language that borrows syntax from the LaTeX typesetting language while retaining the capabilities of the hypertext literature languages twee3 and SugarCube. TweeTeX is not a LaTeX library or a Twine story format; TweeTeX is meant to give twee the syntactical clarity of LaTeX and remove the burden of choosing a story format from the user. The source code may be accessed here: https://github.com/ncreel/TweeTeX. The specification and code are licensed under the MIT License. 
I wrote the specification for TweeTeX based on the specification for twee 3 written by Thomas M. Edwards and Dan Cox , in addition to the documentation of LaTeX as maintained by the LaTeX Team.  The TweeTeX compiler was built using Python 3.7.4, with no external libraries. 
Why TweeTeX?

When I first wrote my own hypertext works, I was unsure which tool(s) I should use given my (at the time) limited knowledge of web development. I wanted a tool that would allow me to easily serve my work to the web without requiring knowledge of server-side scripting, but I also wanted the flexibility of being able to write my own code for different functions when appropriate. In my search for the right tool, I decided to try tools which were used to create hypertext literature I had read previously; One of the first pieces of hypertext literature I read was Howling Dogs by Porpentine  which was created entirely using the open source software Twine 2.  Howling Dogs impressed me with its memory of my actions, its simplistic interface, and its branching storylines, so I decided to create an interactive poetry collection with Twine 2 to take advantage of these powerful features.