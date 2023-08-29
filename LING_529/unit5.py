

"""
Unit  code from LING 529 Human Language Technology I
Course taught by Dr. Gus Hahn-Powell
Author: Channing Donaldson
University of Arizona
Fall 2021


In unit 5 we implement a function to calculate prior and conditional probabilities and to estimate the probability of sequences.

This document includes code written by Channing Donaldson with function frameworks provided by Dr. Hahn-Powell.
"""

import numpy as np
from typing import Any, Dict, Iterable, List, Text, Tuple, Union
from collections import Counter
from nptyping import NDArray

from math import isclose

#UNIT 5

def array_of_zeros(num_zeros: int) -> NDArray[float]:
    """
    Creates a numpy array of zeros.
    """
    #repeat a value n times np.tile(7, 12) (an array of 7 repeated 12 times)
    
    zeroArray = np.tile(0, num_zeros)
    #print(zeroArray)
    return zeroArray

def add_scalar(vector: NDArray[float], scalar: int) -> NDArray[float]:
    """
    Takes a NumPy Array and adds a scalar value to each element in the array
    """
    results = vector + scalar
    newArray = np.array(results)
    #print(newArray)
    return newArray

def divide_by_scalar(vector: NDArray[float], scalar: int) -> NDArray[float]:
    """
    Takes a NumPy Array and divides each element in the array by a scalar value
    """
    results = vector / scalar
    newArray = np.array(results)
    #print(newArray)
    return newArray

## A sightly different Vocabulary class 

class Vocabulary:
    """
    Stateful vocabulary.
    Provides a mapping from term to ID and a reverse mapping of ID to term.
    """
    # symbol for unknown terms    
    UNKNOWN = "<UNK>"
    
    def __init__(self, terms: Iterable[Text]=[], min_count: int = 1):
        self.t2i: Dict[Text, int] = Vocabulary.create_t2i(terms, min_count=min_count)
        self.i2t: Dict[int, Text] = Vocabulary.create_i2t(self.t2i)
            
        #print(self.t2i)
        #print(self.i2t)
    
    # see https://www.python.org/dev/peps/pep-0484/#forward-references
    @staticmethod
    def from_sentences(sentences: Iterable[Iterable[Text]], min_count: int = 1) -> "Vocabulary":
        """
        Convenience method 
        for converting a sequence of tokenized sentences to a Vocabulary instance
        """
        return Vocabulary(terms=[term for sentence in sentences for term in sentence], min_count=min_count)
    
    def id_for(self, term: Text) -> int:
        """
        Looks up ID for term using self.t2i.  
        If the feature is unknown, returns ID of Vocabulary.UNKNOWN.
        """
        if term not in self.t2i:
            return self.t2i[Vocabulary.UNKNOWN]
        else:
            return self.t2i[term]
        
        
    def term_for(self, term_id: int) -> Union[Text, None]:
        """
        Looks up term corresponding to term_id.  
        If term_id is unknown, returns None.
        """
        if term_id not in self.i2t:
            return Vocabulary.UNKNOWN
        else:
            return self.i2t[term_id]
    
    @property
    def terms(self) -> List[Text]:
        return [self.i2t[i] for i in range(len(self.i2t))]
        
    @staticmethod
    def create_t2i(terms: Iterable[Text], min_count: int = 1) -> Dict[Text, int]:
        """
        Takes a flat iterable of terms (i.e., unigrams) and returns a dictionary of term -> int.
        Assumes terms have already been normalized.
        
        If the frequency of a term is less than min_count, 
        do not include the term in the vocabulary
        
        Requirements:
        - First term in vocabulary (ID 0) is reserved for Vocabulary.UNKNOWN.
        - Sort the features alphabetically
        - Only include terms occurring >= min_count
        """
        # terms must be strings
        if not all(isinstance(term, Text) for term in terms):
            raise Exception("terms must be strings")
        
        t2count = dict()
        
        for term in terms:
            if term not in t2count:
                t2count[term] = 0
            count = t2count[term]
            count += 1
            t2count[term] = count
        
        t2ind = dict()
        i = 1
        
        for key in sorted(t2count.keys()):
            count = t2count[key]
            if count >= min_count:
                t2ind[key] = i
                i += 1
        
        t2ind[Vocabulary.UNKNOWN] = 0
        #print("print vocabulary =================")
        #print(len(t2i_min))
        return t2ind
                
    
    @staticmethod
    def create_i2t(t2i: Dict[Text, int]) -> Dict[int, Text]:
        """
        Takes a dict of str -> int and returns a reverse mapping of int -> str.
        """
        return {i:t for (t, i) in t2i.items()}

    def empty_vector(self) -> NDArray[float]:
        """ 
        Creates an empty numpy array based on the vocabulary of terms
        """
        length = len(self.i2t)
        return np.empty(length) 
    
    def __len__(self):
        """
        Defines what should happen when `len` is called on an instance of this class.
        """
        return len(self.t2i)
    
    def __contains__(self, other):
        """
        Example:
        
        v = Vocabulary(["I", "am"])
        assert "am" in v
        """
        return True if other in self.t2i else False

