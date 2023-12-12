"""DamBreak scenario based on the FluidBlock scenario."""
import enum
from typing import List, Literal, Optional
from dataclasses import dataclass

from inductiva import tasks, resources, simulators

import utils
import fluid_block


@dataclass
class ParticleRadius(enum.Enum):
    """Sets particle radius according to resolution."""
    HIGH = 0.008
    MEDIUM = 0.01
    LOW = 0.02


class DamBreak(fluid_block.FluidBlock):
    """Physical scenario of a dam break simulation."""

    def __init__(
        self,
        fluid: utils.fluid_types.FluidType = utils.fluid_types.WATER,
        dimensions: Optional[List[float]] = None,
        position: Optional[List[float]] = None,
    ):
        """Initializes a `DamBreak` object.

        Args:
            fluid: A fluid type to simulate.
            dimensions: A list containing fluid column dimensions,
              in meters.
            position: A list containing fluid column position in a tank,
              in meters.
            """

        if dimensions is None:
            dimensions = [0.3, 0.3, 0.3]

        super().__init__(density=fluid.density,
                         kinematic_viscosity=fluid.kinematic_viscosity,
                         dimensions=dimensions,
                         position=position)

    # pylint: disable=arguments-renamed
    def simulate(
        self,
        simulator: simulators.Simulator = simulators.SplishSplash(),
        machine_group: Optional[resources.MachineGroup] = None,
        storage_dir: Optional[str] = "",
        resolution: Literal["high", "medium", "low"] = "low",
        simulation_time: float = 1,
    ) -> tasks.Task:
        """Simulates the scenario.

        Args:
            simulator: Simulator to use.
            machine_group: The machine group to use for the simulation.
            resolution: Resolution of the simulation.
            simulation_time: Simulation time, in seconds.
            storage_dir: The parent directory where the simulation results
            will be stored.
        """

        # Inherit the simulate from the Parent of FluidBlock (Scenario) to
        # avoid overriding the api_method_prefix with the one of FluidBlock.
        task = super().simulate(
            simulator=simulator,
            machine_group=machine_group,
            storage_dir=storage_dir,
            particle_radius=ParticleRadius[resolution.upper()].value,
            simulation_time=simulation_time)

        return task
