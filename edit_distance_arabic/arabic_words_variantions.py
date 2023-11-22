DICT_LETTER_SWAP_FREQ_END = { # Dictionary of letter pairs with a substitution cost of COST_FREQ1 (0.1)
    'ه':['ه', 'ة', 'ا'], 
    'ة': ['ة', 'ه'],
    'ى': ['ى', 'ي', 'ا', 'ه', 'ة'],
}

DICT_LETTER_SWAP_FREQ_ALL = { # Dictionary of letter pairs with a substitution cost of COST_FREQ1 (0.1)

    'ا':['ا', 'ه'],
    'أ' :['أ','ا', 'إ', 'ئ', 'ؤ', 'ء'], 
    'إ':['إ','ا', 'أ', 'ئ', 'ؤ', 'ء'],
    'ؤ':['ؤ','ء', 'ئ', 'و'],
    'ئ':['ئ', 'ؤ', 'ء', 'ي'],
}

def swap_characters(string):
    permutations = []

    def recurse(current_string, remaining_indices):
        # Check if all characters have been swapped
        if not remaining_indices:
            # print (current_string)
            permutations.append(current_string)
            return

        # Swap characters based on the swap_dict
        for swap_index in remaining_indices:

            char_to_be_swaped = string[swap_index]
            swap_chars = [char_to_be_swaped]
            if char_to_be_swaped in DICT_LETTER_SWAP_FREQ_ALL:
              swap_chars = DICT_LETTER_SWAP_FREQ_ALL[char_to_be_swaped]

            if len(remaining_indices)==1:
              if char_to_be_swaped in DICT_LETTER_SWAP_FREQ_END:
                swap_chars += DICT_LETTER_SWAP_FREQ_END[char_to_be_swaped]

            

            for swap_char in swap_chars:

                modified_string = str(current_string[:swap_index]) + str(swap_char) + str(current_string[swap_index + 1:])

                new_remaining_indices = remaining_indices.copy()
                new_remaining_indices.remove(swap_index)

                recurse(modified_string, new_remaining_indices)
                

    # Initialize remaining indices for swapping
    remaining_indices = list(range(len(string)))

    # Recursively generate permutations
    recurse(string, remaining_indices)

    return set(permutations)  
        

if __name__ == "__main__":
  string1 = "مؤسسة"
  print (string1)
  print (swap_characters(string1))
