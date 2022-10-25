import pandas as pd
import numpy as np


class TransformationMatrix:
    def rotation(alfa):
        alfa_rad = np.deg2rad(alfa)
        return pd.DataFrame([[np.cos(alfa_rad),
                              np.sin(alfa_rad), 0],
                             [-np.sin(alfa_rad),
                              np.cos(alfa_rad), 0], [0, 0, 1]])

    def transmission(lx, ly):
        return pd.DataFrame([[-1, 0, 0], [0, -1, 0], [-ly, lx, -1]])


class BarStiffnessMatrix:
    def lss(BarProps, Bar):
        return pd.DataFrame([[BarProps.E * BarProps.A / Bar.len, 0, 0],
                             [0, 12 * BarProps.E * BarProps.I / Bar.len**3,
                              6 * BarProps.E * BarProps.I / Bar.len**2],
                             [0, 6 * BarProps.E * BarProps.I / Bar.len**2,
                              4 * BarProps.E * BarProps.I / Bar.len]])

    def gss(rotationMatrix, lssBarStiffnessMatrix,
            transmissionMatrix):
        A = rotationMatrix
        k = lssBarStiffnessMatrix
        B = transmissionMatrix

        # shape of final output
        # [kaa, kab],
        # [kba, kbb]

        kaa = A.T.dot(k).dot(A)
        kba = B.dot(kaa)
        kab = kba.T
        kbb = B.dot(kab)

        col1 = pd.concat([kaa, kba])
        col2 = pd.concat([kab, kbb])

        return pd.concat([col1, col2], axis=1)


class LoadMatrix:
    def lss(N, V, M):
        return pd.DataFrame([[N], [V], [M]])

    def gss(localMatrix, A0_transp):
        return A0_transp.dot(localMatrix)

    def super(globalMatrix_1, globalMatrix_2):
        return pd.concat([globalMatrix_1, globalMatrix_2])
