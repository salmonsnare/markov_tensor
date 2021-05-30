from fractions import Fraction
import markov_tensor

tensor_season_temp = {
    "profile": [[['夏', '冬']], [['暑い', '寒い']]], 
    "strands": {
        "[[['夏']], [['暑い']]]": Fraction(8, 10), 
        "[[['夏']], [['寒い']]]": Fraction(2, 10), 
        "[[['冬']], [['暑い']]]": Fraction(7, 10), 
        "[[['冬']], [['寒い']]]": Fraction(3, 10) 
    }
}

tensor_temp_inout = {
    "profile": [[['暑い', '寒い']], [['外出することがある', '外出することがない']]], 
    "strands": {
        "[[['暑い']], [['外出することがある']]]": Fraction(5, 10), 
        "[[['暑い']], [['外出することがない']]]": Fraction(5, 10), 
        "[[['寒い']], [['外出することがある']]]": Fraction(9, 10), 
        "[[['寒い']], [['外出することがない']]]": Fraction(1, 10) 
    }
}

def main():
    markov_tensor.print_tensor(markov_tensor.composition(tensor_season_temp, tensor_temp_inout))

if __name__ == "__main__":
    main()
