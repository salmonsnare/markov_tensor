from fractions import Fraction # 分数を取り扱うために Fraction をインポートします。
import markov_tensor # 結合演算 composition を用いるためにインポートします。

"""
　　黒　白
-----------
赤  0.1 0.2
緑  0.2 0.3
青  0.7 0.5
"""

# 表1 の Python の辞書による表現です。
tensor_a = {
    "profile": [[['黒', '白']], [['赤', '緑', '青']]], 
    "strands": {
        "[[['黒']], [['赤']]]": Fraction(1, 10), 
        "[[['黒']], [['緑']]]": Fraction(2, 10), 
        "[[['黒']], [['青']]]": Fraction(7, 10), 
        "[[['白']], [['赤']]]": Fraction(2, 10), 
        "[[['白']], [['緑']]]": Fraction(3, 10), 
        "[[['白']], [['青']]]": Fraction(5, 10)
    }
}

"""
　　　　　　　　　　　　赤　緑　青
-----------------------------------------
白色のランプが光る  　　0.8 0.9 0.9
白色のランプが光らない  0.2 0.1 0.1
"""

# 表2 の Python の辞書による表現です。
tensor_b = {
    "profile": [[['赤', '緑', '青']], [['白色のランプが光る', '白色のランプが光らない']]], 
    "strands": {
        "[[['赤']], [['白色のランプが光る']]]": Fraction(8, 10),
        "[[['緑']], [['白色のランプが光る']]]": Fraction(9, 10),
        "[[['青']], [['白色のランプが光る']]]": Fraction(9, 10),
        "[[['赤']], [['白色のランプが光らない']]]": Fraction(2, 10),
        "[[['緑']], [['白色のランプが光らない']]]": Fraction(1, 10),
        "[[['青']], [['白色のランプが光らない']]]": Fraction(1, 10)
    }
}

# 表4 の Python の辞書による表現です。
tensor_c = {
    "profile": [[['黒', '白'], ['金', '銀']], [['赤', '緑', '青'], ['桃', '紫']]], 
    "strands": {
        "[[['黒'], ['金']], [['赤'], ['桃']]]": Fraction(1, 10), 
        "[[['黒'], ['金']], [['赤'], ['紫']]]": Fraction(1, 10), 
        "[[['黒'], ['金']], [['緑'], ['桃']]]": Fraction(1, 10), 
        "[[['黒'], ['金']], [['緑'], ['紫']]]": Fraction(1, 10), 
        "[[['黒'], ['金']], [['青'], ['桃']]]": Fraction(1, 10), 
        "[[['黒'], ['金']], [['青'], ['紫']]]": Fraction(5, 10), 

        "[[['黒'], ['銀']], [['赤'], ['紫']]]": Fraction(1, 10),
        "[[['黒'], ['銀']], [['赤'], ['桃']]]": Fraction(1, 10), 
        "[[['黒'], ['銀']], [['緑'], ['桃']]]": Fraction(1, 10), 
        "[[['黒'], ['銀']], [['緑'], ['紫']]]": Fraction(1, 10),
        "[[['黒'], ['銀']], [['青'], ['桃']]]": Fraction(5, 10), 
        "[[['黒'], ['銀']], [['青'], ['紫']]]": Fraction(1, 10), 

        "[[['白'], ['金']], [['赤'], ['桃']]]": Fraction(1, 10), 
        "[[['白'], ['金']], [['赤'], ['紫']]]": Fraction(1, 10), 
        "[[['白'], ['金']], [['緑'], ['桃']]]": Fraction(1, 10), 
        "[[['白'], ['金']], [['緑'], ['紫']]]": Fraction(5, 10), 
        "[[['白'], ['金']], [['青'], ['桃']]]": Fraction(1, 10), 
        "[[['白'], ['金']], [['青'], ['紫']]]": Fraction(1, 10), 

        "[[['白'], ['銀']], [['赤'], ['紫']]]": Fraction(1, 10), 
        "[[['白'], ['銀']], [['赤'], ['桃']]]": Fraction(1, 10), 
        "[[['白'], ['銀']], [['緑'], ['桃']]]": Fraction(5, 10), 
        "[[['白'], ['銀']], [['緑'], ['紫']]]": Fraction(1, 10),
        "[[['白'], ['銀']], [['青'], ['桃']]]": Fraction(1, 10), 
        "[[['白'], ['銀']], [['青'], ['紫']]]": Fraction(1, 10)
    }
}

