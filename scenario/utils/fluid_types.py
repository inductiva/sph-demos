"""Physical properties of different fluid types."""
from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class FluidType:
    """Define the properties of a certain fluid."""
    density: float
    kinematic_viscosity: float

    def to_dict(self):
        """Convert to dict."""
        return {
            "density": self.density,
            "kinematic_viscosity": self.kinematic_viscosity,
        }


# Properties of WATER
WATER = FluidType(density=1000, kinematic_viscosity=1e-6)

HONEY = FluidType(
    density=1400,
    kinematic_viscosity=7.14e-3,
)

OLIVE_OIL = FluidType(
    density=905,
    kinematic_viscosity=4.32e-5,
)
