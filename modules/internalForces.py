from dataclasses import dataclass, field
from modules.model import Bar


class BaseFunctions:
    def loadPosition(self, barLength, load):
        a_distance = barLength - barLength * load.F_position
        b_distance = barLength - a_distance
        return a_distance, b_distance

    def bendingMoment_F(self, load, distance):
        [a_distance, b_distance] = distance
        barLength = a_distance + b_distance

        Ma = -load.F * a_distance * b_distance**2 / barLength**2
        Mb = load.F * a_distance**2 * b_distance / barLength**2
        return Ma, Mb

    def bendingMoment_Q(self, load, distance):
        [a_distance, b_distance] = distance
        barLength = a_distance + b_distance

        Ma = -load.Q * barLength**2 / 12
        Mb = load.Q * barLength**2 / 12
        return Ma, Mb

    def shearForce_F(self, load, distance):
        [a_distance, b_distance] = distance
        barLength = a_distance + b_distance

        Va = -load.F * b_distance**2 / \
            barLength**3 * (barLength + 2 * a_distance)
        Vb = -load.F * a_distance**2 / \
            barLength**3 * (barLength + 2 * b_distance)
        return Va, Vb

    def shearForce_Q(self, load, distance):
        [a_distance, b_distance] = distance
        barLength = a_distance + b_distance

        Vb = -load.Q * barLength / 2
        Va = -load.Q * barLength / 2
        return Va, Vb


@dataclass
class Load:
    Q: int = 0
    F: int = 0
    F_position: int = 0.5


@dataclass
class InternalForces_primary(BaseFunctions):
    load: Load
    bar: Bar = field(repr=False)

    Ma: int = field(init=False, default_factory=lambda: 0)
    Mb: int = field(init=False, default_factory=lambda: 0)

    Va: int = field(init=False, default_factory=lambda: 0)
    Vb: int = field(init=False, default_factory=lambda: 0)

    def __post_init__(self) -> None:
        # define local variables
        barLength = self.bar.len
        load = self.load
        distance = self.loadPosition(barLength, load)

        # assign to self
        if self.load.F != 0:
            [self.Ma, self.Mb] = self.bendingMoment_F(load, distance)
            [self.Va, self.Vb] = self.shearForce_F(load, distance)
        if self.load.Q != 0:
            [self.Ma, self.Mb] = self.bendingMoment_Q(load, distance)
            [self.Va, self.Vb] = self.shearForce_Q(load, distance)