# 表5 の Python の辞書による表現です。
tensor_d = {
    "profile": [[['赤', '緑', '青'], ['桃', '紫']], [['白色のランプ 1 が光る', '白色のランプ 1 が光らない'], ['白色のランプ 2 が光る', '白色のランプ 2 が光らない']]], 
    "strands": {
        "[[['赤'], ['桃']], [['白色のランプ 1 が光る'], ['白色のランプ 2 が光る']]]": Fraction(1, 10),
        "[[['赤'], ['桃']], [['白色のランプ 1 が光る'], ['白色のランプ 2 が光らない']]]": Fraction(2, 10),
        "[[['赤'], ['桃']], [['白色のランプ 1 が光らない'], ['白色のランプ 2 が光る']]]": Fraction(3, 10),
        "[[['赤'], ['桃']], [['白色のランプ 1 が光らない'], ['白色のランプ 2 が光らない']]]": Fraction(4, 10),

        "[[['赤'], ['紫']], [['白色のランプ 1 が光る'], ['白色のランプ 2 が光る']]]": Fraction(4, 10),
        "[[['赤'], ['紫']], [['白色のランプ 1 が光る'], ['白色のランプ 2 が光らない']]]": Fraction(1, 10),
        "[[['赤'], ['紫']], [['白色のランプ 1 が光らない'], ['白色のランプ 2 が光る']]]": Fraction(2, 10),
        "[[['赤'], ['紫']], [['白色のランプ 1 が光らない'], ['白色のランプ 2 が光らない']]]": Fraction(3, 10),

        "[[['緑'], ['桃']], [['白色のランプ 1 が光る'], ['白色のランプ 2 が光る']]]": Fraction(3, 10),
        "[[['緑'], ['桃']], [['白色のランプ 1 が光る'], ['白色のランプ 2 が光らない']]]": Fraction(4, 10),
        "[[['緑'], ['桃']], [['白色のランプ 1 が光らない'], ['白色のランプ 2 が光る']]]": Fraction(1, 10),
        "[[['緑'], ['桃']], [['白色のランプ 1 が光らない'], ['白色のランプ 2 が光らない']]]": Fraction(2, 10),

        "[[['緑'], ['紫']], [['白色のランプ 1 が光る'], ['白色のランプ 2 が光る']]]": Fraction(2, 10),
        "[[['緑'], ['紫']], [['白色のランプ 1 が光る'], ['白色のランプ 2 が光らない']]]": Fraction(3, 10),
        "[[['緑'], ['紫']], [['白色のランプ 1 が光らない'], ['白色のランプ 2 が光る']]]": Fraction(4, 10),
        "[[['緑'], ['紫']], [['白色のランプ 1 が光らない'], ['白色のランプ 2 が光らない']]]": Fraction(1, 10),

        "[[['青'], ['桃']], [['白色のランプ 1 が光る'], ['白色のランプ 2 が光る']]]": Fraction(1, 10),
        "[[['青'], ['桃']], [['白色のランプ 1 が光る'], ['白色のランプ 2 が光らない']]]": Fraction(1, 10),
        "[[['青'], ['桃']], [['白色のランプ 1 が光らない'], ['白色のランプ 2 が光る']]]": Fraction(2, 10),
        "[[['青'], ['桃']], [['白色のランプ 1 が光らない'], ['白色のランプ 2 が光らない']]]": Fraction(6, 10),

        "[[['青'], ['紫']], [['白色のランプ 1 が光る'], ['白色のランプ 2 が光る']]]": Fraction(2, 10),
        "[[['青'], ['紫']], [['白色のランプ 1 が光る'], ['白色のランプ 2 が光らない']]]": Fraction(6, 10),
        "[[['青'], ['紫']], [['白色のランプ 1 が光らない'], ['白色のランプ 2 が光る']]]": Fraction(1, 10),
        "[[['青'], ['紫']], [['白色のランプ 1 が光らない'], ['白色のランプ 2 が光らない']]]": Fraction(1, 10),
    }
}


def main():
    # メソッド composition で表1 tensor_a と表2 tensor_b の結合演算を実施し、
    # メソッド print_tensor で標準出力します。
    markov_tensor.print_tensor(markov_tensor.composition(tensor_a, tensor_b))

    # メソッド composition で表1 tensor_c と表2 tensor_d の結合演算を実施し、
    # メソッド print_tensor で標準出力します。
    markov_tensor.print_tensor(markov_tensor.composition(tensor_c, tensor_d))

if __name__ == "__main__":
    main()
