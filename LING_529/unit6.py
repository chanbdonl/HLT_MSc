"""
Unit 6 code from LING 529 Human Language Technology I
Course taught by Dr. Gus Hahn-Powell
Author: Channing Donaldson
University of Arizona
Fall 2021


In unit 6 we write functions that perform the following: calculate the dot product, calculate Euclidean distance, normalize a vector, calculate cosine similarity and cosine distance, identify the centroid and the medoid of a set of vectors.

This document includes code written by Channing Donaldson with function frameworks provided by Dr. Hahn-Powell.
"""

from typing import Any, Callable, Dict, Iterable, List, Tuple, Union
from collections import Counter
from math import isclose

# we'll be using this for some of our tests
def test_isclose(x: List[float], y: List[float], rel_tol=1.e-6) -> bool:
    if len(x) != len(y):
        return False
    for i in range(len(x)):
        if not isclose(x[i], y[i], rel_tol=rel_tol):
            return False
    return True

def divide_by_scalar(x: List[float], scalar: int) -> List[float]:
    """
    Takes a list of floats representing the vector $x$ and divides each element by a scalar value.
    """
    results = list()
    
    for i in x:
        quotient = i / float(scalar)
        results.append(quotient)
    #print(results)
    return results

def p_norm(x: List[float], p: int) -> float:
    assert p >= 1
    """
    Takes a List (x) representing a vector and p.
    Returns the $p$-norm for $\vec{x}$.
    """

    #Absolute value of each element of the vector
    ab_vals  = list()
    
    for i in x:
        pos_val = abs(i)
        ab_vals.append(pos_val)
    #print(ab_vals)   

    #Raise each absolute value to the power of p
    pow_vals = list()
    
    for j in ab_vals:
        powered = j ** p
        pow_vals.append(powered)
    #print(pow_vals)
    
    #sum all raised absolute value
    summed = float()
    for k in pow_vals:
        summed += k
    #print(summed)
    
    #pth root or raise to the power of 1/p
    root = summed ** (1. / p)
    
    #print(type(root))
    #print(root)
    return root

def normalize(x: List[float]) -> List[float]:
    """
    Returns the 2-norm of the vector x.
    """
    mag = p_norm(x, 2)
    
    norms = list()
    
    for i in range(len(x)):
        if mag <= 0.0:
            norm = x[i] / 0.00001
            norms.append(norm)
        else:
            norm = x[i] / mag
            norms.append(norm)
    #print(norms)
    return norms

def dot_product(x: List[float], y: List[float]) -> float:
    """
    Returns the inner product of two 1D vectors.
    """
    assert len(x) == len(y)
    
    return sum(x_i*y_i for x_i, y_i in zip(x, y))

def euclidean_distance(x: List[float], y: List[float]) -> float:
    """
    Returns in the Euclidean distance of two 1D vectors.
    """
    
    summed_list = sum([(x_i - y_i)**2 for x_i, y_i in zip(x, y)])
    eu_dist = summed_list ** .5
    return eu_dist

def cosine_similarity(x: List[float], y: List[float]) -> float:
    """
    Calculates the cosine similarity of two vectors.
    """
    #normx/y should be a single number
    dotprod = dot_product(x, y)
    normx   = p_norm(x, 2)
    normy   = p_norm(y, 2)
    
    cosine  = dotprod / (normx * normy)
    #print(cosine)
    return(cosine)

def find_centroid(X: List[List[float]]) -> List[float]:
    """
    Calculates centroid given a matrix X.
    X is represented using a list of lists.
    Each inner list is a vector.
    """
    # all vectors must have the same dimensionality
    assert len(set(len(v) for v in X)) == 1

# type for a function that takes a pair of params representing two vectors and returns a float
DistFunction = Callable[[List[float], List[float]], float]

def find_medoid(X: List[List[float]], dist_function: DistFunction) -> List[float]:
    """
    Finds the distance medoid of X (i.e., the vector in X that is on average closest to every other vector)
    """
    # YOUR CODE HERE
    raise NotImplementedError()

