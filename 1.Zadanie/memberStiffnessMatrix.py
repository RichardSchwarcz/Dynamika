import pandas as pd


class MemberStiffnessMatrix:

    def localMember(len, A, E, I):
        return pd.DataFrame([[E * A / len, 0, 0],
                             [0, 12 * E * I / len**3, 6 * E * I / len**2],
                             [0, 6 * E * I / len**2, 4 * E * I / len]])

    def globalMember(rotationMatrix, localMemberStiffnessMatrix,
                     transformationMatrix):
        A = rotationMatrix
        k = localMemberStiffnessMatrix
        B = transformationMatrix

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
