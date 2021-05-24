"""
FXTens の Python による表現

プロファイルと、ストランドの始点と終点のインデックス (格子点) の対と
ストランドの重みを辞書として表現。
  tensor_x = {
    "profile": [[2], [2]],  
    "strands" {
        "[[1], [1]]": 0.3, 
        "[[1], [2]]": 0.7, 
        "[[2], [1]]": 0.5, 
        "[[2], [2]]": 0.5
    }
  }

対応したテンソル計算: 
- 結合演算: メソッド composition
- 恒等射: メソッド identity
- 部分結合: メソッド partial composition
- テンソル積: メソッド tensor_product

"""

import numpy as np
import pandas as pd
from fractions import Fraction
import itertools

DEBUG = True

DOMAIN_PROFILE = 0
CODOMAIN_PROFILE = 1
DOMAIN_LATTICE_POINT = 0
CODOMAIN_LATTICE_POINT = 1

def get_lattice_points(strand):
    """
    格子点の情報を取得
    @param ストランドの格子点の対
    @return ストランドの格子点の始点と終点
    """
    strand_list = eval(strand)
    strand_from = strand_list[0]
    strand_to = strand_list[1]
    return strand_from, strand_to


def check_composable(tensor_x, tensor_y):
    """
    2 個のテンソルが結合可能かチェック
    @param tensor_x テンソル
    @param tensor_y テンソル
    """
    return True if tensor_x["profile"][CODOMAIN_PROFILE] == tensor_y["profile"][DOMAIN_PROFILE] else False


def is_markov(tensor):
    """
    マルコフ性のチェック
    @param tensor
    """
    total = {}
    total_strands = {}
    total["strands"] = {}
    for strand in list(tensor["strands"].keys()):
        strand_from, _ = get_lattice_points(strand)
        strand_from_str = str(strand_from)
        if strand_from_str in total_strands.keys():
            total_strands[strand_from_str] += tensor["strands"][strand]
        else:
            total_strands[strand_from_str] = tensor["strands"][strand]
    total["strands"] = total_strands
    ret = True
    for strand_from_str in total["strands"].keys():
        ret = ret and (total["strands"][strand_from_str] == 1.0)
    if ret:
        print("this tensor is Markov")

    return ret


def create_n_bar(n):
    return [index + 1 for index in range(n)]


def create_indexies(base_list):
    return [list(item) for item in list(itertools.product(*base_list))] # *base_list で引数としてリストを unpack して渡す。


def unit_tensor(domain_or_codomain):
    """
    プロファイルの域、または余域から単位テンソルを作成
    @param domain_or_codomain 域、または余域
    """
    tensor_result = {}
    tensor_result["profile"] = [domain_or_codomain, domain_or_codomain]
    tensor_result["strands"] = {}

    base_list = [create_n_bar(domain_or_codomain_item) for domain_or_codomain_item in domain_or_codomain]

    for item in itertools.product(create_indexies(base_list), create_indexies(base_list)):
        if item[DOMAIN_LATTICE_POINT] == item[CODOMAIN_LATTICE_POINT]:
            tensor_result["strands"][str(list(item))] = 1

    return tensor_result
      

def identity(tensor):
    """
    恒等射
    @param tensor テンソル
    """
    return tensor


def composition_process(tensor_x, tensor_y, strand_x, strand_y, strands_result, tensor_result):
    strand_from_x, strand_to_x = get_lattice_points(strand_x)
    strand_from_y, strand_to_y = get_lattice_points(strand_y)
    # 結合演算の結果のストランドの重みを算出
    if strand_to_x == strand_from_y:  # tensor_x のあるストランドの終点と、tensor_y のあるストランドの始点が一致した場合
        # 結合演算の結果のストランドの始点と終点の設定
        # キー strand_result はストランドの始点と終点を表す格子点を表す。
        strand_lattice_points = str([strand_from_x, strand_to_y])
        mult = round(tensor_x["strands"][strand_x] * tensor_y["strands"][strand_y], 5)
        if DEBUG:
            print("---")
            print("  strand_from_x: {0}, strand_to_x: {1}, tensor_x[strand_x]: {2}".format(strand_from_x, strand_to_x, tensor_x["strands"][strand_x]))
            print("  strand_from_y: {0}, strand_to_y: {1}, tensor_y[strand_y]: {2}".format(strand_from_y, strand_to_y, tensor_y["strands"][strand_y]))
            print("tensor_x[strands][strand_x] * tensor_y[strands][strand_y]: {0}".format(mult))
        if strand_lattice_points in strands_result.keys(): # もし既にキー strand_result に値が設定されていれば加算
            strands_result[strand_lattice_points] += mult
        else: # もし既にキー strand_result に値が設定されていなければ設定
            strands_result[strand_lattice_points] = mult

    return tensor_result, strands_result


