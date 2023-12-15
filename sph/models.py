"""Fluid Block Model"""
from dataclasses import dataclass, asdict
import enum

import numpy as np


@dataclass
class FluidBlock:
    """Physical model of a block of fluid.
    
    Attributes:
        fluid_density: The density of the fluid in kg/m^3.
            Valid range is [400, 2000] kg/m3.
        kinematic_viscosity: The kinematic viscosity of the fluid, in m^2/s.
            Reference value for water is 1e-6 m^2/s.
        dimension: The fluid block dimensions (in x, y, z), in meters.
        position: The position of the fluid block in the tank
            (in x, y, z), in meters.
        velocity: The initial velocity of the fluid block
            (in x, y, z), in m/s.
    """
    density: float
    kinematic_viscosity: float
    dimension: np.array
    position: np.array = np.zeros(3)
    velocity: np.array = np.zeros(3)

    def __post_init__(self):
        """Validates the input parameters after initialization."""

        assert 400 <= self.density <= 2000, '`density` should be in [400, 2000]'
        assert len(self.dimension) == 3, '`dimension` should have 3 components'
        assert len(self.velocity) == 3, '`velocity` should have 3 components'
        assert len(self.position) == 3, '`position` should have 3 components'

    def to_dict(self):
        """Returns a dictionary representation of the model."""
        return asdict(self)


@dataclass(eq=True, frozen=True)
class FluidType:
    """Model for the physical properties of a fluid."""

    density: float
    kinematic_viscosity: float

    def to_dict(self):
        """Returns a dictionary representation of the model."""
        return asdict(self)


# Properties of Water, Honey and Olive Oil
WATER = FluidType(density=1000, kinematic_viscosity=1e-6)
HONEY = FluidType(density=1400, kinematic_viscosity=7.14e-3)
OLIVE_OIL = FluidType(density=905, kinematic_viscosity=4.32e-5)


class ParticleResolution(enum.Enum):
    """Sets particle radius according to resolution."""
    HIGH = 0.008
    MEDIUM = 0.01
    LOW = 0.02
