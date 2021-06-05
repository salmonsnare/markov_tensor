import plotly.graph_objects as go
import numpy as np
import random
import markov_tensor
from fractions import Fraction

fig = go.Figure()

"""
fig = go.Figure(data=go.Heatmap(
                    z=[[1, 20, 30],
                      [20, 1, 60],
                      [30, 60, 1]]))
"""

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

tensor_result = tensor_m
for step in range(20):
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

    tensor_result = markov_tensor.composition(tensor_result, tensor_d)
    markov_tensor.print_tensor(tensor_result)


# Create and add slider
steps = []
for i in range(len(fig.data)):
    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig.data)},
              {"title": "Slider switched to step: " + str(i)}],  # layout attribute
    )
    step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
    steps.append(step)

sliders = [dict(
    active=0,
    currentvalue={"prefix": "Frequency: "},
    pad={"t": 50},
    steps=steps
)]

fig.update_layout(
    sliders=sliders,
    width=800, 
    height=500
)

fig.show()

print(markov_tensor.create_indexies([markov_tensor.create_n_bar(item) for item in [100, 100]]))