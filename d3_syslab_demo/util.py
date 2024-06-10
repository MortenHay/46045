def clamp(a, x, b):
    """
    Restrict x to lie in the range [a, b]
    """
    return max(a, min(x, b))


def overshoot(y, r, T_1, T_2, positive_step=True):
    result, t_max = 0, 0
    if positive_step:
        result = (y - r).loc[T_1:T_2].max()
    else:
        result = (r - y).loc[T_1:T_2].max()

    return max(result, 0), t_max


def undershoot(y, r, T_os, T_2, positive_step=None):
    result, t_max = 0, 0
    if positive_step:
        result = -((r - y.loc[T_2]).loc[T_os:T_2].min())
    else:
        result = -((r - y).loc[T_os:T_2].min())

    return max(result, 0)


def settling_time(y, r, T_1, T_2, M):
    e = r.loc[T_1:T_2] - y.loc[T_1:T_2]
    for t in e.index:
        t_settling = t
        if e.loc[t:].abs().max() < M:
            break

    result = t_settling - T_1
    return result


def rmse(y, r, T_1, T_2):
    sq_e = r.loc[T_1:T_2] - y.loc[T_1:T_2]
    sq_e_sum = 0
    for x in sq_e:
        sq_e_sum += x**2

    rsme = (sq_e_sum / len(sq_e)) ** (1 / 2)
    result = rsme
    return result
