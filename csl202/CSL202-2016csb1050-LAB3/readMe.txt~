How to run the code:
Go to the working directory
python 2016csb1050.py INPUT_FILE

Sample outputs are at the end of this file....

The Python code checks validity of an xml document.
The rules followed are as follows:
tag hierarchy should be correct
there should be a root element
names should either be all uppercase or all lower case for all tags

ALGORITHM:

1) convert the file into a string and replace \n with nothing to include multi line tags
2) check for the following types of tags:
	a) <?xml?> 
	b) <!-- qwfdrhty -->
	c) <abc/> or <ABC/>
	d) <!DOCTYPE note SYSTEM "Note.dtd">
All these tags are valid in their own contexts hence ignore them
3) If the tag does not fall into this category, check if its a xml tag that is something enclosed in <>
4) Next check if it is a opening tag, if yes push it in stack, if no it is a closing tag
5) if a closing tag, check if the top element in stack is its corresponding opening tag. For this I have used regular expressions to extract name from all possibilities including:
	a) <title>
	b) <title id=8> i.e. <title something>
	c) next their cases are mathched after removing < and > and /
	d) next their content is matched
	e) cases like <titLE> vdv </titLE> have been dealt efficiently
6) loop over this and return "Not well-formed" if anything is violated
7) if still the stack is not empty then some opening tag has not been closed, hence not well formed\
8) whenever a valid xml tag is found (not the declarations but actual root tag) the root_found variable is set to 1
9) if root_found = 0 then no root tag was found, hence return "Not well-formed"

NOTE: All the unwanted characters will be removed from time to time


Sample test cases:

Input:
<?xml version="1.0" encoding="UTF-8"?>
<notee note >
<to>Tove</to>
<from>Jani</from> 
<heading>Reminder</heading>
<body>Don't forget me this weekend!</body>
</note>

2016csb1050@kickseed:~/CSL202-2016csb1050-LAB3$ python 2016csb1050.py sample-test-cases/false1.xml
Not well-formed



Input:
<?xml version="1.0" encoding="UTF-8"?>
<note>
<to>Tove</to>
<from>Jani</from> 
<heading>Reminder</pheading>
<body>Don't forget me this weekend!</body>
</note>

2016csb1050@kickseed:~/CSL202-2016csb1050-LAB3$ python 2016csb1050.py sample-test-cases/false2.xml 
Not well-formed


Input:
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE note SYSTEM "Note.dtd">
< note>
<to>Tove</to>
<from>Jani</from>
<heading>Reminder</heading>
<body>Don't forget me this weekend!</body>
</note>
2016csb1050@kickseed:~/CSL202-2016csb1050-LAB3$ python 2016csb1050.py sample-test-cases/true1.xml
well formed

