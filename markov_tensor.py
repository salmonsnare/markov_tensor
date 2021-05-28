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

テンソル計算: 
- 結合演算: メソッド composition
- 恒等射: メソッド identity
- 部分結合: メソッド partial composition
- 同時化: メソッド jointification
- 条件化: メソッド conditionalization
- テンソル積: メソッド tensor_product
- 第一周辺化: メソッド first_marginalization
- 第二周辺化: メソッド second_marginalization

テンソルを構成
- 単位テンソル: メソッド unit_tensor
- マルコフ・テンソル Δ: メソッド delta
- マルコフ・テンソル ！: メソッド exclamation
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


def construct_label_index_dict(tensor_x):
    """
    文字列のラベルをもつようなプロファイルをもつテンソルから、文字列とインデックスを対応付ける。
    @param tensor_x テンソル
    @return domain_label_index 域について文字列のラベルとインデックスの辞書
    @return codomain_label_index 余域について文字列のラベルとインデックスの辞書
    """
    domain_label_index = {}
    codomain_label_index = {}

    domain_profile = tensor_x["profile"][DOMAIN_PROFILE]
    domain_index = 1
    for item in domain_profile[0]:
        domain_label_index[item] = domain_index
        domain_index += 1

    codomain_profile = tensor_x["profile"][CODOMAIN_PROFILE]
    codomain_index = 1
    for item in codomain_profile[0]:
        codomain_label_index[item] = codomain_index
        codomain_index += 1

    return domain_label_index, codomain_label_index


def convert_label2index(tensor_x):
    """
    文字列のラベルをもつようなプロファイルをもつテンソルから、
    文字列のラベルをインデックスに変更したテンソルを構成
    @param tensor_x テンソル
    @return tensor_result 文字列のラベルをインデックスに変更したテンソル
    @return domain_label_index 域について文字列のラベルとインデックスの辞書
    @return codomain_label_index 余域について文字列のラベルとインデックスの辞書
    [変換元]
    tensor_kagee = {
        "profile": [['A', 'B'], ['H', 'M', 'L']], 
        "strands": {
            "[['A'], ['H']]": Fraction(2, 10), 
            "[['A'], ['M']]": Fraction(6, 10), 
            "[['A'], ['L']]": Fraction(2, 10), 
            "[['B'], ['H']]": Fraction(1, 10), 
            "[['B'], ['M']]": Fraction(5, 10), 
            "[['B'], ['L']]": Fraction(4, 10)
        }
    }
    [変換先]
    tensor_kagee = {
        "profile": [[2], [3]], 
        "strands": {
            "[[1], [1]]": Fraction(2, 10), 
            "[[1], [2]]": Fraction(6, 10), 
            "[[1], [3]]": Fraction(2, 10), 
            "[[2], [1]]": Fraction(1, 10), 
            "[[2], [2]]": Fraction(5, 10), 
            "[[2], [3]]": Fraction(4, 10)
        }
    }
    """

    tensor_result = {}
    strands_result = {}
    domain_label_index, codomain_label_index = construct_label_index_dict(tensor_x)
    domain_profile = tensor_x["profile"][DOMAIN_PROFILE]
    codomain_profile = tensor_x["profile"][CODOMAIN_PROFILE]
    tensor_result["profile"] = [
        [len(domain_profile)], [len(codomain_profile)]
    ]

    for strand in tensor_x["strands"].keys():
        strand_list = eval(strand)
        converted_strand = str([
            [ domain_label_index[item] for item in strand_list[DOMAIN_LATTICE_POINT] ], 
            [ codomain_label_index[item] for item in strand_list[CODOMAIN_LATTICE_POINT] ], 
        ])
        strands_result[converted_strand] = tensor_x["strands"][strand]

    tensor_result["strands"] = strands_result

    return tensor_result, domain_label_index, codomain_label_index


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


def eq(list_x, list_y):
    return 1 if list_x == list_y else 0


def create_n_bar(n):
    return [index + 1 for index in range(n)]