def composition(tensor_x, tensor_y):
    """
    結合を算出
    @param tensor_x テンソル
    @param tensor_y テンソル
    """

    tensor_result = {}
    strands_result = {}
    if check_composable(tensor_x, tensor_y):
        tensor_result["profile"] = [
            tensor_x["profile"][DOMAIN_PROFILE], 
            tensor_y["profile"][CODOMAIN_PROFILE]
        ]
        for strand_x in [item for item in list(tensor_x["strands"].keys())]:
            for strand_y in [item for item in list(tensor_y["strands"].keys())]:
                tensor_result, strands_result = composition_process(tensor_x, tensor_y, strand_x, strand_y, strands_result, tensor_result)
    else:
        print("cannot compose")
    tensor_result["strands"] = strands_result

    return tensor_result


def partial_composition(tensor_a_b_sharp_c, tensor_b_d, concat_start_index):
    """
    部分結合を算出
    @param tensor_x テンソル F: a -> b#c
    @param tensor_y テンソル G: b -> d
    @param concat_start_index F の余域 の b と c の区切りとして、c の開始に関する index
    @return tensor_result テンソル a -> d#c
    """

    codomain_profile_tensor_a_b_sharp_c = tensor_a_b_sharp_c["profile"][CODOMAIN_PROFILE]
    unit_tensor_c = unit_tensor(codomain_profile_tensor_a_b_sharp_c[concat_start_index - 1:len(codomain_profile_tensor_a_b_sharp_c)])
 
    if DEBUG:
        print("tensor_a_b_sharp_c")
        print_tensor(tensor_a_b_sharp_c)
        print("tensor_b_d")
        print_tensor(tensor_b_d)
        print("codomain_profile_tensor_a_b_sharp_c: {0}".format(codomain_profile_tensor_a_b_sharp_c))
        print("concat_index: {0}".format(concat_start_index))
        print(codomain_profile_tensor_a_b_sharp_c[concat_start_index - 1:len(codomain_profile_tensor_a_b_sharp_c)])
        print("unit_tensor_c")
        print_tensor(unit_tensor_c)

    return composition(tensor_a_b_sharp_c, tensor_product(tensor_b_d, unit_tensor_c))


def create_profile_tensor_product(tensor_x, tensor_y, tensor_result):
    # テンソル積のプロファイルを作成
    domain = []
    domain.extend(tensor_x["profile"][DOMAIN_PROFILE])
    domain.extend(tensor_y["profile"][DOMAIN_PROFILE])

    codomain = []
    codomain.extend(tensor_x["profile"][CODOMAIN_PROFILE])
    codomain.extend(tensor_y["profile"][CODOMAIN_PROFILE])
    tensor_result["profile"] = [
        domain,  # リストの連接によりプロファイルの域を作成 
        codomain # リストの連接によりプロファイルの余域を作成
    ]
    return tensor_result


def tensor_product_process(tensor_x, tensor_y, strand_x, strand_y, strands_result, tensor_result):
    """
    テンソル積を算出するためのストランド間の計算
    """
    strand_from_x, strand_to_x = get_lattice_points(strand_x)
    strand_from_y, strand_to_y = get_lattice_points(strand_y)

    strand_from = []
    strand_from.extend(strand_from_x)
    strand_from.extend(strand_from_y)

    strand_to = []
    strand_to.extend(strand_to_x)
    strand_to.extend(strand_to_y)

    strand_lattice_points = str([strand_from, strand_to])
    mult = round(tensor_x["strands"][strand_x] * tensor_y["strands"][strand_y], 5)
    if DEBUG:
        print("---")
        print("  strand_from_x: {0}, strand_to_x: {1}, tensor_x[strands][strand_x]: {2}".format(strand_from_x, strand_to_x, tensor_x["strands"][strand_x]))
        print("  strand_from_y: {0}, strand_to_y: {1}, tensor_y[strands][strand_y]: {2}".format(strand_from_y, strand_to_y, tensor_y["strands"][strand_y]))
        print("strand_from: {0}, strand_to: {1}".format(strand_from, strand_to))
        print("tensor_x[strands][strand_x] * tensor_y[stdands][strand_y]: {0}".format(mult))
    strands_result[strand_lattice_points] = mult

    return tensor_result, strands_result


def tensor_product(tensor_x, tensor_y):
    """
    テンソル積を算出
    @param tensor_x テンソル
    @param tensor_y テンソル
    """

    if DEBUG:
        print('tensor_x')
        print_tensor(tensor_x)
        print('tensor_y')
        print_tensor(tensor_y)

    tensor_result = {}
    strands_result = {}
    tensor_result = create_profile_tensor_product(tensor_x, tensor_y, tensor_result)

    for strand_x in [item for item in list(tensor_x["strands"].keys())]:
        for strand_y in [item for item in list(tensor_y["strands"].keys())]:
            tensor_result, strands_result = tensor_product_process(tensor_x, tensor_y, strand_x, strand_y, strands_result, tensor_result)
    tensor_result["strands"] = strands_result

    return tensor_result


