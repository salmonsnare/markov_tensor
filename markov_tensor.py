"""
FXTens の Python による表現

プロファイルと、ストランドの始点と終点のインデックス (格子点) の対と
ストランドの重みを辞書として表現。
  tensor_x = {
    "profile": [[2], [2]],  
    "[[1], [1]]": 0.3, 
    "[[1], [2]]": 0.7, 
    "[[2], [1]]": 0.5, 
    "[[2], [2]]": 0.5, 
  }

結合演算
テンソル積

"""

import numpy as np
import pandas as pd

DEBUG = True

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
    return True if tensor_x["profile"][1] == tensor_y["profile"][0] else False


def is_markov(tensor):
    """
    マルコフ性のチェック
    @param tensor
    """
    total = {}
    for strand in [item for item in list(tensor.keys()) if item != "profile"]:
        strand_from, _ = get_lattice_points(strand)
        strand_from_str = str(strand_from)
        if strand_from_str in total:
            total[strand_from_str] += tensor[strand]
        else:
            total[strand_from_str] = tensor[strand]
    ret = True
    for strand_from_str in total.keys():
        ret = ret and (total[strand_from_str] == 1.0)
    if ret:
        print("this tensor is Markov")

    return ret


def composition_process(tensor_x, tensor_y, strand_x, strand_y, tensor_result):
    strand_from_x, strand_to_x = get_lattice_points(strand_x)
    strand_from_y, strand_to_y = get_lattice_points(strand_y)
    # 結合演算の結果のストランドの重みを算出
    if strand_to_x == strand_from_y:  # tensor_x のあるストランドの終点と、tensor_y のあるストランドの始点が一致したばあい
        # 結合演算の結果のストランドの始点と終点の設定
        # キー strand_result はストランドの始点と終点を表す格子点を表す。
        strand_result = str([strand_from_x, strand_to_y])
        mult = round(tensor_x[strand_x] * tensor_y[strand_y], 5)
        if DEBUG:
            print("strand_to_x: {0}".format(strand_to_x))
            print("strand_from_y: {0}".format(strand_from_y))
            print("tensor_x[strand_x] * tensor_y[strand_y]: {0}".format(mult))
        if strand_result in tensor_result.keys(): # もし既にキー strand_result に値が設定されていれば加算
            tensor_result[strand_result] += mult
        else: # もし既にキー strand_result に値が設定されていなければ設定
            tensor_result[strand_result] = mult

    return tensor_result


def composition(tensor_x, tensor_y):
    """
    結合を算出
    @param tensor_x テンソル
    @param tensor_y テンソル
    """

    tensor_result = {}
    if check_composable(tensor_x, tensor_y):
        tensor_result["profile"] = [
            tensor_x["profile"][0], tensor_y["profile"][1]]
        for strand_x in [item for item in list(tensor_x.keys()) if item != "profile"]:
            for strand_y in [item for item in list(tensor_y.keys()) if item != "profile"]:
                tensor_result = composition_process(tensor_x, tensor_y, strand_x, strand_y, tensor_result)
    else:
        print("cannot compose")

    return tensor_result


# def partial_composition(tensor_x, tensor_y, concat_index):
#     """
#     部分結合を算出
#     @param tensor_x テンソル F: a -> b#c
#     @param tensor_y テンソル G: b -> d
#     @param concat_index F の余域 の b と c の区切りとして、c の開始に関する index
#     """

#     tensor_c = {}
#     codomain_profile_tensor_x = tensor_x["profile"][1]
#     domain_tensor_c = codomain_profile_tensor_x[concat_index:len(codomain_profile_tensor_x)]
#     codomain_tensor_c = domain_tensor_c
#     tensor_c["profile"] = [domain_tensor_c, codomain_tensor_c]


def create_profile_tensor_product(tensor_x, tensor_y, tensor_result):
    # テンソル積のプロファイルを作成
    domain = []
    domain.extend(tensor_x["profile"][0])
    domain.extend(tensor_y["profile"][0])

    codomain = []
    codomain.extend(tensor_x["profile"][1])
    codomain.extend(tensor_y["profile"][1])
    tensor_result["profile"] = [
        domain,  # リストの連接によりプロファイルの域を作成 
        codomain # リストの連接によりプロファイルの余域を作成
    ]
    return tensor_result


