# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 01:24:36 2021

@author: nkong
"""
import sys
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


def main(args):
    qryFile = open("cleanTrain.txt","r")
    recipes = qryFile.readlines()
    qryCuisine = {}
    for line in recipes:
        cuisine = getCuisine(line)
        ID = getID(line)
        qryCuisine[ID] = cuisine
    
    percentCorrect = {}
    for i in range (1, len(argv)):
        #output schema = id cuisine
        outputFile = open(argv[i], "r")
        guesses = outputFile.readlines()
        correct = 0
        qryGuess = {}
        for guess in guesses:
            tokens = guess.split()
            qryGuess[tokens[0]] = tokens[1]
        for guess in qryGuess:
            if qryGuess[guess] == qryCuisine[guess]:
                correct += 1
        percentCorrect[argv[i]] = correct/100
        outputFile.close()
    out = open("scores.txt", "w")
    for file in percentCorrect:
        print(file + " " + percentCorrect[file] + "\n")

if __name__ == '__main__':
	main(sys.argv)