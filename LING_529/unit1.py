"""
Unit 1 code from LING 529 Human Language Technology I
Course taught by Dr. Gus Hahn-Powell
Author: Channing Donaldson
University of Arizona
Fall 2021


Unit 1 served the purpose of introducing ourselves to Dr. Hahn, learning how to utilize Juypter Notebook and testing our basic programming proficiency.

This document includes code written by Channing Donaldson with function frameworks provided by Dr. Hahn-Powell.
"""

def multiply(a: int, b: int) -> int:
	"""
	Takes two integers and returns their product
	"""
	return a*b

def weird_request(seq):
	"""
	:param seq: a list of anything
	takes a list, reverses its contents, drops the element at the front, and returns what remains.
	"""
	while len(seq) > 0:
		seq.reverse()
		seq.pop(0)
		return seq
	else:
		return []

def main():

	print("##########################  Unit 1 Tests  ##########################")

	#Assert that code in multiply() passes test cases
	if multiply(2,2) == 4:
		print("Test case 1 for multiply() Passed: (2x2 = 4)")
	else:
		print("Test case 1 for multiply() Failed. Multiplication error.")

	if multiply(2,0) == 0:
		print("Test case 2 for multiply() Passed: (2x0 = 0)")
	else:
		print("Test case 2 for multiply() Failed. Multiplication error.")

	if multiply(-1,-1) == 1:
		print("Test case 3 for multiply() Passed: (-1x-1 = 1) \n")
	else:
		print("Test case 3 for multiply() Failed Multiplication error. \n")

	#Assert that code in weird_request() passes test cases
	if weird_request(["a","b","c"]) == ["b","a"]:
		print("Test case 1 for weird_request() Passed: [\"b\",\"a\"] is a subset of [\"a\",\"b\",\"c\"]")
	else:
		print("Test case 1 for weird_request() Failed. Subset not a member of the set.")

	
	if weird_request([1,2,3]) == [2,1]:
		print("Test case 2 for weird_request() Passed. [2,1] is a subset of [1,2,3]")
	else:
		print("Test case 2 for weird_request() Failed. Subset not a member of the set.")

	#Assert that code in weird_request() passes test cases
	if weird_request([1]) == []:
		print("Test case 3 for weird_request() Passed. [] is a subset of [1]")
	else:
		print("Test case 3 for weird_request() Failed. Subset not a member of the set.")

	#Assert that code in weird_request() passes test cases
	if weird_request([]) == []:
		print("Test case 4 for weird_request() Passed. [] is a subset of []")
	else:
		print("Test case 4 for weird_request() Failed. Subset not a member of the set.")

if __name__ == "__main__":
	main()