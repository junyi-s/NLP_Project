import sys
import string
import numpy as np
import math

def getIngredients(line):
	temp = line.split("ingredients")
	data = temp[1][3:-3]
	data = data.replace('"', '')
	ingredients = data.split(",")
	return ingredients

def getCuisine(line):
	t = line.split("cuisine")
	t1 = t[1].split(':')
	t2 = t1[1].split('"')
	cuisine = t2[1]
	return cuisine

def getID(line):
	temp = line.split("id")
	t1 = temp[1].split(":")
	t2 = t1[1].split(",")
	ID = t2[0]
	return ID

#tf-idf of query in hw4
def tf_idf_query():
	temp_idf_query = {}

def termCount(terms, freq):
	for term in terms:
		if term in count:
			count[term] += 1
		else:
			count[term] = 1

def cosine (query_vector, abstracts_vector):
	answers = []

#Main Program
def main(args):
	mainfile = open(sys.argv[1], "r")
	contents = mainfile.readlines()

	#Open Abstracts of Journals
	# readfile = open("/Users/junyi/Documents/NLP/Final Project/NLP_Project/cleaned_corpus/cleanTrain.txt", "r")
	# contents = readfile.readlines()
	count = 0
	recipes = dict()
	freq = {}
	cuisine = dict()

	for line in contents:
		#data = getIngredients(line)
		# getCuisine(line)
		print(line)
		getID(line)
	# 	# termCount(data, freq)
	# 	recipes[count] = data
	# 	cuisine[count] = cuisine
	# 	count += 1

	# queryfile = mainfile.readlines()
	# count = 0
	# testing = {}
	# for line in queryfile:
	# 	data = getIngredients(line)
	# 	# termCount(data, freq)
	# 	testing[count] = data
	# 	count += 1

	# print(termCount)
	# print(recipes)
	# print(testing)





if __name__ == '__main__':
	main(sys.argv)
