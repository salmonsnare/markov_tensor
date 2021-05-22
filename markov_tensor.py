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

"""

import numpy as np
import pandas as pd
import datetime

DEBUG = True

def what_is_function():
  print("Hello, world!") # コンソールに文字列表示 str -> 1 (副作用あり)
  datetime.datetime.now() # now に隠れた引数 tz=None がある。 1 = {None},  1 -> datetime
  raise Exception("exception") # 例外を投げる。 String -> ∅ (出力が存在しない。)


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
  tensor.pop("profile")
  total = {}
  for strand in tensor.keys():
      strand_from, _ = get_lattice_points(strand)
      strand_from_str = str(strand_from)
      if strand_from_str in total:
        total[strand_from_str] += tensor[strand]
      else:
        total[strand_from_str] = tensor[strand]
  ret = True
  print(total)
  for strand_from_str in total.keys():
    ret = ret and (total[strand_from_str] == 1.0)
      
  return ret


  print("sum(tensor.values()): {0}".format(sum(tensor.values())))
  return True if sum(tensor.values()) == 1.0 else False


def composition(tensor_x, tensor_y):
    """
    @param tensor_x テンソル
    @param tensor_y テンソル
    """

    tensor_result = {}
    if check_composable(tensor_x, tensor_y):
        tensor_result["profile"] = [tensor_x["profile"], tensor_y["profile"]]
        tensor_x.pop("profile")
        tensor_y.pop("profile")
        for strand_x in tensor_x.keys():
            for strand_y in tensor_y.keys():
                strand_from_x, strand_to_x = get_lattice_points(strand_x) 
                strand_from_y, strand_to_y = get_lattice_points(strand_y) 
                # 結合演算の結果のストランドの重みを算出
                if strand_to_x == strand_from_y: # tensor_x のあるストランドの終点と、tensor_y のあるストランドの始点が一致したばあい
                    strand_result = str([strand_from_x, strand_to_y]) # 結合演算の結果のストランドの始点と終点の設定
                    if strand_result in tensor_result.keys(): 
                        if DEBUG:
                            print("strand_to_x: {0}".format(strand_to_x))
                            print("strand_from_y: {0}".format(strand_from_y))
                            print("tensor_x[strand_x] * tensor_y[strand_y]: {0}".format(tensor_x[strand_x] * tensor_y[strand_y]))
                        tensor_result[strand_result] += tensor_x[strand_x] * tensor_y[strand_y]
                    else:
                        tensor_result[strand_result] = tensor_x[strand_x] * tensor_y[strand_y]
    
    return tensor_result


def main():
  tensor_x = {
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

  tensor_y = {
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

#   tensor_x = {
#     "profile": [[2], [2]],  
#     "[[1], [1]]": 0.3, 
#     "[[1], [2]]": 0.7, 
#     "[[2], [1]]": 0.5, 
#     "[[2], [2]]": 0.5, 
#   }

#   tensor_y = {
#     "profile": [[2], [2]],  
#     "[[1], [1]]": 0.5, 
#     "[[1], [2]]": 0.5, 
#     "[[2], [1]]": 0.5, 
#     "[[2], [2]]": 0.5, 
#   }

  tensor_result = composition(tensor_x, tensor_y)
  if is_markov(tensor_result):
    print("this tensor is markov")

  for key in tensor_result.keys():
      print(key, tensor_result[key])

if __name__ == "__main__":
  main()