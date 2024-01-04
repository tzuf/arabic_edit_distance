"""
This code calculates the weighted edit distance between two strings.
"""

import numpy as np
from nltk.tokenize import word_tokenize
from Levenshtein import distance as lev


PREFIX = [
    'ال', 'ع','و','وال', 'لل', 'ل','ب', 'بال', 'عال', 'وعال', 'وع','ولل', 'ول', 'وب']

COST_FREQ1 = 0.1
DICT_LETTER_SWAP_FREQ1 = { # Dictionary of letter pairs with a substitution cost of COST_FREQ1 (0.1)
    'ه':['ة', 'ا'], 
    'ة': ['ه'],
    'ا':['ه',''],
    'و' :['ؤ'],
    'أ' :['ا', 'إ', 'ئ', 'ؤ', 'ء'], 
    'إ':['ا', 'أ', 'ئ', 'ؤ', 'ء'],
    'ؤ':['ء', 'ئ', 'و'],
    'ئ':['ؤ', 'ء', 'ي'],
    'ى': ['ي', 'ا', 'ه', 'ة'],
}

COST_FREQ2 = 0.5
DICT_LETTER_SWAP_FREQ2 = { # Dictionary of letter pairs with a substitution cost of COST_FREQ2 (0.5)
    'ء' : [''],
    'ل' : ['م','ن', 'ر'],
    'م' : ['ل', 'ن', 'ر'],
    'ن' : ['ل', 'م', 'ر'],
    'ر' : ['ل', 'م', 'ن'],
    'ذ' : ['ز', 'ظ'],
    'ظ' : ['ذ', 'ز', 'ض'],
    'ز' : ['ظ', 'ذ'],
    'ض' : ['ظ', 'د'],
    'د' : ['ض'],
  

}

LIST_DICT_LETTER_SWAP_BY_FREQ = [
    (DICT_LETTER_SWAP_FREQ1, COST_FREQ1),
    (DICT_LETTER_SWAP_FREQ2, COST_FREQ2)
]

class ArabicEditDistance():
    def __init__(
            self, 
            insertion_cost=1, 
            deletion_cost=1, 
            substitution_cost=1,
            list_dict_freq_costs=LIST_DICT_LETTER_SWAP_BY_FREQ,
            ignore_prefix=False,
            is_standard_edit_distance = False
            ):
        """
        Args:
            string1 (str): The first string.
            string2 (str): The second string.
            insertion_cost (int): The cost of inserting a character.
            deletion_cost (int): The cost of deleting a character.
            list_dict_freq_costs (list): list of tuples (dictionary, cost).
            ignore_prefix: if 'True' then the edit distance will not consider optional prefixes.

        """
        self.def_insertion_cost = insertion_cost
        self.def_deletion_cost = deletion_cost
        self.def_substitution_cost = substitution_cost
        self.list_dict_freq_costs = list_dict_freq_costs
        self.ignore_prefix = ignore_prefix
        self.is_standard_edit_distance = is_standard_edit_distance

    def __weighted_letter_swap(
            self, letter_1, letter_2):
        """
        Determines the cost of substituting one letter for another based on their frequency of substitution.

        Args:
            letter_1 (str): The first letter.
            letter_2 (str): The second letter.

        Returns:
            int: The cost of substituting letter_1 for letter_2.
        """
        substitution_cost = self.def_substitution_cost
        for dict_letter_swap, dict_cost in self.list_dict_freq_costs:
            if letter_1 in dict_letter_swap and letter_2 in dict_letter_swap[letter_1]:
                substitution_cost = dict_cost
                break
            elif letter_2 in dict_letter_swap and letter_1 in dict_letter_swap[letter_2]:
                substitution_cost = dict_cost
                break 
        return substitution_cost

    def get_edit_distance(self, pred_string, gt_string):
        """
        Calculates the weighted edit distance between two strings.

        Args:
            string1 (str): The first string.
            string2 (str): The second string.
        Returns:
            float: The weighted edit distance between the two strings.
            float: The normalized score.
        """
        if self.is_standard_edit_distance:
            edit_distance = lev(pred_string, gt_string)
            score = round((1-edit_distance/len(gt_string))*100)
            return edit_distance, score

        else:
            return self._get_arabic_edit_distance(pred_string, gt_string)

    def _get_arabic_edit_distance(
            self, string1, string2):
        """
        Calculates the weighted edit distance between two strings.

        Args:
            string1 (str): The first string.
            string2 (str): The second string.
        Returns:
            float: The weighted edit distance between the two strings.
            float: The normalized score.
        """
        min_weighted_distance = self.__weighted_edit_distance(
            string1=string1, 
            string2=string2)
        if self.ignore_prefix:
            return min_weighted_distance
        
        optional_pre_str1 = []
        optional_pre_str2 = []

        for pre in PREFIX:
            len_pre = len(pre)
            if string1[:len_pre] == pre:
                optional_pre_str1.append(string1[len_pre:])
            if string2[:len_pre] == pre:
                optional_pre_str2.append(string2[len_pre:]) 

        for string_no_pre1 in optional_pre_str1:    
            for string_no_pre2 in optional_pre_str2:

                weighted_distance = self.__weighted_edit_distance(
                    string1=string_no_pre1, 
                    string2=string_no_pre2)
                
                if weighted_distance<min_weighted_distance:
                    min_weighted_distance = weighted_distance
        
        score = round((1-min_weighted_distance/len(string2))*100)
        return min_weighted_distance, score

    def __weighted_edit_distance(
            self, string1, string2):
        """
        Calculates the weighted edit distance between two strings.

        Args:
            string1 (str): The first string.
            string2 (str): The second string.

        Returns:
            int: The weighted edit distance between the two strings.
        """
        n = len(string1)
        m = len(string2)

        d = np.zeros((n + 1, m + 1))

        # Initialize the first row with deletion costs
        for i in range(1, n + 1):
            d[i, 0] = self.def_deletion_cost * i

        # Initialize the first column with insertion costs
        for j in range(1, m + 1):
            d[0, j] = self.def_insertion_cost * j

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if string1[i - 1] == string2[j - 1]:
                    substitution_cost = 0
                else:
                    substitution_cost = self.__weighted_letter_swap(
                        string1[i - 1], string2[j - 1])          

                d[i, j] = min(d[i - 1, j] + self.def_deletion_cost,
                            d[i, j - 1] + self.def_insertion_cost,
                            d[i - 1, j - 1] + substitution_cost)

        return d[n, m]


    def fuzzy_token_set_ratio(self, pred_string, gt_string):

        gt_tokens = word_tokenize(gt_string)
        pred_tokens = word_tokenize(pred_string)

        total_score = 0
        for gt_token in gt_tokens:
            max_score = 0
            for pred_token in pred_tokens:
                _, score = self.get_edit_distance(pred_string=pred_token, gt_string=gt_token)
                if max_score<score:
                    max_score = score

            total_score += max_score

        return round(total_score/len(gt_tokens))




if __name__ == "__main__":
    pred_string = "Juma"
    gt_string = "House of the martyr Ibrahim Juma Mahmoud Al-Najjar"
     
    edit_distance = ArabicEditDistance(is_standard_edit_distance=True)

    print (edit_distance.fuzzy_token_set_ratio(pred_string=pred_string,gt_string=gt_string))

    pred_string = "مسجد"
    gt_string = "مسجد الدين الشهير"

    print (edit_distance.fuzzy_token_set_ratio(pred_string=pred_string,gt_string=gt_string))
