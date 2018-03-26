"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    result_list = []
    result_list_index = 0
    number_of_zeros = 0 
    
    for dummy_index in range(len(line)): # create an empty result list
        result_list.append(0)
            
    for dummy_value in line:  # slide all non-zero values to the left side
        if dummy_value != 0:
            result_list[result_list_index] = dummy_value
            result_list_index += 1  
            
    for dummy_index in range(len(result_list)-1):  # merge equal tiles and count the number of zeros
        if result_list[dummy_index] == result_list[dummy_index + 1]:
            result_list[dummy_index] *= 2
            result_list[dummy_index + 1] = 0 
            number_of_zeros += 1
    
    while number_of_zeros >= 0:
        for dummy_index in range(len(result_list)-1):  # slide all non-zero values to the left side one position for each
            if result_list[dummy_index] == 0:          # zero in the list (work a more efficient way)
                result_list[dummy_index] = result_list[dummy_index + 1]
                result_list[dummy_index + 1] = 0
        number_of_zeros -= 1
        
    return result_list

def test_merge():
    """
    Test the merge function

    [2, 0, 2, 4] should return [4, 4, 0, 0]
    [0, 0, 2, 2] should return [4, 0, 0, 0]
    [2, 2, 0, 0] should return [4, 0, 0, 0]
    [2, 2, 2, 2, 2] should return [4, 4, 2, 0, 0]
    [8, 16, 16, 8] should return [8, 32, 8, 0]
    """

    test1 = [2, 0, 2, 4]
    test2 = [0, 0, 2, 2]
    test3 = [2, 2, 0, 0]
    test4 = [2, 2, 2, 2, 2]
    test5 = [2, 2, 2, 2, 2, 4, 4, 4, 2]
    test6 = [8, 16, 16, 8]

    print merge(test1)
    print merge(test2)
    print merge(test3)
    print merge(test4)
    print merge(test5)
    print merge(test6)
    
test_merge()
