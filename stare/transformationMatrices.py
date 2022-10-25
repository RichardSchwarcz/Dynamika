import numpy as np
import pandas as pd


def rotationMatrix(alfa):
    alfa_rad = np.deg2rad(alfa)
    return pd.DataFrame([[np.cos(alfa_rad),
                          np.sin(alfa_rad), 0],
                         [-np.sin(alfa_rad),
                          np.cos(alfa_rad), 0], [0, 0, 1]])


def transmissionMatrix(lx, ly):
    return pd.DataFrame([[-1, 0, 0], [0, -1, 0], [-ly, lx, -1]])
