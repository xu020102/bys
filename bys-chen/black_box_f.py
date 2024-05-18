import numpy as np
import warnings
warnings.filterwarnings("ignore")
import numpy as np

from scipy.stats import norm


def myBlackBox(X, n_dimen=0):
    """_summary_

    Args:
        :param X (array): _description_
        :param n_dimen (int):
    Returns:
        _type_: _description_

    """

    if type([1, 2, 3]) == type(X):
        len_x = len(X)
        X = np.array([X])
        n_dimen += 1
        if n_dimen == 0:
            X = np.array([X])
    else:
        len_x = 2

    mean1 = [0.7, 0.8]
    cov1 = [0.1, 0.2]
    mean2 = [0.1 for _ in range(len_x)]
    cov2 = [0.08, 0.14]

    Z = norm(mean1, cov1).pdf(X) + norm(mean2, cov2).pdf(X) / 2
    Z = np.sum(Z, axis=1)
    Z = Z - np.random.randn(X.shape[0]) * 0.001

    return Z


def ed(m, n, lq):
    """_summary_

    Args:
        m (_type_): _description_
        n (_type_): _description_

    Returns:
        _type_: _description_
    """
    m = np.array(m)
    n = np.array(n)
    temp = []
    for i in range(len(lq)):
        temp.append(((m[i] - n[i]) ** 2) * lq[i])
    return np.sqrt(np.sum(temp))


def branin_hoo(x: np.ndarray) -> np.ndarray:
    """_summary_

    Args:
        x (np.ndarray): _description_

    Raises:
        Exception: _description_

    Returns:
        np.ndarray: _description_
    """
    a = 1
    b = 5.1 / (4 * np.pi ** 2)
    c = 5 / np.pi
    r = 6
    s = 10
    t = 1 / (8 * np.pi)

    if len(np.shape(x)) == 1 and len(x) == 2:
        x1, x2 = x[0] * 15 - 5, x[1] * 15
        term1 = a * (x2 - b * x1 ** 2 + c * x1 - r) ** 2
        term2 = s * (1 - t) * np.cos(x1)
        term3 = s
        scores = term1 + term2 + term3
        return scores + np.random.randn() * 0.01
    elif len(np.shape(x)) == 2:
        res = []
        for t_x in x:
            res.append(branin_hoo(t_x))
        return np.array(res)
    else:
        raise Exception("The shape of the x is wrong. It should be (X, 2)")


def egg(x: np.ndarray) -> np.ndarray:
    """_summary_

    Args:
        x (np.ndarray): _description_

    Raises:
        Exception: _description_

    Returns:
        np.ndarray: _description_
    """

    if len(np.shape(x)) == 1 and len(x) == 2:
        x1, x2 = x[0] * 1024 - 512, x[1] * 1024 - 512
        term1 = -(x2 + 47) * np.sin(np.sqrt(np.abs(x2 + x1 / 2 + 47)))
        term2 = -x1 * np.sin(np.sqrt(np.abs(x1 - (x2 + 47))))
        scores = term1 + term2
        return scores + np.random.randn() * 0.01
    elif len(np.shape(x)) == 2:
        res = []
        for t_x in x:
            res.append(egg(t_x))
        return np.array(res)
    else:
        raise Exception("The shape of the x is wrong. It should be (X, 2)")


def schewef(xx):
    if len(np.shape(xx)) == 1 and len(xx) == 2:
        d = len(xx)
        s = 0
        for xi in xx:
            xi = xi * 1000 - 500
            s += xi * np.sin(np.sqrt(np.abs(xi)))
        y = 418.9829 * d - s
        y = -y
        return y
    elif len(np.shape(xx)) == 2:
        res = []
        for t_x in xx:
            res.append(schwef(t_x))
        return np.array(res)
    else:
        raise Exception("The shape of the x is wrong. It should be (X, 2)")


def myBlackBox2(X):
    return np.sum(np.sin(6 * X + 1) + np.random.randn(*X.shape) * 0.03, axis=1)


def black_box_f(X, f_name):
    if f_name == 'egg':
        res = -egg(X)
    elif f_name == 'branin':
        res = -branin_hoo(X)
    elif f_name == 'schewef':
        res = schewef(X)
    elif f_name == 'self_black':
        res = myBlackBox(X)
    else:
        raise Exception("Not Find the function")
    return res
