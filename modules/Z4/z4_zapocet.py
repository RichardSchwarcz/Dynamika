import numpy as np


def matica_hmotnosti(m: int) -> np.ndarray:
    diag = np.diag([m, m, m, m])
    vector = np.array([[m], [m], [m], [m]])
    return diag, vector


def H_vector(H: float) -> np.ndarray:
    H_vect = np.array([H/4, 2*H/4, 3*H/4, H])
    return H_vect


def vlastne_frekvencie(list_f: list) -> np.ndarray:
    f = np.array(list_f)
    return f


def uhlove_frekvencie(vlastne_frekvencie: np.ndarray) -> np.ndarray:
    omega = 2*np.pi*vlastne_frekvencie
    return omega


def vlastne_periody(frekvencie):
    T = 1/frekvencie
    return T


def spektrum_parametre(podlozie, typ):
    if typ == 1:
        if podlozie == "A":
            S = 1
            T_B = 0.15
            T_C = 0.4
            T_D = 2.0

        if podlozie == "B":
            S = 1.2
            T_B = 0.15
            T_C = 0.5
            T_D = 2.0

        if podlozie == "C":
            S = 1.15
            T_B = 0.2
            T_C = 0.6
            T_D = 2.0

        if podlozie == "D":
            S = 1.35
            T_B = 0.2
            T_C = 0.8
            T_D = 2.0

        if podlozie == "E":
            S = 1.4
            T_B = 0.15
            T_C = 0.5
            T_D = 2.0

    if typ == 2:
        if podlozie == "A":
            S = 1
            T_B = 0.05
            T_C = 0.25
            T_D = 1.2

        if podlozie == "B":
            S = 1.35
            T_B = 0.05
            T_C = 0.25
            T_D = 1.2

        if podlozie == "C":
            S = 1.5
            T_B = 0.1
            T_C = 0.25
            T_D = 1.2

        if podlozie == "D":
            S = 1.8
            T_B = 0.1
            T_C = 0.3
            T_D = 1.2

        if podlozie == "E":
            S = 1.6
            T_B = 0.05
            T_C = 0.25
            T_D = 1.2

    parametre_podlozia = {
        "S": S,
        "T_B": T_B,
        "T_C": T_C,
        "T_D": T_D,
    }

    return parametre_podlozia


def sd(parametre, T0, ag, q):
    # navrhove spektrum sd
    S = parametre["S"]
    T_B = parametre["T_B"]
    T_C = parametre["T_C"]
    T_D = parametre["T_D"]

    beta = 0.2  # narodna priloha smie stanovit hodnotu beta. Doporucena hodnota je 0.2

    if 0 <= T0 < T_B:
        sd = ag*S*(2/3+T0/T_B*(2.5/q-2/3))
    elif T_B <= T0 < T_C:
        sd = ag*S*(2.5/q)
    elif T_C <= T0 < T_D:
        sd = ag*S*2.5/q*(T_C/T0)
        if sd < ag*beta:
            sd = ag*beta
    elif T_D <= T0:
        sd = ag*S*2.5/q*(T_C*T_D/T0**2)
        if sd < ag*beta:
            sd = ag*beta
    return sd
