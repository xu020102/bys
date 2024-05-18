
import warnings
import os
import glob

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

from matplotlib import pyplot as plt
from scipy.stats import norm
from sklearn.manifold import MDS
from matplotlib import pyplot as plt
from datetime import date


def analyse(file_path, featrue_num, test_path="D:/bysjcs/game.csv"):
    data = pd.read_excel(file_path, header=0, index_col=0)
    # # 获取列名
    for i in range(data.shape[1] - 1):
        data.iloc[:, i:i + 1] = data.iloc[:, i:i + 1].apply(lambda x: np.log(x + 0.001))
    data = data.to_numpy()

    X = data[:, 0:featrue_num]
    Y = data[:, featrue_num:featrue_num + 1].reshape(-1, 1)


    "训练结果"
    data_test = pd.read_csv(test_path, header=0, index_col=0)
    for i in range(featrue_num):
        data_test.iloc[:, i:i + 1] = data_test.iloc[:, i:i + 1].apply(lambda x: np.log(x + 0.001))

    data_test = data_test.to_numpy()

    X = np.concatenate((X, data_test[:, 0:featrue_num]), axis=0)
    Y = np.concatenate((Y, data_test[:, featrue_num:featrue_num + 1].reshape(-1, 1)), axis=0)

    drawMDS(X, Y)


def drawMDS(X, Y, batch_size=20):

    mds3 = MDS(n_components=3, random_state=0)
    X_transform_L3 = mds3.fit_transform(X)

    mds2 = MDS(n_components=2, random_state=0)
    # Get the embeddings
    X_transform_L2 = mds2.fit_transform(X)

    X_all_len = X.shape[0]

    # marker = ['.'] * X_all_len 3

    ss = 300
    beis = 4

    fig = plt.figure(figsize=(15, 6), dpi=300)

    plt.scatter(X_transform_L2[:X_all_len-batch_size, 0], X_transform_L2[:X_all_len-batch_size, 1], s=ss, c='black',
                marker='.', label='Previous times')
    for t_i in range(X_all_len - batch_size):
        if Y[t_i] > 10:
            plt.scatter(X_transform_L2[t_i, 0], X_transform_L2[t_i, 1], s=ss * beis, c='black', marker='.')

    plt.scatter(X_transform_L2[X_all_len-batch_size:, 0], X_transform_L2[X_all_len-batch_size:, 1], s=ss, c='g',
                marker='1', label='This times', zorder=10)

    # plt.xlabel('x', fontsize=20)
    # plt.ylabel('y', fontsize=20)
    # plt.tick_params(axis='x', labelsize=18)
    # plt.tick_params(axis='y', labelsize=18)

    plt.legend(prop={'size': 26})

    day = date.today().strftime("%m-%d")

    plt.savefig(day + '_mds.jpg')

    plt.show()

if __name__ == "__main__":

    file_path = "D:/bysjcs/test3.xlsx"
    analyse(file_path=file_path, featrue_num=10)
