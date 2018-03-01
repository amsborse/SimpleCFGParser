from nltk.tokenize import sent_tokenize, word_tokenize
from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP, NEWLINE
from nltk.stem import *
from io import BytesIO
import re

class Stemmer():
	#fuction to check the grammar
	def is_valid(text):

		if re.match("\s*((\w+-\w+)|(\w+))\s*:((\s*((\w+-\w+)|(\w+))\s*)*\|)*(\s*((\w+-\w+)|(\w+))\s*)*;",text)==None:
			print("Invalid Grammar",text)
			quit()

	def stem(text):
		#grammmar 
		grammar = {}
		#terminals
		terminal = []
		#sentence
		sentence = []
		#temporary variables
		tempList1 = []
		tempList2 = []
		tempString = ""
		#line by line grammar		
		grammar_String = ""
		#special character to check the sequence if occurrence 
		specialCharacter1 = ""
		specialCharacter2 = ""
		#string variable to store the output of stemmer
		stemmerString = ""
		#variable to store line number
		lineNumber = 1
		#flag
		flag = False
		#stemmer variable
		stemmer = SnowballStemmer("english")
		#replace input to make it easy to parse
		text = text.replace('|',' | ')
		text = text.replace(':',' : ')
		text = text.replace(';',' ; ')
		text = text.replace('=',' = ')
		text = text.replace('W',' W ')
		#tokenize the grammar
		tokens = word_tokenize(text)
		#loop to generate the output of the stemmer
		for i in tokens:
			if re.match(r'寿',i):
				lineNumber+=1
			elif re.match(r'W\s*=',i) or re.match(r'W',i):
				flag = True
				stemmerString += i+" STRING "+str(lineNumber)+'\n'
			elif re.match(r'[a-zA-Z]+',i):
				if flag:
					stemmerString += i+" STRING "+stemmer.stem(i)+" "+str(lineNumber)+'\n'
					sentence.append(stemmer.stem(i))
				else:
					stemmerString += i+" STRING "+str(lineNumber)+'\n'
			elif re.match(r'\W',i):
				specialCharacter1=specialCharacter2
				specialCharacter2=i
				stemmerString += i+" OP "+str(lineNumber)+'\n'
			elif re.match(r'\d+',i):
				stemmerString += i + " INT "+str(lineNumber)+'\n'
			elif re.match(r'\d+\.\d+'):
				stemmerString += i + " DOUBLE "+str(lineNumber)+'\n'
			else:
				print("Invalid Grammar")
				exit()

			if (specialCharacter1==":" and specialCharacter2==":") or (specialCharacter1==";" and specialCharacter2=="|") or (specialCharacter1=="|" and specialCharacter2==":") or (specialCharacter1==";" and specialCharacter2==";"):
				print("Invalid Grammar")
				quit()
		#replace input to make it easy to parse
		text = text.replace('寿','')
		#tokenize 
		tokens = word_tokenize(text) 
		flag = True
		#loop to populate the grammar
		for i in tokens:
			grammar_String += ' '+i
			if re.match(r'[a-zA-Z]+',i) and flag:
				tempString = tempString+i
				flag = False
			elif re.match(r':',i):
				continue
			elif re.match(r'[|]',i):
				tempList2.append(tempList1)
				tempList1=[]
			elif re.match(r'[a-zA-Z]+',i) and not flag:
				tempList1.append(i)
			elif re.match(r';',i):
				Stemmer.is_valid(grammar_String);
				grammar_String=""
				tempList2.append(tempList1)
				grammar.update({tempString:tempList2})
				tempList2=[]
				flag=True
				tempString = ""
				tempList1=[]

		flag = False

		tempList1 = []
		#loop to get terminals
		for k  in grammar:
			for i in grammar[k]:
				if len(i)==1 and i[0] not in grammar:
					flag = True
				else:
					flag = False
					break
			if flag:
				terminal.append(k)
				for i in grammar[k]:
					tempList1.append(i[0])
				grammar[k]=tempList1
				tempList1 = []
				flag=False
		
		return grammar, terminal, sentence, stemmerString
