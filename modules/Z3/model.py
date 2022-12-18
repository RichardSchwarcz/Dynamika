from dataclasses import dataclass, field
import math
import numpy as np
import pandas as pd


@dataclass
class Point:
    x: int
    y: int
    number: int


@dataclass
class BarProps:
    FI: int
    E: int

    @property
    def A(self):
        return np.pi * (self.FI*(10**-3)/2)**2


@dataclass
class Load:
    no_points: int
    no_iterations: int
    force: float

    @property
    def vector(self):
        # create Nx1 matrix of zeros because we have N points and each point has 2 DOF
        loadVector = np.zeros((self.no_points*2, 1))
        # fill matrix with values of load P at point 2 in y direction
        loadVector[3] = self.force/self.no_iterations
        return loadVector


@dataclass
class Bar:
    point_a: Point
    point_b: Point
    bar_props: BarProps
    F: list = field(default_factory=list)
    points_displacements: list = field(default_factory=list)

    @property
    def angle(self):
        return angle(self.point_a, self.point_b)

    @property
    def len(self):
        return calculateDistance(self.point_a, self.point_b)

    @property
    def Amatrix(self):
        return np.array([[np.cos(self.angle), np.sin(self.angle), 0, 0],
                         [-np.sin(self.angle), np.cos(self.angle), 0, 0],
                         [0, 0, np.cos(self.angle), np.sin(self.angle)],
                         [0, 0, -np.sin(self.angle), np.cos(self.angle)]])

    @property
    def elasticMatrix(self):
        E = self.bar_props.E
        A = self.bar_props.A
        L = self.len

        return np.array([[E*A/L, 0, -E*A/L, 0],
                         [0, 0, 0, 0],
                         [-E*A/L, 0, E*A/L, 0],
                         [0, 0, 0, 0]])

    @property
    def geometryMatrix(self):
        # sum forces in F list and divide by bar length
        F = sum(np.abs(self.F))/self.len
        return np.array([[0, 0, 0, 0],
                         [0, F, 0, -F],
                         [0, 0, 0, 0],
                         [0, -F, 0, F]])

    @property
    def stiffnessMatrix_GSS(self):
        return self.Amatrix.T @ (self.geometryMatrix + self.elasticMatrix) @ self.Amatrix

    def points_displacements_setter(self, point_a: np.array, point_b: np.array):
        self.points_displacements = np.concatenate((point_a, point_b), axis=0)

    @property
    def end_forces(self):
        return self.stiffnessMatrix_GSS @ self.points_displacements

    @property
    def internal_forces(self):
        return self.Amatrix @ self.end_forces


@dataclass
class Bar_linear:
    point_a: Point
    point_b: Point
    bar_props: BarProps
    F: list = field(default_factory=list)
    points_displacements: list = field(default_factory=list)

    @property
    def angle(self):
        return angle(self.point_a, self.point_b)

    @property
    def len(self):
        return calculateDistance(self.point_a, self.point_b)

    @property
    def A0_matrix(self):
        return np.array([[np.cos(self.angle), np.sin(self.angle), 0],
                         [-np.sin(self.angle), np.cos(self.angle), 0],
                         [0, 0, 1]])

    @property
    def B_matrix(self):
        lx = self.point_b.x - self.point_a.x
        ly = self.point_b.y - self.point_a.y

        return np.array([
                        [-1, 0, 0],
                        [0, -1, 0],
                        [-ly, lx, -1]
                        ])

    @property
    def k0_matrix(self):
        E = self.bar_props.E
        A = self.bar_props.A
        L = self.len
        return np.array([
                        [E*A/L, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0]
                        ])

    @property
    def stiffnessMatrix_GSS(self):
        kaa = self.A0_matrix.T @ self.k0_matrix  @ self.A0_matrix
        kba = self.B_matrix @ kaa
        kab = kba.T
        kbb = self.B_matrix @ kab

        # return pd.DataFrame(np.concatenate((np.concatenate((kaa, kab), axis=1), np.concatenate((kba, kbb), axis=1)), axis=0))
        return {
            'matrix': pd.DataFrame(np.concatenate((np.concatenate((kaa, kab), axis=1), np.concatenate((kba, kbb), axis=1)), axis=0)),
            'kaa': kaa,
            'kab': kab,
            'kbb': kbb,
            'kba': kba

        }


def angle(A, B):
    point_1 = [A.x, A.y]
    point_2 = [B.x, B.y]

    # protilahla
    l_protilahla = point_2[1] - point_1[1]

    # prilahla
    l_prilahla = point_2[0] - point_1[0]

    angle = np.arctan(l_protilahla/l_prilahla)
    return angle


def calculateDistance(A, B):
    point_1 = [A.x, A.y]
    point_2 = [B.x, B.y]
    return math.sqrt((abs(point_2[0]) - abs(point_1[0]))**2 + (abs(point_2[1]) - abs(point_1[1]))**2)