def tensor_product_process(tensor_x, tensor_y, strand_x, strand_y, tensor_result):
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

    strand_result = str([strand_from, strand_to])
    mult = round(tensor_x[strand_x] * tensor_y[strand_y], 5)
    if DEBUG:
        print("---")
        print("  strand_from_x: {0}, strand_to_x: {1}, tensor_x[strand_x]: {2}".format(strand_from_x, strand_to_x, tensor_x[strand_x]))
        print("  strand_from_y: {0}, strand_to_y: {1}, tensor_y[strand_y]: {2}".format(strand_from_y, strand_to_y, tensor_y[strand_y]))
        print("strand_from: {0}, strand_to: {1}".format(strand_from, strand_to))
        print("tensor_x[strand_x] * tensor_y[strand_y]: {0}".format(mult))
    tensor_result[strand_result] = mult

    return tensor_result


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
    tensor_result = create_profile_tensor_product(tensor_x, tensor_y, tensor_result)

    for strand_x in [item for item in list(tensor_x.keys()) if item != "profile"]:
        for strand_y in [item for item in list(tensor_y.keys()) if item != "profile"]:
            tensor_result = tensor_product_process(tensor_x, tensor_y, strand_x, strand_y, tensor_result)

    return tensor_result


def print_tensor(tensor):
    """
    テンソルを標準出力に表示
    @param tensor テンソル
    """
    print("---")
    for key in tensor.keys():
        print(key, tensor[key])


def main():
    tensor_a = {
        "profile": [[2], [2, 2]],
        "[[1], [1, 1]]": 0.25,
        "[[1], [1, 2]]": 0.25,
        "[[1], [2, 1]]": 0.25,
        "[[1], [2, 2]]": 0.25,
        "[[2], [1, 1]]": 0.15,
        "[[2], [1, 2]]": 0.25,
        "[[2], [2, 1]]": 0.35,
        "[[2], [2, 2]]": 0.25
    }

    tensor_b = {
        "profile": [[2, 2], [2, 2]],
        "[[1, 1], [1, 1]]": 0.25,
        "[[1, 1], [1, 2]]": 0.15,
        "[[1, 1], [2, 1]]": 0.35,
        "[[1, 1], [2, 2]]": 0.25,
        "[[1, 2], [1, 1]]": 0.25,
        "[[1, 2], [1, 2]]": 0.25,
        "[[1, 2], [2, 1]]": 0.25,
        "[[1, 2], [2, 2]]": 0.25,
        "[[2, 1], [1, 1]]": 0.25,
        "[[2, 1], [1, 2]]": 0.25,
        "[[2, 1], [2, 1]]": 0.25,
        "[[2, 1], [2, 2]]": 0.25,
        "[[2, 2], [1, 1]]": 0.25,
        "[[2, 2], [1, 2]]": 0.25,
        "[[2, 2], [2, 1]]": 0.25,
        "[[2, 2], [2, 2]]": 0.25
    }

    tensor_domain_empty_list = {
        "profile": [[], [2]],
        "[[], [1]]": 0.1,
        "[[], [2]]": 0.9,
    }

    tensor_c = {
        "profile": [[2], [2]],
        "[[1], [1]]": 0.3,
        "[[1], [2]]": 0.7,
        "[[2], [1]]": 0.5,
        "[[2], [2]]": 0.5,
    }

    tensor_d = {
        "profile": [[2], [2]],
        "[[1], [1]]": 0.4,
        "[[1], [2]]": 0.6,
        "[[2], [1]]": 0.1,
        "[[2], [2]]": 0.9,
    }

    tensor_e = {
        "profile": [[1], [2, 2]], 
        "[[1], [1, 1]]": 0.1, 
        "[[1], [1, 2]]": 0.2, 
        "[[1], [2, 1]]": 0.3, 
        "[[1], [2, 2]]": 0.4
    }

    tensor_f = {
        "profile": [[2], [2]], 
        "[[1], [1]]": 0.5, 
        "[[1], [2]]": 0.5, 
        "[[2], [1]]": 0.5, 
        "[[2], [2]]": 0.5
    }

    # テンソル間の演算
    for tensor_result in [
        composition(tensor_domain_empty_list, identity(tensor_c)), 
        composition(tensor_a, tensor_b), 
        composition(composition(composition(tensor_c, tensor_d), tensor_d), tensor_d), 
        tensor_product(tensor_c, tensor_d), 
        tensor_product(tensor_domain_empty_list, tensor_d)
    ]:
        is_markov(tensor_result)           # マルコフ性のチェック
        print_tensor(tensor_result) # テンソルを標準出力



if __name__ == "__main__":
    main()
