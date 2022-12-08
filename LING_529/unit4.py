"""
Unit 4 code from LING 529 Human Language Technology I
Course taught by Dr. Gus Hahn-Powell
Author: Channing Donaldson
University of Arizona
Fall 2021


In unit 4

This document includes code written by Channing Donaldson with function frameworks provided by Dr. Hahn-Powell.
"""

from typing import List, Union, Iterable, Text, Tuple, Dict, Any
from collections import Counter
import re


# A class that keeps track of observed features and assigns each distinct feature a unique ID which corresponds to its index/column in feature vectors.

# A skeleton class was provided to students and the following methods were written by Channing: id_for, feature_for, create_f2i, add_feature

Feature = Union[Text, Tuple[Any, ...]]

class Vocabulary:
    """
    Stateful vocabulary.
    Provides a mapping from feature to ID and a reverse mapping of ID to feature.
    """
    # symbol for unknown terms    
    UNKNOWN = "<UNK>"
    
    def __init__(self, features: Iterable[Feature]=[]):
        """
        :param features: a sequence of features
        :type features: a sequence of strings
        
        :Example:
        v = Vocabulary(["has_four_legs", "is_furry", "has_tail"])
        """
        self.f2i: Dict[Feature, int] = Vocabulary.create_f2i(features)
        self.i2f: Dict[int, Feature] = Vocabulary.create_i2f(self.f2i)

        #self.f2i[Vocabulary.UNKNOWN] = 0
        #self.i2f[0] = Vocabulary.UNKNOWN

        print(self.f2i)
        print(self.i2f)
        
    def id_for(self, feature: Feature) -> int:
        """
        Looks up ID for feature using self.f2i.  
        If the feature is unknown, returns -1.
        
        :Example:
        
        v = Vocabulary(["b_feature", "a_feature"])
        assert v.id_for('<UNK>') == 0
        assert v.id_for('a_feature') == 1
        assert v.id_for('b_feature') == 2
        assert v.id_for('z_feature') == -1
        """
        
        if feature not in self.f2i:
            return -1
        else:
            return self.f2i[feature]
        
    def feature_for(self, feature_id: int) -> Union[Feature, None]:
        """
        Looks up term corresponding to feature_id.  
        If feature_id is unknown, returns None.
        
        :Example:
        
        v = Vocabulary(["b_feature", "a_feature"])
        assert v.feature_for(0) == v.UNKNOWN
        assert v.feature_for(1) == 'a_feature'
        assert v.feature_for(2) == 'b_feature'
        assert v.feature_for(19) == None
        """
        if feature_id not in self.i2f:
            return None
        else:
            return self.i2f[feature_id]
    
    @property
    def features(self) -> List[Feature]:
        """
        @property decorator allows attribute-like use of a method:
        
        :Example:
        
        v = Vocabulary(["has_four_legs", "is_furry", "has_tail"])
        assert v.features == ['<UNK>', 'has_four_legs', 'has_tail', 'is_furry']
        """
        return [self.i2f[i] for i in range(len(self.i2f))]
   

    @staticmethod
    def create_f2i(features: Iterable[Feature]) -> Dict[Feature, int]:
        """
        Takes a flat iterable of terms and returns a dictionary of term -> int.
        Assumes terms have already been normalized.
        
        Requirements:
        - First term in vocabulary (ID 0) is reserved for Vocabulary.UNKNOWN.
        """
        f2i = dict()
        i = 1
        for feature in sorted(features):
            if feature not in f2i:
                f2i[feature] = i
                i += 1
        
        f2i[Vocabulary.UNKNOWN] = 0
        return f2i
    
    @staticmethod
    def create_i2f(f2i: Dict[Feature, int]) -> Dict[int, Feature]:
        """
        Takes a dict of string -> integer and returns a reverse mapping of integer -> string.
        
        :Example:
        
        assert Vocabulary.create_i2f({"a_feature": 1, "b_feature": 2}) == {1: "a_feature", 2: "b_feature"}
        """
        return {i:f for (f, i) in f2i.items()}

    def add_feature(self, feature: Feature) -> None:
        """
        Takes a term and updates self.f2i 
        and self.i2f if the term is not already in the vocabulary.
        
        :Example:
        
        v = Vocabulary(["first_feature"])
        assert v.features == ['<UNK>', 'first_feature']
        v.add_feature("second_feature")
        assert v.features == ['<UNK>', 'first_feature', 'second_feature']
        assert v.id_for("second_feature") == 2
        """
        i = len(self.f2i) + 1
        if feature in self.f2i:
            return None
        else:
            self.f2i[feature] = i
            self.i2f[i] = feature

        
    def __plus__(self, other):
        """
        Defines what should happen when two instances of Vocabulary are summed.
                
        :Example:
        
        v1 = Vocabulary(["first_feature"])
        v2 = Vocabulary(["second_feature"])
        v3 = v1 + v2
        assert len(v3) == 3
        """
        if isinstance(other, str):
            features = self.f2i.keys() + [other]
            return Vocabulary(terms)
        elif isinstance(other, Vocabulary):
            features = self.f2i.keys() + other.f2i.keys()
            return Vocabulary(terms)
        return self
    
    def __len__(self):
        """
        Defines what should happen when `len` is called on an instance of this class.
        
        :Example:
        
        v = Vocabulary(["first_feature"])
        assert len(v) == 2
        """
        return len(self.f2i)
    
    def __contains__(self, other):
        """
        Defines what should happen when `in` is used with an instance of this class.
        
        :Example:
        
        v = Vocabulary(["feature_1", "feature_2"])
        assert "feature_1" in v
        """
        return True if other in self.f2i else False

