"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    
    ### Tedious way
    
    list2 = []

    for element in list1:
        duplicate = False
        for index in range(len(list2)):
            if list2[index] == element:
                duplicate = True
        if duplicate == False:
            list2.append(element)

    return list2
    """
    result = []
    for element in list1:
        if element not in result:
            result.append(element)
            
    return result

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    
    ### tedious way
    
    list3 = []
    for element1 in list1:
        for element2 in list2:
            if element1 == element2:
                list3.append(element1)
    
    return remove_duplicates(list3)
    """
    result = []
    for element in list1:
        if element in list2:
            result.append(element)
            
    return result
    
# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """ 
    aux1 = list1[:]
    aux2 = list2[:]
    result = []
    
    while aux1 != [] and aux2 != []:
        aux10 = aux1[0]
        aux20 = aux2[0]
        
        if aux10 < aux20:
            result.append(aux10)
            aux1.pop(0)
        else:
            result.append(aux20)
            aux2.pop(0)
            
    result.extend(aux1)
    result.extend(aux2)
    return result

def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) <= 1:
        return list1
    else:
        midpoint = len(list1)/2
        
        aux1 = list1[0:midpoint]
        aux2 = list1[midpoint:]
        
        aux1 = merge_sort(aux1)
        aux2 = merge_sort(aux2)
        
        result = merge(aux1, aux2)
    return result

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if word == "":
        return [""]
    head = word[0]
    tail = word[1:]
    rest_strings = gen_all_strings(tail)
    new_strings = []
    for string in rest_strings:
        if len(string) == 0:
            new_strings.append(head)
            continue
        length = len(string)
        new_list = [string[:idx] + head + string[idx:] for idx in range(length + 1)]
        new_strings.extend(new_list)
    rest_strings.extend(new_strings)
    return rest_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    a_file = urllib2.urlopen(codeskulptor.file2url(filename))
    return list(a_file.readlines())

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()

    
    
