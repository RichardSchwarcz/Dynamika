from dataclasses import dataclass, field
from modules.model import Bar


@dataclass
class Load:
    Q: int = 0
    F: int = 0
    F_position: int = 0.5


@dataclass
class BendingMoment:
    load: Load
    bar: Bar = field(repr=False)

    barLength: int = field(init=False)
    Ma: int = field(init=False, default_factory=lambda: 0)
    Mb: int = field(init=False, default_factory=lambda: 0)

    def __post_init__(self) -> None:
        self.barLength = self.bar.len

        if self.load.F != 0:
            a_distance = self.barLength - self.barLength * self.load.F_position
            b_distance = self.barLength - a_distance

            self.Ma = -self.load.F * a_distance * b_distance**2 / self.barLength**2
            self.Mb = self.load.F * a_distance**2 * b_distance / self.barLength**2

        if self.load.Q != 0:
            self.Ma = -self.load.Q * self.barLength**2 / 12
            self.Mb = self.load.Q * self.barLength**2 / 12


@dataclass
class ShearForce:
    load: Load
    bar: Bar = field(repr=False)

    barLength: int = field(init=False)
    Va: int = field(init=False, default_factory=lambda: 0)
    Vb: int = field(init=False, default_factory=lambda: 0)

    def __post_init__(self) -> None:
        self.barLength = self.bar.len

        if self.load.F != 0:
            a_distance = self.barLength - self.barLength * self.load.F_position
            b_distance = self.barLength - a_distance

            self.Va = -self.load.F * b_distance**2 / \
                self.bar.len**3 * (self.bar.len + 2 * a_distance)

            self.Vb = -self.load.F * a_distance**2 / \
                self.bar.len**3 * (self.bar.len + 2 * b_distance)

        if self.load.Q != 0:
            self.Va = -self.load.Q * self.barLength / 2
            self.Vb = -self.load.Q * self.barLength / 2
