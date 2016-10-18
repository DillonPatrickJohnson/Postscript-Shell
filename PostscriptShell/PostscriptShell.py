#Author: Dillon Johnson
#Postscript shell, implemented in Python


###	Operand Stack
def opPop():
	poppedItem = opstack.pop()				#popping the item off of the end of the List
	return poppedItem						#returns the popped item

def opPush(value):
	opstack.append(value)					#adds the passed in value to the top of the stack
	return opstack							#returns the stack


###	Dictionary Stack
def dictPop():
	poppedItem = dictstack.pop()			#pops the top dictionary item off of the stack
	return poppedItem
	
def dictPush(dictionary):
	dictstack.append(dictionary)			#adds the passed in dictionary value to the top of the stack
	return dictstack						#returns the stack

def define():
	value = opPop()							#popping the value from the opstack
	name = opPop()							#popping the name from the opstack
	dictstack[name] = value					#adding the name and value to the dictionary stack at the hot end

def lookup(name):							#looks up a name and returns the value of that name
	value = ""
	for x in dictstack:						#parses through the dictionaries in dictstack
		for k,v in x.items():
			if name == k:					#if the key == the name passed in, return the value
				value = v
	if value == "":							#else, value not found
		value = "/0"
	return value


###	Arithmetic Operators
def add():									#adds the 2 most recent (top) values in the stack
	v = opPop() + opPop()					#poping 2 values, adding them together and setting v = to the sum
	opPush(v)								#Pushing v to the opstack

def sub():									#subtracts the 2nd value from the 1st value in the stack
	v = opPop() - opPop()					#popping 2 values from the stack and setting v = to the difference
	opPush(v)								#pushing v to the opstack

def div():									#divide
	v = opPop() / opPop()					#popping 2 values from the stack and setting v = to the quotient
	opPush(v)								#pushing v to the opstack

def mul():
	v = opPop() * opPop()					#popping 2 values from the stack and setting v = to the product
	opPush(v)								#pushing v to the opstack

def mod():
	v = opPop() % opPop()					#popping 2 values from the stack and setting v = the modulo
	opPush(v)


###	String operators
def length():
	myVar = opPop()							#pops value off of the stack
	myString = str(myVar)					#converts the value to a string (if it is already a string that is fine)
	i = myString.__len__()					#getting the length of the string
	opPush(i)								#pushing the length of the string to the opstack

def get():
	myInt = opPop()							#pops the top value off, and set myInt = the value
	myString = opPop()						#pops a value off and set myString to the value
	myChar = myString[myInt]				#set myChar = the 'myInt'th index of myString
	opPush(ord(myChar))						#pushing the ascii value of myChar to the opstack

def put():
	myString = 'CptS 355'
	myIndex = opPop()
	myAscii = opPop()
	
	myList = list(myString)					#Creating a list holding each char of the string
	myList[myIndex] = chr(myAscii)			#replacing the character at myIndex with the char value of my Ascii
	myString = "".join(myList)				#setting myString to the elements of the list concatenated
	opPush(myString)

def getinterval():
	myCount = opPop()
	myIndex = opPop()
	myString = opPop()
	temp = myIndex+myCount
	opPush(myString[myIndex:temp])			#pushing the substring from the index to the index + count

	
###	Generic Stack functions
def dup():									#duplicates the top value of the stack
	v = opPop()								#pops the first value of the stack and sets v=poppedval
	opPush(v)								#pushing the popped value onto the stack twice
	opPush(v)

def exch():
	v1 = opPop()							#pops a value off of the stack
	v2 = opPop()							#pops another value off the stack
	opPush(v1)								#pushes the values on in reverse order
	opPush(v2)

def roll():									#i = number of elements, j = number of positions
	numList = []
	numList2 = []
	j = opPop()
	i = opPop()
	myRange = range(0,i)					#creating a range from 0->i
	myRotate = range(0,j)					#creating a range from 0->j
	stackLength = range(0,opstack.__len__()-i)	#Creating a range that will parse through the remaining elements of the list

	for x in myRange:						#filling a list with the specified number of elements that are rolled
		numList.append(opPop())
	for x in myRotate:						#popping the first number in the list and moving to the back, loops j times
		v = numList.pop(0)
		numList.append(v)
	for x in stackLength:					#popping off remaining elements and adding to a new list
		numList2.append(opPop())

	numList.reverse()						#reversing both lists in order to add correctly
	numList2.reverse()

	for x in numList2:						#pushing unchanged elements to the opstack
		opPush(x)
	for x in numList:						#pushing newly rotated (rolled) list to the opstack
		opPush(x)

