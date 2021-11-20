import sys
import string
import numpy as np
import math

def tokenize(line):
    temp = line.split("ingredients")
    data = temp[1][3:-3]
    data = data.replace('"', '')
    ingredients = data.split(",")
    return ingredients
    
	
			
#Main Program
def main(args):
	mainfile = open(sys.argv[1], "r")

	#Open Abstracts of Journals
	readfile = open("/Users/junyi/Documents/NLP/Final Project/NLP_Project/cleaned_corpus/cleanTrain.txt", "r")
	contents = readfile.readlines()
	count = 0
	recipes = {}

	for line in contents:
		data = tokenize(line)
		recipes[count] = data
		count += 1

	queryfile = mainfile.readlines()
	count = 0
	testing = {}
	for line in queryfile:
		data = tokenize(line)
		testing[count] = data
		count += 1

	print(recipes)
	print(testing)
		




if __name__ == '__main__': 
	main(sys.argv)
