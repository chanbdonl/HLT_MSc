from typing import Sequence, List, Text, Optional
from graphviz import Source
import re

"""
Unit 3 code from LING 529 Human Language Technology I
Course taught by Dr. Gus Hahn-Powell
Author: Channing Donaldson
University of Arizona
Fall 2021


In unit 3 we impliment a mostly regex-based tokenizer and text normalization system

This document includes code written by Channing Donaldson with function frameworks provided by Dr. Hahn-Powell.
"""

#The following class is writen by Dr. Hahn-Powell which keeps track of tokens and their attributes

	#The following portion references code written by Dr. Hahn-Powell which creates a solid state machine image using graphviz, but was edited by Channing


s2 = """
digraph abc_v2_lang {
	rankdir=LR;
	size="8,5"

	node [shape = circle, label="S", fontsize=14] S;
	node [shape = circle, label="q1", fontsize=12] q1;
	node [shape = circle, label="q2", fontsize=12] q2;
	node [shape = doublecircle, label="q3", fontsize=12] q3;

	//node [shape = point ]; qi
	//qi -> S;
	S  -> q1 [ label = "a" ];
	S  -> q2 [ label = "b" ];
	q1 -> q2 [ label = "b" ];
	q2 -> q2 [ label = "b" ];
	q2 -> q3 [ label = "c" ];
}
"""

	#End of code written by Hahn-Powell



class Sentence:
	# Used to represent unknown symbols
	UNKNOWN: Text = "???"
	"""
	Class representing a Sentence's tokens and their attributes.
	"""
	def __init__(
		self, 
		tokens: Sequence[Text],
		norms: Optional[Sequence[Text]] = None,
		pos: Optional[Sequence[Text]] = None
	):
		# tokens
		# NOTE: Tuple[Text, ...] means a tuple (i.e., an immutable sequence) 
		# of variable length where each element is a string (Text)
		self.tokens: Tuple[Text, ...]   = tuple(tokens)
		# normalized forms of each token
		self.norms: Tuple[Text, ...]    = tuple(norms) if norms else tokens[::]
		# part-of-speech tags
		self.pos: Tuple[Text, ...]      = tuple(pos) if pos else tuple([Sentence.UNKNOWN] * self.size)
		# ensure each token has an attribute of each type
		assert all(self.size == len(attr) for attr in [self.pos, self.norms])

	@property
	def size(self):
		"""
		Calculates the number of tokens in our sentence.

		# Example: 
		s = Sentence(tokens=["I", "like", "turtles"])
		s.size == 3
		"""
		return len(self.tokens)

	def __len__(self):
		"""
		Calculates the number of tokens in our sentence.
        
		# Example: 
		s = Sentence(tokens=["I", "like", "turtles"])
		len(s) == 3
		"""
		return self.size

	def __repr__(self):
		"""
		The text displayed when printing an instance of our sentence.
		"""
		# convenience function to join lists
		to_str = lambda elems: "\t".join(elems)
		return f"""
		tokens:           {to_str(self.tokens)}
		normalize tokens: {to_str(self.norms)}
		pos:              {to_str(self.pos)}
		"""
    
	def copy(self, 
		tokens = None, 
		norms = None,
		pos = None):
		"""
		Convenience method to copy a Sentence and replace one or more of its attributes.
		"""
		return Sentence(
			tokens   = tokens or self.tokens[::],
			norms    = norms or self.norms[::],
			pos      = pos or self.pos[::]
		)

	#End of code written by Hahn-Powell


def abc_lang_matcher(s: str) -> bool:


	

	matched = re.match(r"[a][b][a-c]+", s)
	if matched:
		return True
	else:
		return False





def abc_v2_lang_matcher(s: str) -> bool:

	#The following class is writen by Dr. Hahn-Powell which creates a solid state machine image using graphviz

	#End of code written by Hahn-Powell


	matched = re.match(r"\b[a]?[b]+[a-c]\b", s)
	if matched:
		return True
	else:
		return False

#RegEx based tokenizer

def tokenize_on_whitespace(text: str) -> List[str]:
	spaces = r"\s+"
	tokens = re.split(spaces, text, flags=re.UNICODE)
	words = list()
	for word in tokens:
		if( len(word) != 0 ):
			words.append(word)
	#print(words)
	return words

def tokenize_better(text: str) -> List[str]:
	pattern_list = [r'\s',r'(n\'t)',r'(\'m)',r'(\'ll)',r'(\'ve)',r'(\'s)',r'(\'re)',r'(\'d)']
	pattern=re.compile('|'.join(pattern_list))
	tokens = pattern.split(text)
	words = list()
    
	for word in tokens:
		if word is not None and len(word) != 0:
			words.append(word)
 	#print(words)
	return words

def tokenize_even_better(text: str) -> List[str]:
	pattern = r"\s+|(?=')|(?=\?)|(?=\!)|(?=,)|(?=[.])(?<!Dr)"
	tokens = re.split(pattern,text)
	print(tokens)
	return tokens

#Text normalization

def casefold(text: str, lower: bool) -> str:
	for i in text:
		if lower == True:
			return text.lower()
		else:
			if lower == False:
				return text.upper()

def url_replace(text: str) -> str:
	"""
	Replaces text spans resembling URLs with URL.
	"""
	pattern = r'\w+\.com|\w+\.ai|^https://\w+'
	REPLACE_WITH = "URL"
	print(re.sub(pattern=pattern, repl=REPLACE_WITH, string=text))
	return re.sub(pattern=pattern, repl=REPLACE_WITH, string=text)