def exclamation(domain):
    """
    域が与えられたとき、マルコフ・テンソル ! を構成
    @param domain 域
    """
    tensor_result = {}
    strands_result = {}
    tensor_result["profile"] = [domain, []]
    tensor_result["strands"] = strands_result
    base_list = [create_n_bar(domain_item) for domain_item in domain]
    for item in itertools.product(create_indexies(base_list), [[]]):
        tensor_result["strands"][str(list(item))] = 1

    return tensor_result
    

def print_tensor(tensor):
    """
    テンソルを標準出力に表示
    @param tensor テンソル
    """
    print("---")
    print("profile: ", tensor["profile"])
    strands = tensor["strands"]
    for key in strands.keys():
        print(key, strands[key])


def main():
    tensor_a = {
        "profile": [[2], [2, 2]],
        "strands": {
            "[[1], [1, 1]]": Fraction(1, 4),
            "[[1], [1, 2]]": Fraction(1, 4),
            "[[1], [2, 1]]": Fraction(1, 4),
            "[[1], [2, 2]]": Fraction(1, 4),
            "[[2], [1, 1]]": Fraction(3, 20),
            "[[2], [1, 2]]": Fraction(1, 4),
            "[[2], [2, 1]]": Fraction(7, 20),
            "[[2], [2, 2]]": Fraction(1, 4)
        }
    }

    tensor_b = {
        "profile": [[2, 2], [2, 2]],
        "strands": {
            "[[1, 1], [1, 1]]": Fraction(1, 4),
            "[[1, 1], [1, 2]]": Fraction(3, 20),
            "[[1, 1], [2, 1]]": Fraction(7, 20),
            "[[1, 1], [2, 2]]": Fraction(1, 4),
            "[[1, 2], [1, 1]]": Fraction(1, 4),
            "[[1, 2], [1, 2]]": Fraction(1, 4),
            "[[1, 2], [2, 1]]": Fraction(1, 4),
            "[[1, 2], [2, 2]]": Fraction(1, 4),
            "[[2, 1], [1, 1]]": Fraction(1, 4),
            "[[2, 1], [1, 2]]": Fraction(1, 4),
            "[[2, 1], [2, 1]]": Fraction(1, 4),
            "[[2, 1], [2, 2]]": Fraction(1, 4),
            "[[2, 2], [1, 1]]": Fraction(1, 4),
            "[[2, 2], [1, 2]]": Fraction(1, 4),
            "[[2, 2], [2, 1]]": Fraction(1, 4),
            "[[2, 2], [2, 2]]": Fraction(1, 4)
        }
    }

    tensor_domain_empty_list = {
        "profile": [[], [2]],
        "strands": {
            "[[], [1]]": Fraction(1, 10),
            "[[], [2]]": Fraction(9, 10)
        }
    }

    tensor_c = {
        "profile": [[2], [2]],
        "strands": {
        "[[1], [1]]": Fraction(3, 10),
        "[[1], [2]]": Fraction(7, 10),
        "[[2], [1]]": Fraction(1, 2),
        "[[2], [2]]": Fraction(1, 2)
        }
    }

    tensor_d = {
        "profile": [[2], [2]],
        "strands": {
            "[[1], [1]]": Fraction(2, 5),
            "[[1], [2]]": Fraction(3, 5),
            "[[2], [1]]": Fraction(1, 10),
            "[[2], [2]]": Fraction(9, 10)
        }
    }

    tensor_e = {
        "profile": [[1], [2, 2]], 
        "strands": {
            "[[1], [1, 1]]": Fraction(1, 10), 
            "[[1], [1, 2]]": Fraction(2, 10), 
            "[[1], [2, 1]]": Fraction(3, 10), 
            "[[1], [2, 2]]": Fraction(4, 10)
        }
    }

    tensor_f = {
        "profile": [[2], [2]], 
        "strands": {
            "[[1], [1]]": Fraction(1, 2), 
            "[[1], [2]]": Fraction(1, 2), 
            "[[2], [1]]": Fraction(1, 2), 
            "[[2], [2]]": Fraction(1, 2)
        }
    }

    # テンソル間の演算
    for tensor_result in [
        composition(tensor_a, tensor_b), 
        identity(tensor_a),  
        composition(tensor_a, unit_tensor(tensor_a["profile"][CODOMAIN_PROFILE])), 
        partial_composition(tensor_a, tensor_c, 2), 
        composition(tensor_domain_empty_list, tensor_c), 
        composition(composition(composition(tensor_c, tensor_d), tensor_d), tensor_d), 
        tensor_product(tensor_c, tensor_d), 
        tensor_product(tensor_domain_empty_list, tensor_d), 
        exclamation([2, 2, 3])
    ]:
        is_markov(tensor_result)    # マルコフ性のチェック
        print_tensor(tensor_result) # テンソルを標準出力


if __name__ == "__main__":
    main()