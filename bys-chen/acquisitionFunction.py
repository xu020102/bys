import warnings
import math

import numpy as np

from scipy.stats import norm


def acquisition_function(
        AC,
        mean,
        std,
        iter_t,
        train_y,
        n_samples=200,
        n_d=9
):
    """The acquisition function obtains the next optimal query by using the different strategies from the
    posterior mean and posterior variance obtained by the surrogate model.
    There are different startegies:
    a. ucb
    b. ei
    c. pi
    d. ucb_t
    e. ei_pi
    f. es
    g. pes

    Args:
        mean (List[float]): posterior mean
        std (List[float]): posterior variance
        iter_t (int): current number of iterations

    Returns:
        List[float]: the result of evaluation function
    """
    with warnings.catch_warnings():

        warnings.simplefilter("ignore")
        __delta = 0.8  # value of the delta

        if AC.get('ac') == "ucb":
            return mean + AC.get('beta') * std

        elif AC.get('ac') == "ei":
            a = (mean - max(train_y))
            z = a / (std + 1e-8)
            res = a * norm.cdf(z) + std * norm.pdf(z)
            res[std == 0] = 0
            return res

        elif AC.get('ac') == "pi":
            z = (mean - max(train_y)) / (std + 1e-8)
            res = norm.cdf(z)
            res[std == 0] = 0
            return res

        elif AC.get('ac') == "ucb_t":
            trade_off = 2 * math.log(float(iter_t ** 2 * 2 * math.pi ** 2) / (3 * __delta)) + \
                        2 * 3 * (math.log(float(n_d * iter_t ** 2)) + 1 / 2 *
                                 math.log(float(math.log(float(4 * n_d) / __delta))))
            # print(trade_off)
            return mean + trade_off * std

        elif AC.get('ac') == "ei_pi":
            a = (mean - max(train_y))
            z = a / std
            ei = a * norm.cdf(z) + std * norm.pdf(z)
            z = (mean - max(train_y)) / std
            pi = norm.cdf(z)
            return ei + AC.get('beta') * pi

        elif AC.get('ac') == 'es':
            U = (max(train_y) - mean) / std
            p = norm.pdf(U)
            c = norm.cdf(U)
            E = np.sum(p / (c + 1e-8), axis=0) / n_samples
            E[std == 0] = 0
            entropy = np.log(std + 1e-8) + E
            entropy[std == 0] = 0
            return entropy

        elif AC.get('ac') == 'pes':
            entropy = 0.5 * np.log(std + 1e-8)
            entropy[std == 0] = 0
            return entropy

    pass
