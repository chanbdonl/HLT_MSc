"""
Unit 2 code from LING 529 Human Language Technology I
Course taught by Dr. Gus Hahn-Powell
Author: Channing Donaldson
University of Arizona
Fall 2021


In unit 2 we implimented a naive and incomplete rule-based sysem for POS tagging.

This document includes code written by Channing Donaldson with function frameworks provided by Dr. Hahn-Powell.
"""

from typing import Tuple, Sequence, Text, Optional

#The following class is writen by Dr. Hahn-Powell which keeps track of tokens and their attributes
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



def rule_based_ly_adv_tagger(s: Sentence) -> Sentence:
    """
    Takes a Sentence and returns a new Sentence with updated POS tags.
    
    If a token ends with "ly", assign it a POS tag of RB.
    """
    tag_RB = []

    for i, token in enumerate(s.tokens):
        prev_pos = s.pos[i]
        if token[-2:] == "ly":
            tag_RB.append("RB")
        else:
            tag_RB.append(prev_pos)
    s2 = s.copy(pos = tag_RB)
    return s2

def rule_based_det_tagger(s: Sentence) -> Sentence:
    """
    Takes a Sentence and returns a new Sentence with updated POS tags.
    
    If a token is one of the following:
      a, all, an, any, each, every, no, some, that, the, these, this, those, which
    """
    tag_DT = []
    det = ["a", "all", "ALL", "All", "an", "any", "each", "every", "no", "NO", "No", "some", "that", "the", "THE", "these", "this", "those", "Those", "which"]
    for i, token in enumerate(s.tokens):
        prev_pos = s.pos[i]
        if token in det:
            tag_DT.append("DT")
        else:
            tag_DT.append(prev_pos)
    s2 = s.copy(pos = tag_DT)
    return s2

def rule_based_not_adv_adj_tagger(s: Sentence) -> Sentence:
    """
    Takes a Sentence and returns a new Sentence with updated POS tags.
    
    If a token ends in y and is not already tagged as an adverb (RB), tag it as JJ.
    """
    tag_JJ = []
    s_adv = rule_based_ly_adv_tagger(s)
    
    for i, token in enumerate(s_adv.tokens):
        pos_adv = s_adv.pos[i]
        if token.endswith("y") and pos_adv != "RB":
            tag_JJ.append("JJ")
        else:
            tag_JJ.append(pos_adv)
    s2 = s_adv.copy(pos = tag_JJ)
    return s2

#Considering the surrounding tags to inform the tag assignmet of the current word

def verb_copula(s: Sentence) -> Sentence:
    """
    Takes a Sentence and returns a new Sentence with updated POS tags.
    
    Assigns the following tags:
    
    am -> VBP
    is -> VBZ
    are -> VBP
    was -> VBD
    were -> VBD
    """
    verb_map = {"am": "VBP", "is": "VBZ", "are": "VBP", "was": "VBD", "were": "VBD"}
    tag_verb = []
    
    for i, token in enumerate(s.tokens):
        prev_pos = s.pos[i]
        if token in verb_map:
            verb_pos = verb_map[token]
            tag_verb.append(verb_pos)
        else:
            tag_verb.append(prev_pos)
    s2 = s.copy(pos = tag_verb)
    return s2

def det_noun_verb(s: Sentence) -> Sentence:
    """
    Takes a Sentence and returns a new Sentence with updated POS tags.
    
    If a token _t_ is ...
    1) immediately preceded by a token $_t_{t-1}$ already tagged as a determiner 
    and ...
    2) immediately followed by a token already tagged as a verb

    tag the token as a NOUN (we'll ignore plural vs singular distinctions).
    
    Examples:
    DT ??? VBD -> DT NOUN VBD
    
    """
    tag_noun = []
    s_det = rule_based_det_tagger(s)
    tag_s = verb_copula(s_det)
    verb_map = {"am": "VBP", "is": "VBZ", "are": "VBP", "was": "VBD", "were": "VBD"}
    for i, token in enumerate(tag_s.tokens):
        pos_prev_tag = tag_s.pos[i]
        if i > 0 and i < len(tag_s) - 1 and tag_s.pos[i - 1] == "DT" and tag_s.pos[i + 1] in verb_map.values():
            tag_noun.append("NOUN")
        else:
            tag_noun.append(pos_prev_tag)
    s2 = tag_s.copy(pos = tag_noun)
    return s2

