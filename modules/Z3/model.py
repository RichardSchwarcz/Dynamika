from dataclasses import dataclass, field
import math
import numpy as np


@dataclass
class Point:
    x: int
    y: int


@dataclass
class BarProps:
    FI: int
    E: int

    @property
    def A(self):
        return np.pi * (self.FI*(10**-3)/2)**2


@dataclass
class Bar:
    point_a: Point
    point_b: Point

    @property
    def angle(self):
        return angle(self.point_a, self.point_b)

    @property
    def len(self):
        return calculateDistance(self.point_a, self.point_b)


def angle(A, B):
    point_1 = [A.x, A.y]
    point_2 = [B.x, B.y]

    # protilahla
    l_protilahla = point_2[1] - point_1[1]

    # prilahla
    l_prilahla = point_2[0] - point_1[0]

    angle = np.rad2deg(np.arctan(l_protilahla/l_prilahla))
    return angle


def calculateDistance(A, B):
    point_1 = [A.x, A.y]
    point_2 = [B.x, B.y]
    return math.sqrt((abs(point_2[0]) - abs(point_1[0]))**2 + (abs(point_2[1]) - abs(point_1[1]))**2)
