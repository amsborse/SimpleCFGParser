from stemmer import *
from parser import *
if __name__ == '__main__':
	#input variable
	text = ""
	#loop to read input
	flag = True
	while True:
	    line = input()
	    
	    if len(re.findall(r'[^#a-zA-Z0-9|;:\s.=-]+',line))>0:
	    	print("Invalid Grammar",line)
	    	exit()
	    if len(line)==0 and flag:
	    	print("")
	    	print("No Input: Please Input without any empty lines at the start")
	    	exit()
	    flag = False
	    if len(line)==0 or re.match('#',line):
	    	continue
	    text += "%s 寿 " % line
	    if re.match(r'W\s*=',line) :
	        break
	
	print("Stemmer:")
	#call stemmer
	grammar, terminal, sentence, stemmerString = Stemmer.stem(text)
	#print stemmer output
	print(stemmerString)
	if len(sentence)==0:
		print("No Word")
		exit();
	print("ENDFILE")
	#parsed chart output
	print("Parsed Chart:")
	#create object early
	parsedSentence = Parser(sentence, grammar, terminal)
	#call parse
	parsedSentence.parse()
	#print the output of the parser
	print(parsedSentence)