def tag_with_rules(s: Sentence) -> Sentence:
    """
    Takes a Sentence and returns a new Sentence with updates POS tags
    by applying a series of rules for part of speech tagging
    """
    tagged_sent = []
    tag_s_RB    = rule_based_ly_adv_tagger(s)
    tag_s_DT    = rule_based_det_tagger(tag_s_RB)
    tag_s_JJ    = rule_based_not_adv_adj_tagger(tag_s_DT)
    tag_s_VERB  = verb_copula(tag_s_JJ)
    tag_s_NOUN  = det_noun_verb(tag_s_VERB)
    s2          = tag_s_NOUN.copy(tagged_sent)
    return s2


#You've now written a toy rule-based POS tagger.  Try improving it!  

#- You may copy your previous rules below and/or write entirely new ones. 
#- If you're feeling confident, try further organizing your code using a class.
#  - ex. `class EnglishRuleBasedPosTagger` with a `def tag(self, s: Sentence) -> Sentence:` method.

#Write a few tests to demonstrate its capabilities.  
#- What are some of its shortcomings?  
#- How does it improve upon the earlier version?  
#- What tagset did you adopt?

#def tag_with_rules_v2(s: Sentence) -> Sentence:
#    """
#    Takes a Sentence and returns a new Sentence with updates POS tags
#    by applying a series of rules for part of speech tagging
#    """
    # YOUR CODE HERE