#Preprocessing text to string

def tokenize(text: str) -> List[str]:
	"""
	Tokenizes text; split on whitespaces, remove any extra spaces
	"""
	pattern = r"\s+|(?=')|(?=\?)|(?=\!)|(?=,)|(?=[.])(?<!Dr)"
	tokens  = re.split(pattern, text, flags=re.UNICODE)
	return tokens
    

def normalize(tokens: List[str]) -> List[str]:
	"""
	normalize text; normalize word format
	"""

	foldedWords = tokens.casefold()

	pattern = r'\w+\.com|\w+\.ai|^https://\w+'
	REPLACE_WITH = "URL"
	wordNorms = re.sub(pattern=pattern, repl=REPLACE_WITH, string=foldedWords)
	return wordNorms


def preprocess(text: str) -> Sentence:
	"""
	Takes text, tokenizes the text, and creates a Sentence with normalized tokens 
	"""
	return tokenize.Sentence



def main():

	print("##########################Unit 3 Tests##########################")

	#Assert that code in abc_lang_matcher() passes test cases
	if abc_lang_matcher("ac")   == False:
		print("Test case 1 for abc_lang_matcher() Passed.")
	else:
		print("Test case 1 for abc_lang_matcher() Failed.")

	if abc_lang_matcher("abc")   == True:
		print("Test case 2 for abc_lang_matcher() Passed.")
	else:
		print("Test case 2 for abc_lang_matcher() Failed.")

	if abc_lang_matcher("abbc")   == True:
		print("Test case 3 for abc_lang_matcher() Passed.")
	else:
		print("Test case 3 for abc_lang_matcher() Failed.")

	if abc_lang_matcher("xabc")   == False:
		print("Test case 4 for abc_lang_matcher() Passed. \n")
	else:
		print("Test case 4 for abc_lang_matcher() Failed.\n")

	s1_path = '/home/channing/HLT_MSc/LING_529/Source.gv'
	s1 = Source.from_file(s1_path)
	s1.view()

	#Assert that code in abc_v2_lang_matcher() passes test cases
	if abc_v2_lang_matcher("ac")   == False:
		print("Test case 1 for abc_v2_lang_matcher() Passed.")
	else:
		print("Test case 1 for abc_v2_lang_matcher() Failed.")

	if abc_v2_lang_matcher("abc")   == True:
		print("Test case 2 for abc_v2_lang_matcher() Passed.")
	else:
		print("Test case 2 for abc_v2_lang_matcher() Failed.")

	if abc_v2_lang_matcher("abbc")   == True:
		print("Test case 3 for abc_v2_lang_matcher() Passed.")
	else:
		print("Test case 3 for abc_v2_lang_matcher() Failed.")

	if abc_v2_lang_matcher("c")   == False:
		print("Test case 4 for abc_v2_lang_matcher() Passed.")
	else:
		print("Test case 4 for abc_v2_lang_matcher() Failed.")

	if abc_v2_lang_matcher("bc")   == True:
		print("Test case 5 for abc_v2_lang_matcher() Passed.")
	else:
		print("Test case 5 for abc_v2_lang_matcher() Failed.")

	if abc_v2_lang_matcher("bbc")   == True:
		print("Test case 6 for abc_v2_lang_matcher() Passed.")
	else:
		print("Test case 6 for abc_v2_lang_matcher() Failed.")

	if abc_v2_lang_matcher("bbbc")   == True:
		print("Test case 7 for abc_v2_lang_matcher() Passed.")
	else:
		print("Test case 7 for abc_v2_lang_matcher() Failed.")

	if abc_v2_lang_matcher("abbcx")   == False:
		print("Test case 8 for abc_v2_lang_matcher() Passed. \n")
	else:
		print("Test case 8 for abc_v2_lang_matcher() Failed. \n")
	s2.view()
	print("\n")
	#Assert that code in tokenize_on_whitespace() passes test cases
	if tokenize_on_whitespace("The name of the wind.") == ["The", "name", "of", "the", "wind."]:
		print("Test case 1 for tokenize_on_whitespace() Passed.")
	else:
		print("Test case 1 for tokenize_on_whitespace() Failed.")

	if tokenize_on_whitespace("    The               name of the wind.") == ["The", "name", "of", "the", "wind."]:
		print("Test case 2 for tokenize_on_whitespace() Passed.")
	else:
		print("Test case 2 for tokenize_on_whitespace() Failed.")

	if tokenize_on_whitespace("His family name is spelled S ö z e")      == ["His", "family", "name", "is", "spelled", "S", "ö", "z", "e"]:
		print("Test case 3 for tokenize_on_whitespace() Passed.")
	else:
		print("Test case 3 for tokenize_on_whitespace() Failed.")

	if 	tokenize_on_whitespace("Abre los ojos, señor Cruise")             == ["Abre", "los", "ojos,", "señor", "Cruise"]:
		print("Test case 4 for tokenize_on_whitespace() Passed.")
	else:
		print("Test case for for tokenize_on_whitespace() Failed.")

	if tokenize_on_whitespace("Heghlu'meH QaQ jajvam!")                  == ["Heghlu'meH", "QaQ", "jajvam!"]:
		print("Test case 5 for tokenize_on_whitespace() Passed.")
	else:
		print("Test case 5 for tokenize_on_whitespace() Failed.")

if __name__ == "__main__":
	main()