def copy():
	myList = []
	n = opPop()
	myRange = range(0,n)					#creating a range for iteration that has n elements
	for x in myRange:
		myList.append(opPop())				#pop off n values
	myList.reverse()						#reverse the list to maintain correct format when pushing
	for x in myList:						#push each value in the list back to the stack
		opPush(x)
	for x in myList:						#repeat the push to copy the list
		opPush(x)

def clear():								#clears the stack
	myRange = range(0, opstack.__len__())
	for x in myRange:
		opPop()
			
def stack():								#prints the stack non destructively
	L = []
	for x in opstack:
		L.append(x)
	L.reverse()
	for x in L:
		print(x)


###	Dicitonary manipulation operators
def dict():
	size = opPop()
	myDict = {}								#creating a new dictionary
	opPush(myDict)							#pushing the new dictionary onto the opstack

def begin():
	d1 = opPop()							#pops the value (dictionary) off of the opstack
	dictPush(d1)							#pushes the new dictionary to the dictionary stack

def end():
	dictPop()								#pops the dict stack

def psDef():
	value = opPop()							#pops off the value
	name = opPop()							#pops off the name
	dictstack[dictstack.__len__()-1][name] = value			#adding the new definition to the dictstacks hot end


def tokenize(s):
    return re.findall("/?[a-zA-Z][a-zA-Z0-9_]*|[(][\w \W]*[)]|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]", s)

def parse(tokens):
	it = tokens.__iter__()								#creating an iterator for the tokens list
	S = groupMatching(it)								#assigning S to the output of groupMatching (replacing {} with list of elements)
	#print("s: ", S)
	S = returnints(S)									#converting all of the integers in string form, to integers in int form
	return S
	
	
def groupMatching(it):									#function that turns the code array blocks into lists
	res = []
	for c in it:
		#print("c val = ", c)
		if c == '}':
			return res
		elif c =='{':
			res.append(groupMatching(it))
		else:
			res.append(c)
	return res

def returnints(L1):										#function that converts a string of an number, to an integer
	for x in L1:										#looping through all elements in the passed in List
		if isinstance(x, list) == True:					#If x is a list itself,
			L1[L1.index(x)] = returnints(x)				#	do a recursive call to convert the inside of the list to integers
		else:
			try:										#doing a try to catch the error of passing in a string
				if isinstance(int(x), int) == True:		#if the integer casted string == an integer, 
					L1[L1.index(x)] = int(x)			#	we then assign the Xth index of the List to the converted integer
			except ValueError:
				pass
	return L1											#finally, we return the modified string

def interpret(L):										#function that: Executes commands in code array, defines variables, for loops
	for x in L:											#looping through each element in the list
		if isinstance(x, str) == True:					#if the element is a string, we check the first index to see if it is a string '(', name '/', or command 'a-z'
			if x[0] == '/':								#x is a name
				opPush(x[1:])
			elif x[0] == '(':							#x is a string
				opPush(x[1:])
				pass
			else:										#x is a command
				if x == "def":							#special exception since the def function is actually named psDef
					stack()
					psDef()
				elif x == "for":						#handling the for loop
					command = opPop()					#popping off the 4 values for the for loop
					finish = opPop()
					iterate = opPop()
					initial = opPop()
					initrange = range(finish, initial+1)

					for x in initrange:					#parsing through the range
						opPush(initial - x+1)			#pushing the value, and then performing the operation
						globals()[str(command[0])]()

				elif lookup(x) != "/0":
					Li = lookup(x)						#creating a new variable and setting it to the value of x in the dictstack
					if isinstance(Li, list) == True:	#if the value is a list, we do a recursive call to interpret that list
						interpret(Li)
					else:								#otherwise, the value is a number, so we push it to the stack
						opPush(Li)
				else:									#if the command is not def, and there is no associated dict value, we assume that the given command is defined
					globals()[x]()						#calling the given command
				pass
		elif isinstance(x, list) == True:				#if we are given a list, we push it to the opstack
			opPush(x)
		elif isinstance(x, int) == True:				#if we are given an integer, we push it to the opstack
			opPush(x)
	pass
		

###	Main
if __name__ == '__main__':	#main function
	import re

	opstack = []							#List that acts as a operand stack. The 'hot end' will be the end of the List, this list will hold ints, strings, and code arrays.
	dictstack = [{}]						#List of dictionaries...

	s = ""
	while s != "exit":
		s = input(">")
		if s == "exit": break
		userInput = tokenize(s)
		UIList = parse(userInput)
		interpret(UIList)