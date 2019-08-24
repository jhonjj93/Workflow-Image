import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#from pandas.plotting import parallel_coordinates


def pl(list_plot, consolidated_data):
    # list_plot=[["LAI","SPAD","NDVI_mean"]]
    groups = consolidated_data.groupby(["ID"])
    fig, axes = plt.subplots(
        len(list_plot), len(
            list_plot[0]), figsize=(
            20, 10))
    # print(len(list_plot))
    for j in range(len(list_plot)):
        for h in range(len(list_plot[j])):
            group = groups[list_plot[j][h]]
            x = group.get_group(1).index.levels[0].to_list()
            for i in range(1, len(groups) - 1):
                y = group.get_group(i)
                if len(list_plot) > 1 and len(list_plot[0]) > 1:
                    axes[j][h].plot(x, y, label=i, marker='o')
                elif len(list_plot) == 1 and len(list_plot[0]) > 1:
                    axes[h].plot(x, y, label=i, marker='o')
                elif len(list_plot) == 1 and len(list_plot[0]) == 1:
                    axes.plot(x, y, label=i, marker='o')
            if len(list_plot) > 1 and len(list_plot[0]) > 1:
                axes[j][h].legend()
                axes[j][h].set_title(list_plot[j][h])
            elif len(list_plot) == 1 and len(list_plot[0]) > 1:
                axes[h].legend()
                axes[h].set_title(list_plot[j][h])
            elif len(list_plot) == 1 and len(list_plot[0]) == 1:
                axes.legend()
                axes.set_title(list_plot[j][h])