def ngrams_for(
    # the size of the n-gram
    n: int, 
    # a list of tokens
    tokens: List[Text], 
    # whether or not to use the start and end symbols
    use_start_end: bool = True,
    # the symbol to use for the start of the sequence (assuming user_start_end is true)
    start_symbol: str = "<S>",
    # the symbol to use for the end of the sequence (assuming user_start_end is true)
    end_symbol: str = "</S>"
) -> List[Tuple[str]]:
    """
    Generates a list of n-gram tuples for the provided sequence of tokens.
    """
    tokens_dup = tokens
    if use_start_end:
        prefix  = [start_symbol] * (n-1)
        suffix  = [end_symbol] * (n-1)
        tokens_dup = prefix + tokens + suffix
    else:
        if len(tokens_dup) < n or n == 0:
            return []
    #print(tokens_dup)
    ngrams_tup = list()
    for i in range(len(tokens_dup) - n + 1):
        ngram = tokens_dup[i:i+n] 
        ngrams_tup.append(tuple(ngram))
    #print(ngrams_tup)
    return ngrams_tup

def prior_probs(tokens: Iterable[str], vocab: Vocabulary) -> NDArray[float]:
    """
    Calculates the prior probability for each token,
    given some vocabulary
    """
    termcount  = dict()
    totalcount = 0
    unkcount   = 0
    for term in tokens:
        if term not in termcount:
            termcount[term] = 0
        count       = termcount[term]
        count      += 1
        totalcount += 1
        termcount[term] = count
        if term not in vocab:
            unkcount += 1
    
    probs = vocab.empty_vector()
    
    for term in vocab.terms:
        i = vocab.id_for(term)
        if term not in termcount:
            probs[i] = 0.0
        else:
            count    = termcount[term]
            prob     = count / totalcount
            probs[i] = prob
    
    probs[0] = unkcount / totalcount
    
    return probs

# ex. [("I", "am"), ("she", "is")]
NgramType = Tuple[str, ...]

def make_conditional_probs(ngrams: Iterable[NgramType], vocab: Vocabulary) -> Dict[Tuple[Text, ...], NDArray[float]]:
    """
    Takes a sequence of n-grams and a vocabulary
    Returns a dictionary of conditional probability distributions for each n-gram's history
    """
    #Use joint prob to find conditional
    #P(A|B) = P(A, B)/P(B)
    #use one conditional probability to find another
    #P(A|B) = P(B|A) * P(A) / P(B)
    
    
    
    cond_probs = dict()
    cond_words = dict() #dictionary that maps ngram prefix to list of words
    for ngram in ngrams:
        ngramprefix = ngram[0:-1]
        #print(ngram)
        #print(ngramprefix)
        probs = vocab.empty_vector()
        for i in range(len(probs)):
            probs[i] = 0.0
        cond_probs[ngramprefix] = probs
        lastterm = ngram[-1]
        if ngramprefix not in cond_words:
            cond_words[ngramprefix] = list()
        wordlist = cond_words[ngramprefix]
        wordlist.append(lastterm)
    
        #print(i)
        #print(lastterm)
    
    for ngramprefix in cond_words:
        probs = cond_probs[ngramprefix]
        wordlist = cond_words[ngramprefix]
        counts = dict()
        for word in wordlist:
            if word not in counts:
                counts[word] = 0
            count = counts[word]
            count += 1
            counts[word] = count
        for word in counts:
            count = counts[word]
            p = count / len(wordlist)
            index = vocab.id_for(word)
            probs[index] = p
        
        #print("prefix is " + str(ngramprefix))
        #print("Word list is " + str(wordlist))
        #print("Probability is " + str(probs))
    return cond_probs

