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
import time

import gc

from gpflow.ci_utils import reduce_in_tests
from tqdm import tqdm
from gpflow.utilities import print_summary

from acquisitionFunction import acquisition_function
from black_box_f import black_box_f, ed


def dataCon(file1_path):

    data1 = pd.read_excel(file1_path, header=0, index_col=0).to_numpy()
    data_all = pd.read_excel("../data/test4.xlsx", header=0, index_col=0)
    list_name = data_all.columns.tolist()

    res = np.concatenate((data_all.to_numpy(), data1), axis=0)

    save_data = pd.DataFrame(res)
    # list_name[-1] = "评价值"
    save_data.columns = list_name

    save_data.to_excel("../data/test4.xlsx")
    print(save_data)


if __name__ == "__main__":
    f_p = sys.argv[1]
    # f_p =  "D:/bysjcs/text2.xlsx"
    dataCon(f_p)