def create_indexies(base_list):
    return [list(item) for item in list(itertools.product(*base_list))] # *base_list で引数としてリストを unpack して渡す。
      

def identity(tensor):
    """
    恒等射
    @param tensor テンソル
    """
    return tensor


def composition_process(tensor_x, tensor_y, strand_x, strand_y, strands_result, tensor_result):
    """
    結合演算のためのストランド間の計算
    @param tensor_x テンソル
    @param tensor_y テンソル
    @param strand_x テンソル tensor_x のストランド
    @param strand_y テンソル tensor_y のストランド
    @param strands_result 結果のストランド
    @param tensor_result 結果のテンソル
    """
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
    @param tensor_x テンソル
    @param tensor_y テンソル
    @param strand_x テンソル tensor_x のストランド
    @param strand_y テンソル tensor_y のストランド
    @param strands_result 結果のストランド
    @param tensor_result 結果のテンソル
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


def unit_tensor(list_x):
    """
    リストから単位テンソルを作成
    @param list_x リスト
    """
    tensor_result = {}
    tensor_result["profile"] = [list_x, list_x]
    tensor_result["strands"] = {}

    is_number = True
    for item in list_x:
        is_number = is_number and type(item) == int

    base_list = list_x
    if is_number:
        base_list = [create_n_bar(item) for item in list_x]

    for item in itertools.product(create_indexies(base_list), create_indexies(base_list)):
        if item[DOMAIN_LATTICE_POINT] == item[CODOMAIN_LATTICE_POINT]:
            tensor_result["strands"][str(list(item))] = 1

    return tensor_result



def delta(list_x):
    """
    リストが与えられたとき、マルコフ・テンソル Δ を構成
    @param list_x リスト
    """
    tensor_result = {}
    strands_result = {}

    domain = list_x
    codomain = []
    codomain.extend(list_x)
    codomain.extend(list_x)

    tensor_result["profile"] = [domain, codomain]
    tensor_result["strands"] = strands_result

    is_number = True
    for item in list_x:
        is_number = is_number and type(item) == int

    base_list_a = domain
    base_list_a_a = codomain
    if is_number:
        base_list_a = [create_n_bar(item) for item in domain]
        base_list_a_a = [create_n_bar(item) for item in codomain]
    

    for item in itertools.product(create_indexies(base_list_a), create_indexies(base_list_a_a)):
        x = item[DOMAIN_LATTICE_POINT]
        codomain_lattice_point = item[CODOMAIN_LATTICE_POINT]
        concat_index = int(len(codomain_lattice_point) / 2)
        x_ = codomain_lattice_point[0:concat_index]
        x__ = codomain_lattice_point[concat_index:len(codomain_lattice_point)]

        if DEBUG:
            print("x: {0}".format(x))
            print("x_: {0}".format(x_))
            print("x__: {0}".format(x__))
            print("eq(x_, x): {0}".format(eq(x_, x)))
            print("eq(x__, x): {0}".format(eq(x__, x)))

        tensor_result["strands"][str(item)] = eq(x_, x) * eq(x__, x)

    return tensor_result


def exclamation(list_x):
    """
    リストが与えられたとき、マルコフ・テンソル ! を構成
    @param list_x リスト
    """
    tensor_result = {}
    strands_result = {}
    tensor_result["profile"] = [list_x, []]
    tensor_result["strands"] = strands_result

    is_number = True
    for item in list_x:
        is_number = is_number and type(item) == int

    base_list = list_x
    if is_number:
        base_list = [create_n_bar(item) for item in list_x]

    for item in itertools.product(create_indexies(base_list), [[]]):
        tensor_result["strands"][str(list(item))] = 1

    return tensor_result


