from fractions import Fraction
import markov_tensor

tensor_h = {
    "profile": [[['M', 'W']], [['H', 'M', 'L']]], 
    "strands": {
        "[[['M']], [['H']]]": Fraction(2, 10), 
        "[[['M']], [['M']]]": Fraction(6, 10), 
        "[[['M']], [['L']]]": Fraction(2, 10), 
        "[[['W']], [['H']]]": Fraction(1, 10), 
        "[[['W']], [['M']]]": Fraction(5, 10), 
        "[[['W']], [['L']]]": Fraction(4, 10)
    }
}

tensor_s = {
    "profile": [[['M', 'W']], [['S+', 'S-']]], 
    "strands": {
        "[[['M']], [['S+']]]": 0, 
        "[[['M']], [['S-']]]": 1, 
        "[[['W']], [['S+']]]": Fraction(5, 10), 
        "[[['W']], [['S-']]]": Fraction(5, 10) 
    }
}

tensor_c = {
    "profile": [[['O+', 'O-']], [['C+', 'C-']]], 
    "strands": {
        "[[['O+']], [['C+']]]": Fraction(2, 10),
        "[[['O+']], [['C-']]]": Fraction(8, 10),
        "[[['O-']], [['C+']]]": 0, 
        "[[['O-']], [['C-']]]": 1 
    }
}

tensor_p = {
    "profile": [[], [['M', 'W'], ['O+', 'O-']]], 
    "strands": {
        "[[], [['M'], ['O+']]]": Fraction(1, 10),
        "[[], [['M'], ['O-']]]": Fraction(4, 10),
        "[[], [['W'], ['O+']]]": Fraction(15, 100),
        "[[], [['W'], ['O-']]]": Fraction(35, 100)
    }
}

tensor_n = {
    "profile": [[['M', 'W'], ['O+', 'O-']], [['MO+', 'MO-', 'WO+', 'WO-']]], 
    "strands": {
        "[[['M'], ['O+']], [['MO+']]]": 1,
        "[[['M'], ['O+']], [['MO-']]]": 0,
        "[[['M'], ['O+']], [['WO+']]]": 0,
        "[[['M'], ['O+']], [['WO-']]]": 0,
        "[[['M'], ['O-']], [['MO+']]]": 0,
        "[[['M'], ['O-']], [['MO-']]]": 1,
        "[[['M'], ['O-']], [['WO+']]]": 0,
        "[[['M'], ['O-']], [['WO-']]]": 0,
        "[[['W'], ['O+']], [['MO+']]]": 0,
        "[[['W'], ['O+']], [['MO-']]]": 0,
        "[[['W'], ['O+']], [['WO+']]]": 1,
        "[[['W'], ['O+']], [['WO-']]]": 0,
        "[[['W'], ['O-']], [['MO+']]]": 0,
        "[[['W'], ['O-']], [['MO-']]]": 0,
        "[[['W'], ['O-']], [['WO+']]]": 0,
        "[[['W'], ['O-']], [['WO-']]]": 1 
    }
}


def main():
    # Problem 1.
    markov_tensor.print_tensor(markov_tensor.composition(tensor_p, tensor_n))
    # profile:  [[], [['MO+', 'MO-', 'WO+', 'WO-']]]
    # [[], [['MO+']]] 1/10
    # [[], [['MO-']]] 2/5
    # [[], [['WO+']]] 3/20
    # [[], [['WO-']]] 7/20

    # Problem 2.
    tensor_empty_mw = markov_tensor.first_marginalization(tensor_p, 2)
    markov_tensor.print_tensor(tensor_empty_mw)
    # profile:  [[], [['M', 'W']]]
    # [[], [['M']]] 1/2
    # [[], [['W']]] 1/2

    # Problem 3.
    tensor_empty_o = markov_tensor.second_marginalization(tensor_p, 2)
    markov_tensor.print_tensor(tensor_empty_o)
    # profile:  [[], [['O+', 'O-']]]
    # [[], [['O+']]] 1/4
    # [[], [['O-']]] 3/4

    # Problem 4.
    markov_tensor.print_tensor(markov_tensor.conversion(tensor_empty_mw, tensor_h))
    # profile:  [[['H', 'M', 'L']], [['M', 'W']]]
    # [[['H']], [['M']]] 2/3
    # [[['M']], [['M']]] 6/11
    # [[['L']], [['M']]] 1/3
    # [[['H']], [['W']]] 1/3
    # [[['M']], [['W']]] 5/11
    # [[['L']], [['W']]] 2/3

    markov_tensor.print_tensor(markov_tensor.conversion(tensor_empty_mw, tensor_s))
    # profile:  [[['S+', 'S-']], [['M', 'W']]]
    # [[['S+']], [['M']]] 0
    # [[['S-']], [['M']]] 2/3
    # [[['S+']], [['W']]] 1
    # [[['S-']], [['W']]] 1/3

    markov_tensor.print_tensor(markov_tensor.conversion(tensor_empty_o, tensor_c))
    # profile:  [[['C+', 'C-']], [['O+', 'O-']]]
    # [[['C+']], [['O+']]] 1
    # [[['C-']], [['O+']]] 4/19
    # [[['C+']], [['O-']]] 0
    # [[['C-']], [['O-']]] 15/19

    # Problem 5.
    markov_tensor.print_tensor(markov_tensor.conversion(tensor_p, tensor_n))
    # profile:  [[['MO+', 'MO-', 'WO+', 'WO-']], [['M', 'W'], ['O+', 'O-']]]
    # [[['MO+']], [['M'], ['O+']]] 1
    # [[['MO-']], [['M'], ['O+']]] 0
    # [[['WO+']], [['M'], ['O+']]] 0
    # [[['WO-']], [['M'], ['O+']]] 0
    # [[['MO+']], [['M'], ['O-']]] 0
    # [[['MO-']], [['M'], ['O-']]] 1
    # [[['WO+']], [['M'], ['O-']]] 0
    # [[['WO-']], [['M'], ['O-']]] 0
    # [[['MO+']], [['W'], ['O+']]] 0
    # [[['MO-']], [['W'], ['O+']]] 0
    # [[['WO+']], [['W'], ['O+']]] 1
    # [[['WO-']], [['W'], ['O+']]] 0
    # [[['MO+']], [['W'], ['O-']]] 0
    # [[['MO-']], [['W'], ['O-']]] 0
    # [[['WO+']], [['W'], ['O-']]] 0
    # [[['WO-']], [['W'], ['O-']]] 1

if __name__ == "__main__":
    main()
