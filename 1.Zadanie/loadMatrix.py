import pandas as pd


class LoadMatrix:

    def localMatrix(N, V, M):
        return pd.DataFrame([[N], [V], [M]])

    def globalMatrix(localMatrix, A0_transp):
        return A0_transp.dot(localMatrix)

    def superMatrix(globalMatrix_1, globalMatrix_2):
        return pd.concat([globalMatrix_1, globalMatrix_2])