def main():

    print("########################## LING 529 Unit 6 Tests  ##########################")

    #Assert that code in divide_by_scaler() passes test cases
    if divide_by_scalar([12., 3., 5.3], 4) == [3.0, 0.75, 1.325]:
        print("Test case 1 for divide_by_scalar() Passed: ([12., 3., 5.3], 4) == [3.0, 0.75, 1.325]")
    else:
        print("Test case 1 for divide_by_scalar() Failed. Division error.")

    if divide_by_scalar([0., 0., 0.], 17) == [0., 0., 0.]:
        print("Test case 2 for divide_by_scalar() Passed: ([0., 0., 0.], 17) == [0., 0., 0.]")
    else:
        print("Test case 2 for divide_by_scalar() Failed. Division error.")

    #Assert that code in p_norm() passes test cases
    if isclose(p_norm([1., 2., 3.], p=1), 6., rel_tol=1.e-0) == True:
        print("Test case 1 for p_norm() Passed: isclose(p_norm([1., 2., 3.], p=1), 6., rel_tol=1.e-0) == True")
    else:
        print("Test case 1 for p_norm() Failed. L1 norm for vector is not within acceptable range.")

    if isclose(p_norm([1., 2., 3.], p=2), 3.74165738, rel_tol=1.e-6) == True:
        print("Test case 2 for p_norm() Passed: isclose(p_norm([1., 2., 3.], p=2), 3.74165738, rel_tol=1.e-6) == True")
    else:
        print("Test case 2 for p_norm() Failed. L2 norm for vector not within acceptable range.")

    if isclose(p_norm([1., 2., 3.], p=3), 3.301927, rel_tol=1.e-6) == True:
        print("Test case 3 for p_norm() Passed: isclose(p_norm([1., 2., 3.], p=3), 3.301927, rel_tol=1.e-6) == True.")
    else:
        print("Test case 3 for p_norm() Failed. p_norm for vector not within acceptable range.")

    if p_norm([1., 2., 3.], p=1) == 6:
        print("Test case 4 for p_norm() Passed. p_norm([1., 2., 3.], p=1) == 6")
    else:
        print("Test case 4 for p_norm() Failed. p_norm does not equal 6.")

    if isclose(p_norm([7., 14., 3.], p=2), 15.9373774, rel_tol=1.e-6) == True:
        print("Test case 5 for p_norm() Passed: isclose(p_norm([7., 14., 3.], p=2), 15.9373774, rel_tol=1.e-6) == True")
    else:
        print("Test case 5 for p_norm() Failed. p_norm not within accpetable range")

#Assert that code in normalize() passes test cases
    if test_isclose(normalize([1., 2., 3.]), [0.26726124, 0.53452248, 0.80178373], rel_tol=1.e-6) == True:
        print("Test case 1 for normalize() Passed: test_isclose(normalize([1., 2., 3.]), [0.26726124, 0.53452248, 0.80178373], rel_tol=1.e-6) == True")
    else:
        print("Test case 1 for normalize() Failed. Vector not normalized to acceptable range.")

    if test_isclose(normalize([10., 20., 30.]), [0.26726124, 0.53452248, 0.80178373], rel_tol=1.e-6) == True:
        print("Test case 2 for normalize() Passed: test_isclose(normalize([10., 20., 30.]), [0.26726124, 0.53452248, 0.80178373], rel_tol=1.e-6) == True")
    else:
        print("Test case 2 for normalize() Failed. Vector not normalized to acceptable range.")

    if test_isclose(normalize([100., 200., 300.]), [0.26726124, 0.53452248, 0.80178373], rel_tol=1.e-6) == True:
        print("Test case 3 for normalize() Passed: test_isclose(normalize([100., 200., 300.]), [0.26726124, 0.53452248, 0.80178373], rel_tol=1.e-6) == True.")
    else:
        print("Test case 3 for normalize() Failed. Vector not normalized to acceptable range.")

    if test_isclose(normalize([1000., 2000., 3000.]), [0.26726124, 0.53452248, 0.80178373], rel_tol=1.e-6):
        print("Test case 4 for normalize() Passed. test_isclose(normalize([1000., 2000., 3000.]), [0.26726124, 0.53452248, 0.80178373], rel_tol=1.e-6) == True")
    else:
        print("Test case 4 for normalize() Failed. Vector not normalized to acceptable range.")

    if test_isclose(normalize([52., -2., 13.]), [0.96946785, -0.03728723, 0.24236696], rel_tol=1e-05) == True:
        print("Test case 5 for normalize() Passed: test_isclose(normalize([52., -2., 13.]), [0.96946785, -0.03728723, 0.24236696], rel_tol=1e-05) == True")
    else:
        print("Test case 5 for normalize() Failed. Vector not normalized to acceptable range.")

    if test_isclose(normalize([520., -20., 130.]), [0.96946785, -0.03728723, 0.24236696], rel_tol=1e-05) == True:
        print("Test case 6 for normalize() Passed: test_isclose(normalize([520., -20., 130.]), [0.96946785, -0.03728723, 0.24236696], rel_tol=1e-05) == True")
    else:
        print("Test case 6 for normalize() Failed. Vector not normalized to acceptable range.")

    if test_isclose(normalize([0., 0., 0.]), [0., 0., 0.], rel_tol=1e-02) == True:
        print("Test case 7 for normalize() Passed: test_isclose(normalize([0., 0., 0.]), [0., 0., 0.], rel_tol=1e-02) == True")
    else:
        print("Test case 7 for normalize() Failed. Vector not normalized to acceptable range.")

