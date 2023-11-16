"""
This code calculates the weighted edit distance between two strings.
"""

import numpy as np


COST_FREQ1 = 0.1
DICT_LETTER_SWAP_FREQ1 = { # Dictionary of letter pairs with a substitution cost of COST_FREQ1 (0.1)
    'ه':'ة', 
    'ة': 'ه',
    'ا':'ه',
    'ه':'ا',
    'ؤ':'و',
    'و' :'ؤ',
    'أ' :'ا', 
    'أ' :'إ', 
    'أ' :'ئ', 
    'أ' :'ؤ', 
    'أ' :'ء', 
    'إ':'ا',
    'إ':'أ',
    'إ':'ئ',
    'إ':'ؤ',
    'إ':'ء',
    'ؤ':'ئ',
    'ؤ':'ء',
    'ئ':'ؤ',
    'ئ':'ء',
    'ئ':'ء',
    'ى': 'ي',
    'ى': 'ا',
    'ى': 'ه',
    'ى': 'ة',
    'ئ': 'ي',    
}

COST_FREQ2 = 0.5
DICT_LETTER_SWAP_FREQ2 = { # Dictionary of letter pairs with a substitution cost of COST_FREQ2 (0.5)
    'ء' : '',
    'ل' : 'م',
    'م' : 'ل',
    'ن' : 'ل',
    'ل' : 'ن',
    'ل' : 'ر',
    'ر' : 'ل',
    'م' : 'ن',
    'ن' : 'م',
    'ر' : 'م',
    'م' : 'ر',
    'ن' : 'ر',
    'ر' : 'ن',
    'ر' : 'ن',
    'ذ' : 'ز',
    'ز' : 'ذ',
    'ظ' : 'ذ',
    'ذ' : 'ظ',
    'ز' : 'ظ',
    'ظ' : 'ز',
    'ظ' : 'ض',
    'ض' : 'ظ',
    'ض' : 'د',
    'د' : 'ض',
  

}

LIST_DICT_LETTER_SWAP_BY_FREQ = [
    (DICT_LETTER_SWAP_FREQ1, COST_FREQ1),
    (DICT_LETTER_SWAP_FREQ2, COST_FREQ2)
]


def weighted_letter_swap(
        letter_1, letter_2, def_substitution_cost, list_dict_freq_costs):
    """
    Determines the cost of substituting one letter for another based on their frequency of substitution.

    Args:
        letter_1 (str): The first letter.
        letter_2 (str): The second letter.
        def_substitution_cost (float): the default substitution cost if not in the dictionaries.
        list_dict_freq_costs (list): list of tuples: dictionary and cost.

    Returns:
        int: The cost of substituting letter_1 for letter_2.
    """
    cost = def_substitution_cost
    for dict_letter_swap, cost in list_dict_freq_costs:
        if letter_1 in dict_letter_swap and dict_letter_swap[letter_1]==letter_2:
            cost = cost
            break
        if letter_2 in dict_letter_swap and dict_letter_swap[letter_2]==letter_1:
            cost = cost
            break 
    return cost

def weighted_edit_distance(
        string1, string2, insertion_cost=1, deletion_cost=1, def_substitution_cost=1, 
        list_dict_freq_costs=LIST_DICT_LETTER_SWAP_BY_FREQ):
    """
    Calculates the weighted edit distance between two strings.

    Args:
        string1 (str): The first string.
        string2 (str): The second string.
        insertion_cost (int): The cost of inserting a character.
        deletion_cost (int): The cost of deleting a character.
        list_dict_freq_costs (list): list of tuples (dictionary, cost).

    Returns:
        int: The weighted edit distance between the two strings.
    """
    n = len(string1)
    m = len(string2)

    d = np.zeros((n + 1, m + 1))

    # Initialize the first row with deletion costs
    for i in range(1, n + 1):
        d[i, 0] = deletion_cost * i

    # Initialize the first column with insertion costs
    for j in range(1, m + 1):
        d[0, j] = insertion_cost * j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if string1[i - 1] == string2[j - 1]:
                substitution_cost = 0
            else:
                substitution_cost = weighted_letter_swap(
                    string1[i - 1], string2[j - 1], def_substitution_cost, list_dict_freq_costs)          

            d[i, j] = min(d[i - 1, j] + deletion_cost,
                          d[i, j - 1] + insertion_cost,
                          d[i - 1, j - 1] + substitution_cost)

    return d[n, m]


if __name__ == "__main__":
    string1 = "مؤسسة"
    string2 = "موسسة"
     
    weighted_distance = weighted_edit_distance(string1, string2)
    normalized_weighted_distance = weighted_distance/len(string2)
    
    print("Weighted edit distance:", weighted_distance)
    print ("Normalized weighted edit distance:", normalized_weighted_distance)