def jointification_process(tensor_x, tensor_y, strand_x, strand_y, strands_result, tensor_result):
    """
    同時化を算出するためのストランド間の計算
    @param tensor_x テンソル
    @param tensor_y テンソル
    @param strand_x テンソル tensor_x のストランド
    @param strand_y テンソル tensor_y のストランド
    @param strands_result 結果のストランド
    @param tensor_result 結果のテンソル
    """

    strand_from_x, strand_to_x = get_lattice_points(strand_x)
    strand_from_y, strand_to_y = get_lattice_points(strand_y)

    strand_from = []
    strand_to = []
    strand_to.extend(strand_from_y)
    strand_to.extend(strand_to_y)

    if strand_to_x == strand_from_y:  # tensor_x のあるストランドの終点と、tensor_y のあるストランドの始点が一致した場合
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


def jointification(tensor_x, tensor_y):
    """
    同時化を算出
    @param tensor_x テンソル [] -> a
    @param tensor_y テンソル a -> b
    @return tensor_result テンソル [] -> a#b
    """
    tensor_result = {}
    strands_result = {}
    if check_composable(tensor_x, tensor_y):
        tensor_result["profile"] = [
            tensor_x["profile"][DOMAIN_PROFILE], 
            tensor_y["profile"][CODOMAIN_PROFILE]
        ]

    for strand_x in list(tensor_x["strands"].keys()):
        for strand_y in list(tensor_y["strands"].keys()):
            tensor_result, strands_result = jointification_process(tensor_x, tensor_y, strand_x, strand_y, strands_result, tensor_result)
    tensor_result["strands"] = strands_result

    return tensor_result


def conditionalization(tensor_x, concat_start_index):
    """
    条件化を算出
    @param tensor_x テンソル [] -> a&b
    @param concat_start_index F の余域 の a と b の区切りとして、b の開始に関する index
    @return tensor_result テンソル a -> b 
    """

    tensor_result = {}
    strands_result = {}
    total = {}

    codomain_profile = tensor_x["profile"][CODOMAIN_PROFILE]
    tensor_result["profile"] = [
        codomain_profile[0:concat_start_index - 1], 
        codomain_profile[concat_start_index - 1:len(codomain_profile)]
    ]

    for strand in list(tensor_x["strands"].keys()):
        _, strand_to = get_lattice_points(strand)
        total_strand_from = str([strand_to[0:concat_start_index - 1]])
        if total_strand_from in total.keys(): # もし既にキー strand_result に値が設定されていれば加算
            total[total_strand_from] += tensor_x["strands"][strand]
        else:
            total[total_strand_from] = tensor_x["strands"][strand]

    for strand in list(tensor_x["strands"].keys()):
        _, strand_to = get_lattice_points(strand)
        total_strand_from = str([strand_to[0:concat_start_index - 1]])
        strand_lattice_points = str([strand_to[0:concat_start_index - 1], strand_to[concat_start_index - 1:len(codomain_profile)]])
        strands_result[strand_lattice_points] = tensor_x["strands"][strand] / total[total_strand_from]
    tensor_result["strands"] = strands_result

    return tensor_result


def first_marginalization(tensor, concat_start_index):
    """
    部分結合を算出
    @param tensor テンソル F: [] -> a&b
    @param concat_start_index F の余域 の a と b の区切りとして、b の開始に関する index
    @return tensor_result テンソル [] -> a
    """
    if tensor["profile"][DOMAIN_PROFILE] == []:
        codomain_profile_tensor = tensor["profile"][CODOMAIN_PROFILE]
        domain_unit_tensor_a = codomain_profile_tensor[0:concat_start_index - 1]
        domain_tensor_b = codomain_profile_tensor[concat_start_index - 1:len(codomain_profile_tensor)]
        unit_tensor_a = unit_tensor(domain_unit_tensor_a)

        if DEBUG:
            print("codomain_profile_tensor: {0}".format(codomain_profile_tensor))
            print("domain_unit_tensor_a: {0}".format(domain_unit_tensor_a))
            print("domain_tensor_b: {0}".format(domain_tensor_b))
            print("unit_tensor_a: {0}".format(unit_tensor_a))

        return composition(tensor, tensor_product(unit_tensor_a, exclamation(domain_tensor_b)))
    else:
        print("cannot compute first marginalization")