def main():

	print("##########################  Unit 2 Tests  ##########################")

	UNK = Sentence.UNKNOWN
	s1  = Sentence(tokens = ["I", "'m", "fairly", "certain", "this", "will", "be", "easy"])
	s2  = Sentence(tokens = ["Do", "n't", "be", "an", "ugly", "bully"])
	s3  = Sentence(tokens=["I", "'m", "anxiously", "awaiting", "your", "answer"])
	s4  = Sentence(tokens = ["some", "cats", "LOVE", "that", "fish"])
	s5  = Sentence(tokens = ["No", "means", "no", ",", "Dr.", "No", "!"])
	s6  = Sentence(tokens=["ALL", "THE", "YOUNG", "DUDES", "CARRY", "THE","NEWS"])
	s7  = Sentence(tokens=["That", "mask", "is", "fairly", "scary"])
	s8  = Sentence(tokens=["Harry", "is", "very", "hairy"])
	s9  = Sentence(tokens=["I", "am", "the", "walrus"])
	s10 = Sentence(tokens=["We", "are", "the", "champions"])
	s11 = Sentence(tokens=["They", "were", "late"])
	s12 = Sentence(tokens=["Who", "was", "singing", "?"])
	s13 = Sentence(tokens=["The", "goat"], pos=["DT", UNK])
	s14 = Sentence(tokens=["The", "goat", "dreams"], pos=["DT", UNK, "VBZ"])
	s15 = Sentence(tokens=["The", "goat", "dreams"])
	s16 = Sentence(tokens=["The"], pos=["DT"])
	s17 = Sentence(tokens=["Those", "hungry", "goats", "bleat", "quietly"])
	s18 = Sentence(tokens=["Those", "hungry", "goats", "bleat", "quietly"], pos=[UNK, UNK, UNK, "V??", "RB"])
	s19 = Sentence(tokens=["All", "bats", "are", "righteously", "funky"])

	#Assert that code in rule_based_ly_adv_tagger() passes test cases
	res1 = rule_based_ly_adv_tagger(s1)
	print(res1)
	if res1.pos == (UNK, UNK, "RB", UNK, UNK, UNK, UNK, UNK):
		print("Test case 1 for rule_based_ly_adv_tagger() Passed.")
	else:
		print("Test case 1 for rule_based_ly_adv_tagger() Failed.")

	res2 = rule_based_ly_adv_tagger(s2)
	print(res2)
	if res2.pos == (UNK, UNK, UNK, UNK, "RB", "RB"):
		print("Test case 2 for rule_based_ly_adv_tagger() Passed, but reported a false positive.")
	else:
		print("Test case 2 for rule_based_ly_adv_tagger() Failed.")

	res3 = rule_based_ly_adv_tagger(s3)
	print(res3)
	if res3.pos == (UNK, UNK, UNK, UNK, "RB", "RB"):
		print("Test case 3 for rule_based_ly_adv_tagger() Passed.")
	else:
		print("Test case 3 for rule_based_ly_adv_tagger() Failed.")

	#Assert that code in rule_based_det_tagger() passes test cases
	res4 = rule_based_det_tagger(s4)
	print(res4)
	if res4.pos == ("DT", UNK, UNK, "DT", UNK):
		print("Test case 1 for rule_based_det_tagger() Passed.")
	else:
		print("Test case 1 for rule_based_det_tagger() Failed.")

	res5 = rule_based_det_tagger(s5)
	print(res5)
	if res5.pos == ("DT", UNK, "DT", UNK, UNK, "DT", UNK):
		print("Test case 2 for rule_based_det_tagger() Passed.")
	else:
		print("Test case 3 for rule_based_det_tagger() Failed.")

	res6 = rule_based_det_tagger(s6)
	print(res6)
	if res6.pos == ("DT", "DT", UNK, UNK, UNK, "DT", UNK):
		print("Test case 4 for rule_based_det_tagger() Passed.")
	else:
		print("Test case 4 for rule_based_det_tagger() Failed.")

	#Assert that code in rule_based_not_adv_adj_tagger() passes test cases
	res7 = rule_based_not_adv_adj_tagger(s7)
	print(res7)
	if res7.pos == (UNK, UNK, UNK, "RB", "JJ"):
		print("Test case 1 for rule_based_not_adv_adj_tagger() Passed.")
	else:
		print("Test case 1 for rule_based_not_adv_adj_tagger() Failed.")

	res8 = rule_based_not_adv_adj_tagger(s8)
	print(res8)
	if res8.pos == ("JJ", UNK, "JJ", "JJ"):
		print("Test case 2 for rule_based_not_adv_adj_tagger() Passed, but reported a false positive.")
	else:
		print("Test case 2 for rule_based_not_adv_adj_tagger() Failed.")

	#Assert that code in verb_copula() and det_noun_verb() passes test cases
	res9 = verb_copula(s9)
	print(res9)
	if res9.pos == (UNK, "VBP", UNK, UNK):
		print("Test case 1 for verb_copula() Passed.")
	else:
		print("Test case 1 for verb_copula() Failed.")

	res10 = verb_copula(s10)
	print(res10)
	if res10.pos == (UNK, "VBP", UNK, UNK):
		print("Test case 2 for verb_copula() Passed.")
	else:
		print("Test case 2 for verb_copula() Failed.")

	res11 = verb_copula(s11)
	print(res11)
	if res11.pos == (UNK, "VBD", UNK):
		print("Test case 3 for verb_copula() Passed.")
	else:
		print("Test case 3 for verb_copula() Failed.")

	res12 = verb_copula(s12)
	print(res12)
	if res12.pos == (UNK, "VBD", UNK, UNK):
		print("Test case 4 for verb_copula() Passed.")
	else:
		print("Test case 4 for verb_copula() Failed.")

	#Assert that code in det_noun_verb() passes test cases
	res13 = det_noun_verb(s13)
	print(res13)
	if res13.pos == ("DT", UNK):
		print("Test case 1 for det_noun_verb() Passed.")
	else:
		print("Test case 1 for det_noun_verb() Failed.")

	res14 = det_noun_verb(s14)
	print(res14)
	if res14.pos == ("DT", "NOUN", "VBZ"):
		print("Test case 2 for det_noun_verb() Passed.")
	else:
		print("Test case 2 for det_noun_verb() Failed.")

	res15 = det_noun_verb(s15)
	print(res15)
	if res15.pos == (UNK, UNK, UNK):
		print("Test case 3 for det_noun_verb() Passed.")
	else:
		print("Test case 3 for det_noun_verb() Failed.")

	res16 = det_noun_verb(s16)
	print(res16)
	if res16.pos == ("DT",):
		print("Test case 4 for det_noun_verb() Passed.")
	else:
		print("Test case 4 for det_noun_verb() Failed.")

	#Assert that code in tag_with_rules() passes test cases
	res17 = tag_with_rules(s17)
	print(res17)
	if res17.pos == ("DT", "JJ", UNK, UNK, "RB"):
		print("Test case 1 for tag_with_rules() Passed.")
	else:
		print("Test case 1 for tag_with_rules() Failed.")

	res18 = tag_with_rules(s18)
	print(res18)
	if res18.pos == ("DT", "JJ", UNK, "V??", "RB"):
		print("Test case 2 for tag_with_rules() Passed.")
	else:
		print("Test case 2 for tag_with_rules() Failed.")

	res19 = tag_with_rules(s19)
	print(res19)
	if res19.pos == ("DT", "JJ", UNK, "V??", "RB"):
		print("Test case 3 for tag_with_rules() Passed.")
	else:
		print("Test case 3 for tag_with_rules() Failed.")

if __name__ == "__main__":
	main()