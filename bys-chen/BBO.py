import sys
import warnings

warnings.filterwarnings("ignore")

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import pandas as pd
import seaborn as sns
import gpflow as gpf
import math

import gc

from gpflow.ci_utils import reduce_in_tests
from tqdm import tqdm
from gpflow.utilities import print_summary

from acquisitionFunction import acquisition_function
from black_box_f import black_box_f, ed

from sklearn.manifold import MDS
from matplotlib import pyplot as plt
from datetime import date

def analyse(file_path, featrue_num, file_path_mds):
    test_path = "../result/" + file_path_mds + ".csv"
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

    drawMDS(X, Y ,file_path_mds)


def drawMDS(X, Y, file_path_mds, batch_size=20):

    mds3 = MDS(n_components=3, random_state=0)
    X_transform_L3 = mds3.fit_transform(X)

    mds2 = MDS(n_components=2, random_state=0)
    # Get the embeddings
    X_transform_L2 = mds2.fit_transform(X)

    X_all_len = X.shape[0]

    # marker = ['.'] * X_all_len

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

    plt.savefig("../result/" + file_path_mds + '.jpg')


def test(times=50, batch_size=10, epoch=1, dim_n=2, function_name="self_black"):
    """

    :param times: 迭代次数
    :param batch_size: 批次大小
    :param epoch: 测试轮次
    :param dim_n: 维度
    :param function_name: 仿真黑盒名称
    :return:
    最优观测点，最优观测值
    """
    np.random.seed()
    origin_x = np.random.random((epoch, dim_n))
    res_x = []
    res_y = []
    for x in origin_x:
        X1 = np.array(x).reshape(1, dim_n)
        Y1 = np.array(black_box_f(X1, function_name)).reshape(-1, 1)
        for timett in tqdm(range(times)):
            Batch_res = start(X1, Y1, timett=timett, flag=False)
            print(Batch_res)
            for b_x in Batch_res:
                temp_x = np.array([b_x])
                X1 = np.concatenate((X1, temp_x), axis=0)
                Y_ob = np.array(black_box_f(temp_x, function_name)).reshape(-1, 1)
                Y1 = np.concatenate((Y1, np.array(Y_ob)), axis=0)
        res_y.append(max(Y1))
        res_x.append(X1[np.argmax(Y1)])
    return res_x, res_y


def start(X, Y, batch_size=20, timett=1, flag=True):
    """

    :param X: 训练数据
    :param Y: 训练数据结果
    :param dim_n: 维度
    :param batch_size: 批次大小
    :param timett: 当前迭代次数
    :return:
    批次推荐点
    """
    dim_n = np.shape(X)[1]
    n_m = np.shape(X)[0]
    test_size = 100 if flag else 1000
    m = gpf.models.GPR(data=(X, Y), kernel=gpf.kernels.RBF(lengthscales=[0.5 + 0.2 * timett] * np.shape(X)[1]))
    maxiter = reduce_in_tests(5)
    gpf.optimizers.Scipy().minimize(
        m.training_loss,
        m.trainable_variables,
        options=dict(maxiter=maxiter),
        method="L-BFGS-B",
    )
    lq = m.kernel.lengthscales.numpy()
    test_x = np.random.rand(test_size, dim_n)
    mu, var = m.predict_f(test_x)
    std = np.sqrt(var)
    M = max(Y)
    AC_orign = acquisition_function({'ac': 'ucb', 'beta': 0.1 + 0.02 * n_m}, mu, std, 0, 0)
    Batch_s = []
    AC_value = []
    mu_set = []
    std_set = []
    L_set = []
    for ia in range(len(X)):
        for ja in range(ia):
            L_set.append(abs(Y[ia] - Y[ja]) / ed(X[ia], X[ja], 1 / lq))
    if L_set == [] or max(L_set) < 1e-7:
        L = 1e-7
    else:
        L = max(L_set)

    # for ind, xt in enumerate(test_x):
    #     min_num = 1e-6
    #     temp = abs(m.predict_f(np.array([xt + min_num]))[0] - m.predict_f(np.array([xt - min_num]))[0])
    #     ed_x = ed(xt + min_num, xt - min_num, 1 / lq)
    #     t_L = temp / ed_x
    #     if t_L < 1e-7:
    #         L.append(1)
    #     else:
    #         L.append(t_L)
    for _ in range(batch_size):
        if Batch_s == []:
            Batch_s.append(test_x[np.argmax(AC_orign)])
            mu_set.append(mu[np.argmax(AC_orign)])
            std_set.append(std[np.argmax(AC_orign)])
            AC_value.append(max(AC_orign))
        else:
            mu, var = m.predict_f(test_x)
            std = np.sqrt(var)
            AC_orign = acquisition_function({'ac': 'ucb', 'beta': 0.1 + 0.02 * n_m}, mu, std, 0, 0).numpy()
            for xj in Batch_s:
                for ind, xt in enumerate(test_x):
                    ed_x = ed(xj, xt, 1 / lq)
                    E_r = abs(M[0] - mu[ind]) / L
                    varphi = min(1, ed_x / (E_r + (std[ind] / L)))
                    AC_orign[ind] *= varphi
            Batch_s.append(test_x[np.argmax(AC_orign)])
            mu_set.append(mu[np.argmax(AC_orign)])
            std_set.append(std[np.argmax(AC_orign)])
            # AC_value.append(max(AC_orign_copy))
            AC_value.append(AC_orign[np.argmax(AC_orign)])

    if flag:
        return Batch_s, mu_set, std_set, AC_value
    else:
        return Batch_s