class LanguageModel():
    """
    An _n_-gram language model using an _n_th order Markov assumption.
    """
    
    def __init__(self, 
                 corpus: Iterable[Iterable[str]], 
                 n=2,
                 min_count=1,
                 use_start_end: bool = False
    ):
        assert n >= 2
        self.n = n
        self.use_start_end = use_start_end
        # though not stored as an instance attribute, we need this temporarily to calculate other attributes
        ngrams: Iterable[Tuple(Text, ...)] = [gram for sentence in corpus\
                                             for gram in ngrams_for(n=self.n, tokens=sentence, use_start_end=self.use_start_end)]
        self.vocab: Vocabulary                                   = Vocabulary.from_sentences(corpus, min_count)
        self.pdist: Dict[Tuple[Text, ...], NDArray[float]]       = make_conditional_probs(ngrams, self.vocab)
    
    def cond_prob(self, term: Text, given: Tuple[str, ...]) -> float:
        """
        Calculates the conditional probability for the provided term and the term's context.
        
        P(am|I) = cond_prob(term = "am", given = ("I",))
        """
        tprobabilties = self.pdist[given]
        termind = self.vocab.id_for(term)
        return tprobabilties[termind]
        
            
        
    def prob_of(self, tokens: Iterable[Text]) -> float:
        """
        Calculates the probability of a token sequence using an _n_th order Markov assumption.
        """
        # the starting probability of the sequence
        #print(self.pdist)
        p = 1
        for gram in ngrams_for(n=self.n, tokens=tokens, use_start_end=self.use_start_end):
            next_tok = gram[-1]
            history  = gram[:-1]
            cp = self.cond_prob(next_tok, history)
            p = p * cp
        return p

#Try training a bigram language model using a book from Project Gutenberg. See below for an example to get started

# from requests import get

# url = "http://www.gutenberg.org/cache/epub/35688/pg35688.txt"

# res = get(url)
# content = res.text

# # tokenize content, clean it up, and use it to train a bigram language model

#Bonus: Better estimates for probabilities (max 5 points)

#Our naïve language model assumes a probability of 0 when it encounters unknown terms. A consequence of this is that grammatical strings end up being assigned a probability of zero.

#Common solutions to this problem involve smoothing or a form of backoff.
#Task

#    Redefine the LanguageModel class and add a new method called def smoothed_prob_of(self, tokens: Iterable[str]) -> float and/or def prob_of(self, tokens: Iterable[str], backoff: bool) -> float.
#    Implement a smoothing or backoff algorithm of your choice. See Sections 3.3-3.6 of the textbook for examples of smoothing and backoff algorithms. Alternatively, you may invent your own.
#    Add at least two tests



def main():

    print("##########################Unit 5 Tests##########################")

    print("\n")
    #Assert that code in array_of_zeros passes test cases
    
    res1 = array_of_zeros(3)
    res2 = add_scalar(array_of_zeros(7), 34)
    res3 = add_scalar(array_of_zeros(4), 2)

    if type(res1) == np.ndarray:
        print("Test case 1 for array_of_zeros Passed. This array is of type np.ndarray.")
    else:
        print("Test case 1 for array_of_zeros Failed. This array is not of type np.ndarray.")

    if res1.ndim == 1:
        print("Test case 2 for array_of_zeros Passed. This array is 1D.")
    else:
        print("Test case 2 for array_of_zeros Failed. This array is not 1D.")

    if res.shape[0] == 3:
        print("Test case 3 for array_of_zeros Passed. This array contains a sequence length of 3.")
    else:
        print("Test case 3 for array_of_zeros Failed. This array does not contain a sequence length of 3.")

    if all(x == 0 for x in res):
        print("Test case 4 for array_of_zeros Passed. This array contains all zero values.")
    else:
        print("Test case 4 for array_of_zeros Failed. This array contains all zero values.")

    print("\n")

    if type(res2) == np.array:
        print("Test case 1 for add_scalar Passed. The array type is ndarray.")
    else:
        print("Test case 1 for add_scalar Failed. The array type is not ndarray")


if __name__ == "__main__":
	main()