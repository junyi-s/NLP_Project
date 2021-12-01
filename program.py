import sys
import string
import numpy as np
import math
from nltk.stem import PorterStemmer
import numpy as np

from nltk.tokenize import word_tokenize
from numpy import dot
from numpy.linalg import norm

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

#idf of query in hw4
def idf_query(queries_list):
	temp_idf_query = {}
	for each_query in queries_list:
		query_tokens = word_tokenize(each_query)
		num_of_sameword_in_same_query = 0
		for word in query_tokens:
			if word not in temp_idf_query:
				temp_idf_query[word] = 1
				num_of_sameword_in_same_query += 1
			elif word in temp_idf_query and num_of_sameword_in_same_query == 0:
				temp_idf_query[word] += 1

	idf_query_dict = {}
	for word in temp_idf_query:
		idf_query_dict[word] = np.log(9997/temp_idf_query[word])

	return idf_query_dict

def calculate_tf_query(queries_dict):
	tf_query = {}
	for current_num in queries_dict:
		tf_query[current_num] = {}
		query_tokens = word_tokenize(queries_dict[current_num])
		for word in query_tokens:
			if word not in tf_query[current_num]:
				tf_query[current_num][word] = 1
			else:
				tf_query[current_num][word] += 1
	return tf_query

def calculate_idf_abstract(abstract_dict):
	temp_idf_abstract = {}
	for current_num in abstract_dict.keys():
		abstract_tokens = word_tokenize(abstract_dict[current_num])
		num_of_sameword_in_same_abstract = 0
		for word in abstract_tokens:
			if word not in temp_idf_abstract:
				temp_idf_abstract[word] = 1
				num_of_sameword_in_same_abstract += 1
			elif word in temp_idf_abstract and num_of_sameword_in_same_abstract == 0:
				num_of_sameword_in_same_abstract += 1

	idf_abstract = {}
	for word in temp_idf_abstract:
		idf_abstract[word] = np.log(1400 / temp_idf_abstract[word])



def termCount(terms, freq):
	for term in terms:
		if term in freq:
			freq[term] += 1
		else:
			freq[term] = 1

def cosine (vectors_for_abstract):
	cosine_sim = {}
	for q_num in vectors_for_abstract:
		cosine_sim[q_num] = {}
		q_vector = list(vectors_for_abstract[q_num].values())
		for a_num in vectors_for_abstract[q_num][a_num].keys():
			a_vector = list(vectors_for_abstract[q_num][a_num].values())
			cos_sim = dot(q_vector, a_vector) / (norm(q_vector) * norm(a_vector))
			if math.isnan(cos_sim):
				cos_sim = 0
			cosine_sim[q_num][a_num] = cos_sim
	return cosine_sim


#Main Program
def main(args):
	mainfile = open(sys.argv[1], "r")
	queryfile = mainfile.readlines()
	recipes = dict()
	queryTerms = dict()
	abstractTerms = dict()
	cuisine = dict()
	count = 0
	testing_dict = {}
	testing_list = []
	for line in queryfile:
		data = getIngredients(line)
		termCount(data, queryTerms)
		#testing_dict[count] = data
		temp_each_query = ""
		for item in data:
			temp_each_query += item + " "
		testing_list.append(temp_each_query)
		testing_dict[count] = temp_each_query
		count += 1

	idf_query_dict = idf_query(testing_list)
	tf_query_dict = calculate_tf_query(testing_dict)

	tf_idf_query = {}
	for current_num in tf_query_dict:
		tf_idf_query[current_num] = {}
		for word in tf_query_dict[current_num]:
			tf_idf_query[current_num][word] = tf_query_dict[current_num][word] * idf_query_dict[word]

	print(tf_idf_query)




	#Open Abstracts of Journals
	readfile = open("cleaned_corpus/cleanTrain.txt", "r")
	contents = readfile.readlines()
	count = 0
	abstract_dict = {}
	for line in contents:
		data = getIngredients(line)
		getCuisine(line)
		termCount(data, abstractTerms)
		recipes[count] = data
		#cuisine[count] = cuisine
		count += 1



	# print(termCount)
	# print(recipes)
	# print(testing)





if __name__ == '__main__':
	main(sys.argv)
