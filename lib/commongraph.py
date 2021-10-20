# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from pychartjs import BaseChart, ChartType, Color

'''
    refer url : https://matplotlib.org/  ,  https://wikidocs.net/92071, https://pypi.org/project/pyChart.JS/ (chart example)
'''


def draw_example():
    x = np.arange(1, 10)
    y = x * 5

    plt.plot(x, y, 'r')
    plt.show()


class TestGraph(BaseChart):
    o_type = ChartType.Bar

    class data:
        label = "Numbers"
        data = [12, 19, 3, 17, 10]
        backgroundColor = Color.Green


if __name__ == '__main__':
    draw_example()
