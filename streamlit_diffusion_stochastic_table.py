import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random
import markov_tensor
from fractions import Fraction

st.title('拡散確率テーブル')
st.sidebar.header("制御")
st.sidebar.markdown("スライダー")


def construct_default_data():
    tensor_m = {
        "profile": [[], [3, 2]],  
        "strands": {
            "[[], [1, 1]]": 1, 
            "[[], [1, 2]]": 0, 
            "[[], [2, 1]]": 0, 
            "[[], [2, 2]]": 0, 
            "[[], [3, 1]]": 0, 
            "[[], [3, 2]]": 0, 
        }
    }

    tensor_d = {
        "profile": [[3, 2], [3, 2]],  
        "strands": {
            "[[1, 1], [1, 1]]": 0.7, # Fraction(7, 10), 
            "[[1, 1], [1, 2]]": 0.1, # Fraction(1, 10), 
            "[[1, 1], [2, 1]]": 0.1, # Fraction(1, 10), 
            "[[1, 1], [2, 2]]": 0.1, # Fraction(1, 10), 
            "[[1, 1], [3, 1]]": 0, 
            "[[1, 1], [3, 2]]": 0, 

            "[[1, 2], [1, 1]]": 0, 
            "[[1, 2], [1, 2]]": 1, 
            "[[1, 2], [2, 1]]": 0, 
            "[[1, 2], [2, 2]]": 0, 
            "[[1, 2], [3, 1]]": 0, 
            "[[1, 2], [3, 2]]": 0, 

            "[[2, 1], [1, 1]]": 0.1, # Fraction(1, 10), 
            "[[2, 1], [1, 2]]": 0.1, # Fraction(1, 10), 
            "[[2, 1], [2, 1]]": 0.5, # Fraction(5, 10), 
            "[[2, 1], [2, 2]]": 0.2, # Fraction(2, 10), 
            "[[2, 1], [3, 1]]": 0.1, # Fraction(1, 10), 
            "[[2, 1], [3, 2]]": 0, 

            "[[2, 2], [1, 1]]": 0, 
            "[[2, 2], [1, 2]]": 0.1, # Fraction(1, 10), 
            "[[2, 2], [2, 1]]": 0, 
            "[[2, 2], [2, 2]]": 0.9, # Fraction(9, 10), 
            "[[2, 2], [3, 1]]": 0, 
            "[[2, 2], [3, 2]]": 0, 

            "[[3, 1], [1, 1]]": 0, 
            "[[3, 1], [1, 2]]": 0, 
            "[[3, 1], [2, 1]]": 0, 
            "[[3, 1], [2, 2]]": 1, 
            "[[3, 1], [3, 1]]": 0, 
            "[[3, 1], [3, 2]]": 0, 

            "[[3, 2], [1, 1]]": 0, 
            "[[3, 2], [1, 2]]": 0, 
            "[[3, 2], [2, 1]]": 0.2, # Fraction(2, 10), 
            "[[3, 2], [2, 2]]": 0.4, # Fraction(4, 10), 
            "[[3, 2], [3, 1]]": 0.4, # Fraction(4, 10), 
            "[[3, 2], [3, 2]]": 0
        }
    }
    return tensor_m, tensor_d


def construct_tensor(num): 
    tensor_m = {}
    strands = {}
    for item in markov_tensor.create_indexies([markov_tensor.create_n_bar(item) for item in [10, 10]]):
        strands[str([[], item])] = 1 if item == [1, 1] else 0
    tensor_m["profile"] = [[], [num, num]]
    tensor_m["strands"] = strands
    markov_tensor.print_tensor(tensor_m)

    tensor_d = {}
    strands = {}
    for item_i in markov_tensor.create_indexies([markov_tensor.create_n_bar(item) for item in [num, num]]):
        for item_j in markov_tensor.create_indexies([markov_tensor.create_n_bar(item) for item in [num, num]]):
            if item_i == item_j:
                strands[str([item_i, item_j])] = 0.8
            else:
                strands[str([item_i, item_j])] = 0

    for item_i in markov_tensor.create_indexies([markov_tensor.create_n_bar(item) for item in [num, num]]):
        for item_j in markov_tensor.create_indexies([markov_tensor.create_n_bar(item) for item in [num, num]]):
            if (item_i[0] + 1) % num ==  item_j[0] and (item_i[1] + 1) % num == item_j[1]:
                strands[str([item_i, item_j])] = 0.2
        
    tensor_d["profile"] = [[num, num], [num, num]]
    tensor_d["strands"] = strands
    markov_tensor.print_tensor(tensor_d)
    return tensor_m, tensor_d


def main():
    tensor_m, tensor_d = construct_default_data()
    tensor_result = tensor_m
    fig = go.Figure()
    step = st.sidebar.slider('ステップ数',  min_value=0, max_value=20, step=1, value=0)
    st.write("Step {0}".format(step))
    for item in range(step):
        tensor_result = markov_tensor.composition(tensor_result, tensor_d)
        markov_tensor.print_tensor(tensor_result)
    val=[
        [ 
            tensor_result["strands"][str([[], [index_i + 1, index_j + 1]])] for index_i in range(tensor_result["profile"][1][0]) 
        ] for index_j in range(tensor_result["profile"][1][1])
    ]
    fig.add_trace(
            go.Heatmap(
                z=val, 
                colorscale = "Blues", 
                colorbar=dict(
                    tick0=0,
                    dtick=1
                ) 
            )
    )
    st.write(fig)


if __name__ == "__main__":
    main()
