"""
Unit 1 code from LING 531 Human Language Technology II
Course taught by Dr. Eric Jackson
Author: Channing Donaldson
University of Arizona
Fall 2021


The purpose of unit 1 was to write a function that parse training data from the "NewB" corpus into lines and then write a second function that took the output of the previous function, parsed it into a list of lists, where each top level of the list corresponses to the category of the successive sentence.

This document includes code written by Channing Donaldson with function frameworks provided by Dr. Jackson.
"""

import os
import re


#you'll need to change this to fit the location
#of this file on your system
newbfile  = '/home/channing/Desktop/LING-531/NewB/train_orig.txt'


def getlines(filename):
    '''read in file and return the lines
    
    args:
        filename: name of the file
    returns:
        lines: a list of lines
    '''
    # YOUR CODE HERE
    #raise NotImplementedError()
    
    #read in text file
    txtfile = open(newbfile, 'rt')
    readtxt = txtfile.read()
    
    
    #split on new line
    newlines = readtxt.split('\n')
    
    txtfile.close()
    
    #sortedlines = sorted(newlines)
    
    #print(type(newlines))
    #print(sortedlines[0:3])
    return newlines

def makeSentences(lines):
    '''convert the list of sentences into a
    list of lists
    
    args:
        lines: the list of lines produced by getlines()
    
    returns:
        listlist: the list of lists
    '''
    #cats   = ["Newsday", "New York Times", "Cable News Network", "Los Angeles Times",
    #          "Washington Post", "Politico", "Wall Street Journal", "New York Post",
    #          "Daily Press", "Daily Herald", "Chicago Tribune"]
    sents  = list()
    for i in range(11):
        catlist = list()
        sents.append(catlist)

    
    for line in lines:
        getlabel = re.split(r'\t', line)
        if len(getlabel) == 2:
            category = int(getlabel[0])
            #print(category)
            sentence = getlabel[1]
            #print(sentence)
            catlist = sents[category]
            catlist.append(sentence)

    
    #return catlist
    #print(sent[0:3])
    return sents

def main():

    print("########################## LING 531 Unit 1 Tests  ##########################")

    res = getlines(newbfile)

    #Assert that code in getlines() passes test cases
    if type(res) == list:
        print("Test case 1 for getlines() Passed: type(res) == list")
    else:
        print("Test case 1 for getlines() Failed. Type error.")

    if len(res) == 253782:
        print("Test case 2 for getlines() Passed: len(res) == 253782")
    else:
        print("Test case 2 for getlines() Failed. Length incorrect.")

	#Assert that code in makeSentences() passes test cases
    
    sentences = makeSentences(res)
    sections = []
    for section in sentences:
        sections.append(len(section) == 23071)
    assert all(sections)

    if type(sentences) == list:
        print("Test case 1 for makeSentences() Passed: type(sentences) == list")
    else:
        print("Test case 1 for makeSentences() Failed. Type error.")

    if len(sentences) == 11:
        print("Test case 2 for makeSentences() Passed. len(sentences) == 11")
    else:
        print("Test case 2 for makeSentences() Failed. Length incorrect.")

    if sentences[4][10] == 'if they criticize trump the president attacks them':
        print("Test case 3 for makeSentences() Passed. sentences[4][10] == \'if they criticize trump the president attacks them\'.")
    else:
        print("Test case 3 for makeSentences() Failed. Expected outcome not retrieved.")


if __name__ == "__main__":
	main()