def main(file_path, res_save_path, featrue_num, batch_size=20):
    # 在这里处理读取的数据

    data = pd.read_excel(file_path, header=0, index_col=0)
    # # 获取列名
    # print(data.columns.tolist())
    lsit_name = data.columns.tolist()
    min_max_value_list = []
    for i in range(data.shape[1] - 1):
        data.iloc[:, i:i + 1] = data.iloc[:, i:i + 1].apply(lambda x: np.log(x + 0.001))
    # print(data)
    data = data.to_numpy()
    for i in range(featrue_num):
        max_value = max(data[:, i])
        min_value = min(data[:, i])

        min_max_value_list.append(min_value)
        min_max_value_list.append(max_value)
        for ii in range(0, data.shape[0]):
            data[ii, i] = (data[ii, i] - min_value) / (max_value - min_value)

    X = data[:, 0:featrue_num]
    Y = data[:, featrue_num:featrue_num+1].reshape(-1, 1)

    Batch_s, mu_set, std_set, AC_value = start(X, Y, batch_size=batch_size)
    # print("Recommend Point: ", Batch_s)

    temp = []
    for t in range(len(Batch_s)):
        for j in range(featrue_num):
            # print(data_value[t][j])
            # try:
            #     Batch_s[t][j] = round(math.pow(math.e, Batch_s[t][j] * \
            #                                    (min_max_value_list[j * 2 + 1] - min_max_value_list[j * 2]) +
            #                                    min_max_value_list[j * 2]) - 0.001, 2)
            # except OverflowError:
            #     Batch_s[t][j] = math.inf

            Batch_s[t][j] = round(np.exp(Batch_s[t][j] * \
                                           (min_max_value_list[j * 2 + 1] - min_max_value_list[j * 2]) +
                                           min_max_value_list[j * 2]) - 0.001, 2)

            # Batch_s[t][j] = round(np.power(math.e, Batch_s[t][j] * \
            #                                (min_max_value_list[j * 2 + 1] - min_max_value_list[j * 2]) +
            #                                min_max_value_list[j * 2]) - 0.001, 2)
            temp.append(Batch_s[t][j])
    # Batch_s = temp
    # print(Batch_s)
    res_x = np.array(Batch_s)
    res_value = np.array(AC_value)
    # res_mu = np.array(mu_set)
    # res_std = np.array(std_set)
    res = np.concatenate((res_x, res_value), axis=1)
    # res = np.concatenate((res, res_std), axis=1)
    # res = np.concatenate((res, res_value), axis=1)
    save_data = pd.DataFrame(res)
    lsit_name[-1] = "评价值"
    save_data.columns = lsit_name
    print(save_data)

    save_data.to_csv("../result/"+res_save_path+".csv")


if __name__ == '__main__':
    # res_x, res_y = test()
    # print("best point : ", res_x, "best value : ", res_y)

    # 直接训练数据：
    file_path ="../data/test4.xlsx"
    # file_path_res = sys.argv[1]  # 从命令行参数获取文件路径
    file_path_res = "abcde"
    # pd.DataFrame().to_csv(file_path_res+".csv")
    main(file_path=file_path, res_save_path=file_path_res, featrue_num=10, batch_size=20)
    analyse(file_path=file_path, featrue_num=10, file_path_mds=file_path_res)
    # data = pd.read_csv()
    # X = data[0:11]
    # Y = data[11]
    # Batch_s = start(X, Y)
    # print("Recommend Point: ", Batch_s)
    # save_data = pd.DataFrame(Batch_s)
    # save_data.to_csv(" ",index_label=,columns=)


