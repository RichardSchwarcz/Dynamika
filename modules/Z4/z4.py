import numpy as np
import matplotlib.patches as mpatches


def matica_hmotnosti(m: int) -> np.ndarray:
    return np.diag([m, m, m, m])


def H_vector(H: float) -> np.ndarray:
    H_vect = np.array([H, 3*H/4, 2*H/4, H/4, 0])
    return H_vect


def plotSchema(delta: np.ndarray, H_vector_: np.ndarray, hmoty: int, ax, index: int) -> None:
    i = index
    delta = np.insert(delta, 4, 0, axis=1)
    X = delta[i]
    Y = H_vector_

    ax.plot(X, Y, 'o-', color='gray')
    # plt.axis('off')
    # deformated circle because of difference in scaling of x axis
    el = mpatches.Circle((X[i], Y[i]), radius=2, alpha=0.5)
    ax.add_artist(el)

    ax.margins(0.5, 0.2)
    ax.title.set_text(f"{hmoty-i+1}. bod")

    for xy in zip(X, Y):
        ax.annotate('(%s, %s)' % xy, xy=xy, textcoords='data')


def delta_inv(delta):
    return np.linalg.inv(delta)


def frekvencie(delta_inv, mm):
    eigvals = np.linalg.eig(delta_inv)[0]
    reoder = [eigvals[2], eigvals[3], eigvals[1], eigvals[0]]
    L = np.diag(reoder)

    omega = np.nan_to_num(np.sqrt(L/mm))
    f = np.diag(np.sqrt(L/(mm*10**-3)))/(2*np.pi)

    print(
        f'frekvencia 1. tvaru: {f[0]:.3f} Hz \n frekvencia 2. tvaru: {f[1]:.3f} Hz \n frekvencia 3. tvaru: {f[2]:.3f} Hz')
    return f, omega


def periody(frekvencie):
    T = 1/frekvencie
    T = np.delete(T, -1)
    print(
        f'perioda 1. tvaru: {T[0]:.3f} s \n perioda 2. tvaru: {T[1]:.3f} s \n perioda 3. tvaru: {T[2]:.3f} s')
    return T


def vlastny_tvar(hmoty, tvary, mm, omega, delta_inv, iteracia):
    i = iteracia

    V0k = np.zeros((hmoty, tvary))

    # diag matrix of hmoty * omega
    # p4 = np.eye(hmoty) * omega[i, i]
    p4 = np.eye(hmoty) * omega[i]
    # print(f'p4 \n {p4}')
    p5 = delta_inv - mm * p4**2
    # print(f'p5 \n {p5}')

    # drop first row and first column
    A = p5[1:hmoty, 1:hmoty]
    # get first column and drop first row
    B = p5[1:hmoty, 0:1]

    # solve linear equation
    # -1 lebo som prehodil posledny stlpec na druhu stranu rovnice
    S = np.linalg.solve(A, B)*-1
    S = np.insert(S, 0, 1)
    # print(f'S \n {S}')

    # insert S to V0k
    V0k[:, i] = S

    # dot product of V0k transposed, mm and V0k
    q0 = 1/np.sqrt(np.dot(np.dot(V0k.T, mm), V0k))[i, i]
    # print(f'q0 = {q0}')

    # insert q0 to V0
    V0 = q0*S*10**3
    print(f'{i+1}. vlastny tvar V0 = {V0}')

    return V0


def spektrum_parametre_2(podlozie):
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


def hmoty_total(M, hmoty):
    return M*hmoty


def Fb(hmoty_total, sd, lambda_):
    Fb = hmoty_total*lambda_*sd
    print(f"Fb = {Fb} kN")
    return Fb


def seizmicke_sily(V0, M, Fb_, hmoty):
    F = []
    for i in range(hmoty):
        V01 = V0[0].sum()
        V01 = V01 - V0[0][i]
        FF = Fb_*(V0[0][i]*M)/(V01*3*M)
        F.append(FF)
    print(f'F [kN] = {F}')
    return F


def moment_FxR(F, HV):
    M = HV * F
    print(f'Momenty [kNm]\n {M}')
    return M


def gama(V0, mm):
    m = np.array([np.diag(mm)])
    gama = np.dot(V0, m.T*10**-3)
    print(f'Sucinitel participacie gama \n {gama}')
    return gama


def zrychlenie_i(Sd, gama, V0, riadky=0, stlpce=0):
    i = riadky
    j = stlpce
    X = Sd[j]*gama[j, 0]*V0[j, i]
    return X


def sily_zrychlenia(zrychlenia, M):
    F = M*zrychlenia*10**-3
    print(f'Vysledne sily \n {F}')
    return F


def moment(Sd, gama, V0, H_vector, riadky=0, stlpce=0):
    i = riadky
    j = stlpce
    X = Sd[j]*gama[j, 0]*V0[j, i]*H_vector[j, 0]
    return X
