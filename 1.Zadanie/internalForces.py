class BendingMoment:

    def _init_(self, length, F, q):
        self.length = length
        self.F = F
        self.q = q

    def pointLoad_A(length, F):
        return F * length / 8

    def pointLoad_B(length, F):
        return -F * length / 8

    def distributedLoad_A(length, q):
        return -q * length**2 / 12

    def distributedLoad_B(length, q):
        return -q * length**2 / 12


class ShearForce:

    def _init_(self, length, F, q):
        self.length = length
        self.F = F
        self.q = q

    def pointLoad(F):
        return F / 2

    def distributedLoad(length, q):
        return q * length / 2
