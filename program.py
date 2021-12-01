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
		idf_abstract[word] = np.log(29777 / temp_idf_abstract[word])
	return idf_abstract

def calculate_tf_abstract(abstract_dict):
	tf_abstract = {}
	for current_num in abstract_dict:
		tf_abstract[current_num] = {}
		abstract_tokens = word_tokenize(abstract_dict[current_num])
		for word in abstract_tokens:
			if word not in tf_abstract[current_num]:
				tf_abstract[current_num][word] = 1
			else:
				tf_abstract[current_num][word] += 1
	return tf_abstract

def findCuisine (abstract_index, cuisine_list):
	answer = cuisine_list[abstract_index]
	return answer

def sort(cosine_similarity):
	sorted_output = {}
	for q_num in cosine_similarity:
		sorted_output[q_num] = sorted(cosine_similarity[q_num].items(), key=lambda item: item[1], reverse=True)
	return sorted_output

def results(sorted_output):
	output = open("output.txt", "w")
	for q_num in sorted_output:
		for abs_data in sorted_output[q_num]:
			if(abs_data[1] == 0):
				continue
			output.write(str(q_num) + " " + str(abs_data[0]) + " " + str(abs_data[1]) + "\n")
	output.close()

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
	cuisine_abstract = dict()
	cuisine_query = dict()
	count = 0
	testing_dict = {}
	testing_list = []
	for line in queryfile:
		data = getIngredients(line)
		c = getCuisine(line)
		termCount(data, queryTerms)
		#testing_dict[count] = data
		temp_each_query = ""
		for item in data:
			temp_each_query += item + " "
		testing_list.append(temp_each_query)
		testing_dict[count] = temp_each_query
		cuisine_query[count] = c
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
		c = getCuisine(line)
		termCount(data, abstractTerms)
		recipes[count] = data
		temp_each_abstract = ""
		for item in data:
			temp_each_abstract += item + " "
		abstract_dict[count] = temp_each_abstract
		cuisine_abstract[count] = c
		count += 1

	idf_abstract_dict = calculate_idf_abstract(abstract_dict)
	tf_abstract_dict = calculate_tf_abstract(abstract_dict)

	tf_idf_abstract = {}
	for current_num in tf_abstract_dict:
		tf_idf_abstract[current_num] = {}
		for word in tf_abstract_dict[current_num]:
			tf_idf_abstract[current_num][word] = tf_abstract_dict[current_num][word] * idf_abstract_dict[word]

	print(tf_idf_abstract)


	vectors_for_abstract = {} #vectors_for_abstract[Q_num][A_num][word both in Q and A] = [] => vectors(list) for abstract
#Finding vectors for abstract: Later use for cosine similarity
	for current_Q_num in tf_idf_query:
		current_query_words = tf_idf_query[current_Q_num].keys()
		# current_query_vector = []
		# for word in current_query_words:
		#     current_query_vector = tf_idf_query[current_Q_num][word]
		vectors_for_abstract[current_Q_num] = {}
		for current_A_num in tf_idf_abstract:
			vectors_for_abstract[current_Q_num][current_A_num] = {}
			for word in current_query_words:
				vectors_for_abstract[current_Q_num][current_A_num][word] = {}
				if word in tf_idf_abstract[current_A_num]:
					# if tf_idf_abstract[current_A_num][word] <0 :
					#     print('here', current_A_num, word)
					#     break
					vectors_for_abstract[current_Q_num][current_A_num][word] = tf_idf_abstract[current_A_num][word]
				else:
					vectors_for_abstract[current_Q_num][current_A_num][word] = 0

	cosine = cosine(vectors_for_abstract)
	sorted_cosine = sort(cosine)
	answers =





if __name__ == '__main__':
	main(sys.argv)