# N-Grams

def ngrams(
    # the size of the n-gram
    n: int, 
    # a list of tokens
    tokens: List[str], 
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
    print(ngrams_tup)
    return ngrams_tup

def char_ngrams(
    n: int, 
    text: Text,
    use_start_end: bool = True,
    start_symbol: Text   = "^",
    end_symbol: Text     = "$"
) -> List[Text]:
    """
    Generates a list of n-gram tuples for the provided text.
    """
    text_dup = text 
    
    if n == -1:
        return []  
    
    if use_start_end:
        prefix   = [start_symbol] * (n-1)
        suffix   = [end_symbol] * (n-1)
        text_dup = prefix + list(text) + suffix
        #print(text_dup)
    
    chargrams = list()
    for i in range(len(text_dup) - n + 1):
        ngram = text_dup[i:i+n] 
        chargrams.append(tuple(ngram))
    print(chargrams)
    return chargrams

def make_count_vector(datum_features: Iterable[Feature], vocab: Vocabulary) -> List[int]:
    """
    Converts a sequence of features to a count vector.
    
    Takes a datum (seq of features) and a Vocabulary instance
    returns a new vector where each feature value is mapped to either 0 or 1
    """

    featurecount = dict()
    
    for j in range(len(datum_features)):
        word = datum_features[j]
        if word not in featurecount:
            featurecount[word] = 0
        count = featurecount[word]
        count += 1
        featurecount[word] = count
    
    vector = [0] * len(vocab)
    unkcount = 0
    for word in featurecount.keys():
        count = featurecount[word]
        if word in vocab:
            wordind = vocab.id_for(word)
            vector[wordind] = count
        else:
            unkcount += count
    
    vector[0] = unkcount
   
    print(vector)
    return vector

def binarize_vector(vector: List[int]) -> List[int]:
    """
    Takes a count vector and 
    returns a new vector where each feature value is mapped to either 0 or 1
    """
    bin_vec = []
    for i in vector:
        if i >= 1:
            bin_vec.append(int(1))
        else:
            if i == 0:
                bin_vec.append(int(0))
    print(bin_vec)
    return bin_vec

###BONUS TASK FROM UNIT 4

# Bonus: task-specific feature functions and feature vectors

#Representations for words and documents are often task-specific.  Implement 3 or more feature functions that will aid in carrying out a specific task.

## Option A: SPAM vs $\neg$SPAM
#`bonus_docs` represents a toy SPAM classification dataset.  Write feature functions and use them to generate representations for each document in `bonus_docs`.

### Requirements

#- Create at least 3 new feature functions.
#- Generate feature vectors for 3 or more documents (for example, `bonus_docs`).  
#- Describe your features.  How are they suited to the task you're modeling (ex. distinguishing between SPAM and HAM (not SPAM)?

##Bonus Question Framework

# from dataclasses import dataclass

# @dataclass
# class Datum:
#     doc: Text
#     label: Text
        
# dataset: List[Datum] = [
#     Datum(
#         # SPAM
#         doc="""
#         FROM : "MR.LAMIDO SANUSI" <elvislives478@aol.com>
#         SUBJECT: Your kind Attention: Beneficiary, Call me at +2348080754902 for more information.
#         BODY:
#         My Name Is Mr. Lamido Sanusi. I Am The Governor Central Bank Of Nigeria.  This Is To Notify You That Your Over Due Inheritance Funds Has Been Gazzeted To Be Released To You Via The Foreign Remmitance Department Of Our Bank.

#         Meanwhile, A Woman Came To My Office Few Days Ago With A Letter, Claiming To Be Your Representative And Sent By You.  If she is not your reprsentative or sent by you, kindly respond immediately reconfirming to me the following details to avoid any mistake.
#         + Full name
#         + Full residential contact address
#         + Direct telephone number number
#         + Age and current occupation
#         + Copy of your identification if available.

#         However, We Shall Proceed To Issue All Payments Details To The Said Mrs. Barbara Kleihans If We Do Not Hear From You Within The Next Three Working Days From Today. Await for your prompt response

#         You.Regards,

#         Mr. Lamido Sanusi
#         """,
#         label="SPAM"
#     ),
#     Datum(
#         # SPAM
#         doc="""
#         FROM: saxquatch4life@aol.com
#         SUBJECT: You're a Winner!
#         BODY: 
#         This President Zump. You've been pre-selected for early retirement. 
#         Please send your social security number ASAP to claim prize.
#         """,
#         label="SPAM"
#     ),
#     Datum(
#         # NOT SPAM
#         doc="""
#         FROM: ***REDACTED***@arizona.edu
#         SUBJECT: [ling_dept_faculty] Response needed
#         BODY: 
#         Please send your syllabus to ***REDACTED*** by 4PM on Friday.
#         """,
#         label="NOT_SPAM"
#     ),
#     Datum(
#         # NOT SPAM
#         doc="""
#         FROM: ***REDACTED***@arizona.edu
#         SUBJECT: Deadline extension?
#         BODY: 
#         Dr. Hahn-Powell,

#         I hope you are well.  Is there any way I can get an extension on the homework?  

#         Respectfully,

#             ***REDACTED***
#         """,
#         label="NOT_SPAM"
#     ),
#     Datum(
#         # NOT SPAM
#         doc="""
#         FROM: drive-shares-noreply@google.com
#         SUBJECT: Internship report - Invitation to edit
#         BODY:     
#             ***REDACTED*** has invited you to edit the following document:

#             Internship report

#             Open in Docs


#         Google Docs: Create and edit documents online.
#         Google LLC, 1600 Amphitheatre Parkway, Mountain View, CA 94043, USA
#         You have received this email because medeiros@email.arizona.edu shared a document with you from Google Docs.
#         """,
#         label="NOT_SPAM"
#     )
# ]
    
# for datapoint in dataset:
#     # we can access attributes of a dataclass just like any other class
#     print(datapoint.label)




def main():

    

    print("##########################Unit 4 Tests##########################")
    print("\n")
    print("v1")
    v1 = Vocabulary()
    print("\n")
    print("v2")
    v2 = Vocabulary(["ends_with_ly"])
    print("\n")
    print("v3")
    v3 = Vocabulary(["ends_with_ly", "ends_with_ly"])  
    new_features = ["a$", "^h", "ho", "ol", "la", "la"]
    print("\n")
    print("v4")
    v4 = Vocabulary()    
    ids = set([Vocabulary.UNKNOWN])

    for feat in new_features:
        v4.add_feature(feat)
        ids.add(v4.id_for(feat)) 



    print("\n")
    #Assert that code in class Vocabulary passes test cases
    if len(v1) == 1:
        print("Test case 1 for v1 = Vocabulary() Passed. Length of Vocabulary is currently 1.")
    else:
        print("Test case 1 for v1 = Vocabulary() Failed. Length of Vocabulary is not 2.")

    if Vocabulary.UNKNOWN in v1:
        print("Test case 2 for v1 = Vocabulary() Passed.")
    else:
        print("Test case 2 for v1 = Vocabulary() Failed.")
    print("\n")

    if len(v2) == 2:
        print("Test case 3 for v2 = Vocabulary([\"ends_with_ly\"]) Passed. Length of Vocabulary is now 2.")
    else:
        print("Test case 3 for v2 = Vocabulary([\"ends_with_ly\"]) Failed. Length of Vocabulary is not 2.")

    print("\n")
    
    if len(v3) == 2:
        print("Test case 4 for v3 = Vocabulary([\"ends_with_ly\", \"ends_with_ly\"]) Passed. Length of Vocabulary is still 2.")
    else:
        print("Test case 4 for v3 = Vocabulary([\"ends_with_ly\", \"ends_with_ly\"]) Failed. Length of Vocabulary is still 2.")

    print("\n")
    if v1.features == [Vocabulary.UNKNOWN]:
        print("Test case 5 for v1 = Vocabulary() Passed. v1.features == [Vocabulary.UNKNOWN]")
    else:
        print("Test case 5 for v1 = Vocabulary() Failed.")

    if v1.i2f[0] == Vocabulary.UNKNOWN:
        print("Test case 6 for v1 = Vocabulary() Passed. v1.i2f[0] == Vocabulary.UNKNOWN")
    else:
        print("Test case 6 for v1 = Vocabulary() Failed.")

    if v1.id_for(Vocabulary.UNKNOWN) == 0:
        print("Test case 7 for v1 = Vocabulary() Passed. v1.id_for(Vocabulary.UNKNOWN) == 0")
    else:
        print("Test case 7 for v1 = Vocabulary() Failed.")

    if v1.id_for("Xxx") == -1:
        print("Test case 8 for v1 = Vocabulary() Passed. v1.id_for(\"Xxx\") == -1")
    else:
        print("Test case 8 for v1 = Vocabulary() Failed.")

    if v1.feature_for(0) == Vocabulary.UNKNOWN:
        print("Test case 9 for v1 = Vocabulary() Passed. v1.feature_for(0) == Vocabulary.UNKNOWN")
    else:
        print("Test case 9 for v1 = Vocabulary() Failed.")

    print("\n")
    if len(ids) == len(v4):
        print("Test case 10 for v4 = Vocabulary() Passed. len(ids) == len(v4)")
    else:
        print("Test case 10 for v4 = Vocabulary() Failed.")

    if len(ids) == len(set(new_features)) + 1:
        print("Test case 11 for v4 = Vocabulary() Passed. len(ids) == len(set(new_features)) + 1 ")
    else:
        print("Test case 11 for v4 = Vocabulary() Failed.")

if __name__ == "__main__":
	main()