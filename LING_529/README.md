# Linguistics 529 Human Language Technology I

This folder contains all course work from LING 529 "Human Language Technology I" taught by Dr. Gus Hahn-Powell at the University of Arizona during the Fall 2021 semester.

### Course Description
This class serves as an introduction to human language technology (HLT), an emerging interdisciplinary field that encompasses most subdisciplines of linguistics, as well as computational linguistics, natural language processing, computer science, artificial intelligence, psychology, philsophy, mathematics, statistics. Content includes a combination of theoretical and applied topics such as (but not limited to) tokenization across languages, n-grams, word representation, basic probability theory, introductory programming, and verison control.



## Unit 1

In this unit we covered basic python programming tasks in mutliplying, reversing lists, dropping elements, and returning the remainder.

1. The first function takes in an integer a and an integer b and returned an integer. The function mupltiples `a*b`

2. The second function takes in an sequence, reverses the content, drops the last element and returns what remains of the sequence using the methods pop and reverse.

## Unit 2

This unit covers a naive implementation of an incomplete rule-based system for POS tagging.

1. The first function is a rule base adverb tagger which takes a sentence as an input and rewrites the POS tag for any token ending in "-ly" as RB.

2. The second function is a rule base determiner tagger which takes a sentence as an input and rewrites the POS tag for any token that is one of the following words: a, all, an, any, each, every, no, some, that, the, these, this, those, which.

3. The third function is a rule base adjective tagger which takes a sentence as an input and rewrites the POS tag to JJ for any token ending in a "y" that was not previously tagged as an adverb.

4. The fourth function is a rule based verb copula tagger that which takes a sentence as an input and POS tags instances of the English verb "be" such that:
am --> VBP
is --> VBZ
are --> VBP
was --> VBD
were --> VBD

5. The fifth function is a rule based noun tagger which takes a sentence as an input and POS tags NOUN for any token that is immediately preceded by a token tagged as DT and immediately followed by a token tagged as some type of verb.

6. The sixth function takes a sentence as an input, applys rule base tagging functions 1-5, and returns a new sentence of POS tags.

## Unit 3

This unit covers an implementation of a regex-based tokenizer and a text normalization system.

## Unit 4

This unit introduces a class which is used to keep track of observed features and assign each distinct feature a unique ID which corrsponds to its index/column in the feature vector.

## Unit 5

This unit implements a function to calculate prior and conditional probabilities and to estimate the probability of sequences.

## Unit 6

This unit implements functions to calculate dot product, Euclidean distance, normalize a vector, the centroid of a set of vectors and the medoid of a set of vectors.