def second_marginalization(tensor, concat_start_index):
    """
    部分結合を算出
    @param tensor テンソル F: [] -> a&b
    @param concat_start_index F の余域 の a と b の区切りとして、b の開始に関する index
    @return tensor_result テンソル [] -> b
    """
    if tensor["profile"][DOMAIN_PROFILE] == []:
        codomain_profile_tensor = tensor["profile"][CODOMAIN_PROFILE]
        domain_tensor_a = codomain_profile_tensor[0:concat_start_index - 1]
        domain_unit_tensor_b = codomain_profile_tensor[concat_start_index - 1:len(codomain_profile_tensor)]
        unit_tensor_b = unit_tensor(domain_unit_tensor_b)

        if DEBUG:
            print("codomain_profile_tensor: {0}".format(codomain_profile_tensor))
            print("domain_tensor_a: {0}".format(domain_tensor_a))
            print("domain_unit_tensor_b: {0}".format(domain_unit_tensor_b))
            print("unit_tensor_b: {0}".format(unit_tensor_b))

        return composition(tensor, tensor_product(exclamation(domain_tensor_a), unit_tensor_b))
    else:
        print("cannot compute second marginalization")



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

    tensor_g = {
        "profile": [[], [2, 2]], 
        "strands": {
            "[[], [1, 1]]": Fraction(1, 10), 
            "[[], [1, 2]]": Fraction(2, 10), 
            "[[], [2, 1]]": Fraction(3, 10), 
            "[[], [2, 2]]": Fraction(4, 10)
        }
    }

    tensor_label1 = {
        "profile": [[['A', 'B']], [['H', 'M', 'L']]], 
        "strands": {
            "[['A'], ['H']]": Fraction(2, 10), 
            "[['A'], ['M']]": Fraction(6, 10), 
            "[['A'], ['L']]": Fraction(2, 10), 
            "[['B'], ['H']]": Fraction(1, 10), 
            "[['B'], ['M']]": Fraction(5, 10), 
            "[['B'], ['L']]": Fraction(4, 10)
        }
    }

    tensor_label2 = {
        "profile": [[['H', 'M', 'L']], [['a', 'b']]], 
        "strands": {
            "[['H'], ['a']]": Fraction(1, 10), 
            "[['H'], ['b']]": Fraction(9, 10), 
            "[['M'], ['a']]": Fraction(2, 10), 
            "[['M'], ['b']]": Fraction(8, 10), 
            "[['L'], ['a']]": Fraction(3, 10),
            "[['L'], ['b']]": Fraction(7, 10), 
        }
    }


    # テンソル計算
    for tensor_result in [
        composition(tensor_a, tensor_b), 
        composition(tensor_label1, tensor_label2), 
        identity(tensor_a),  
        composition(tensor_a, unit_tensor(tensor_a["profile"][CODOMAIN_PROFILE])), 
        composition(tensor_label1, unit_tensor(tensor_label1["profile"][CODOMAIN_PROFILE])), 
        partial_composition(tensor_a, tensor_c, 2), 
        composition(tensor_domain_empty_list, tensor_c), 
        composition(composition(composition(tensor_c, tensor_d), tensor_d), tensor_d), 
        tensor_product(tensor_label1, tensor_label2), 
        tensor_product(tensor_c, tensor_d), 
        tensor_product(tensor_domain_empty_list, tensor_d),
        delta([2, 2]),
        delta([['a', 'b']]), 
        exclamation([2, 2, 3]), 
        exclamation([['a', 'b', 'c']]), 
        unit_tensor([2, 2, 3]), 
        unit_tensor([['a', 'b', 'c']]), 
        jointification(tensor_domain_empty_list, tensor_c), 
        first_marginalization(tensor_g, 2), 
        second_marginalization(tensor_g, 2), 
        conditionalization(tensor_g, 2)
    ]:
        is_markov(tensor_result)    # マルコフ性のチェック
        print_tensor(tensor_result) # テンソルを標準出力

    tensor_result, domain_label_index, codomain_label_index = convert_label2index(tensor_label1)
    print(tensor_result, domain_label_index, codomain_label_index)
    

if __name__ == "__main__":
    main()