#Assert that code in dot_product() passes test cases
    if dot_product([0., 0., 0.],   [0., 0., 0.]) == 0.:
        print("Test case 1 for dot_product() Passed: dot_product([0., 0., 0.],   [0., 0., 0.]) == 0.")
    else:
        print("Test case 1 for dot_product() Failed. Dot Product incorrect.")

    if dot_product([0., 2., 0.],   [0., 0., 0.]) == 0.:
        print("Test case 2 for dot_product() Passed: dot_product([0., 2., 0.],   [0., 0., 0.]) == 0.")
    else:
        print("Test case 2 for dot_product() Failed. Dot Product incorrect.")

    if dot_product([0., 0., 0.],   [0., 2., 0.]) == 0.:
        print("Test case 3 for dot_product() Passed: dot_product([0., 0., 0.],   [0., 2., 0.]) == 0.")
    else:
        print("Test case 3 for dot_product() Failed. Dot Product incorrect.")

    if dot_product([12., 3., 7.], [2., 4., 4.]) == 64.:
        print("Test case 4 for dot_product() Passed. dot_product([12., 3., 7.], [2., 4., 4.]) == 64.")
    else:
        print("Test case 4 for dot_product() Failed. Dot Product incorrect.")

#Assert that code in euclidean_distance() passes test cases
    if euclidean_distance([1., 2., 3.], [1., 2., 3.]) == 0.:
        print("Test case 1 for euclidean_distance() Passed: euclidean_distance([1., 2., 3.], [1., 2., 3.]) == 0.")
    else:
        print("Test case 1 for euclidean_distance() Failed. Euclidean distance incorrect.")

    if euclidean_distance([1., 2., 3.], [2., 2., 3.]) == 1.:
        print("Test case 2 for euclidean_distance() Passed: euclidean_distance([1., 2., 3.], [2., 2., 3.]) == 1.")
    else:
        print("Test case 2 for euclidean_distance() Failed. Euclidean distance incorrect.")

    if euclidean_distance([1., 2., 3.], [0., 2., 3.]) == 1.:
        print("Test case 3 for euclidean_distance() Passed: euclidean_distance([1., 2., 3.], [0., 2., 3.]) == 1.")
    else:
        print("Test case 3 for euclidean_distance() Failed. Dot Product incorrect.")

    if euclidean_distance([1., 2., 3.], [0., 0., 0.]) == p_norm([1., 2., 3.], p=2):
        print("Test case 4 for euclidean_distance() Passed. euclidean_distance([1., 2., 3.], [0., 0., 0.]) == p_norm([1., 2., 3.], p=2)")
    else:
        print("Test case 4 for euclidean_distance() Failed. The Euclidean distance of some vector v and the origin is not equal to the L2 norm of v.")

#Assert that code in cosine_similarity() passes test cases
    if isclose(cosine_similarity([100., 200., 300.], [100., 200., 300.]), 1., rel_tol=1.e-6) == True:
        print("Test case 1 for cosine_similarity() Passed: isclose(cosine_similarity([100., 200., 300.], [100., 200., 300.]), 1., rel_tol=1.e-6)")
    else:
        print("Test case 1 for cosine_similarity() Failed. Incorrect cosine similarity.")

    if isclose(cosine_similarity([100., 200., 300.], [0.26726124, 0.53452248, 0.80178373]), 1., rel_tol=1.e-6) == True:
        print("Test case 2 for cosine_similarity() Passed: isclose(cosine_similarity([100., 200., 300.], [0.26726124, 0.53452248, 0.80178373]), 1., rel_tol=1.e-6)")
    else:
        print("Test case 2 for cosine_similarity() Failed. Incorrect cosine similarity.")

    if isclose(cosine_similarity([2., 2., 2.], [-2., -2., -2.]), -1., rel_tol=1.e-2) == True:
        print("Test case 3 for cosine_similarity() Passed: isclose(cosine_similarity([2., 2., 2.], [-2., -2., -2.]), -1., rel_tol=1.e-2)")
    else:
        print("Test case 3 for cosine_similarity() Failed. Incorrect cosine similarity.")

    if isclose(cosine_similarity([2., 0.], [0., 2.]), 0., rel_tol=1.e-2) == True:
        print("Test case 4 for cosine_similarity() Passed. isclose(cosine_similarity([2., 0.], [0., 2.]), 0., rel_tol=1.e-2)")
    else:
        print("Test case 4 for cosine_similarity() Failed. Incorrect cosine similarity.")

    if cosine_similarity([2., 0.], [0., 2.]) == dot_product([2., 0.], [0., 2.]):
        print("Test case 5 for cosine_similarity() Passed. cosine_similarity([2., 0.], [0., 2.]) == dot_product([2., 0.], [0., 2.])")
    else:
        print("Test case 5 for cosine_similarity() Failed. If the cosine is 0, then the dot product must also be 0.")

if __name__ == "__main__":
	main()