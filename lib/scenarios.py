"""Scenarios with SPH simulators via Inductiva API."""
from dataclasses import dataclass, asdict
from typing import Optional
import os

import inductiva

from .models import FluidBlock

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


@dataclass
class SimulationParameters:
    """Simulation-specific configuration parameters"""
    simulation_time: float = 1
    particle_radius: float = 0.02
    time_step: float = 0.001
    output_export_rate: float = 60

    def to_dict(self):
        """Returns a dictionary representation of the simulation parameters."""
        return asdict(self)


class FluidBlockSplishSplash(inductiva.mixins.FileManager):
    """FluidBlock scenario with SplishSplash simulator."""

    SCENARIO_DIR = "fluid_block_splishsplash"
    SCENARIO_TEMPLATE_DIR = os.path.join(TEMPLATE_DIR, "splishsplash")

    def __init__(self, fluid_block: FluidBlock):
        """Initializes the FluidBlock scenario.

        Args:
            fluid_block: The fluid block model.
        """
        self.fluid_block = fluid_block

    def simulate(
        self,
        sim_params: SimulationParameters,
        machine_group: Optional[inductiva.resources.MachineGroup] = None
    ) -> inductiva.tasks.Task:

        self.set_root_dir(self.SCENARIO_DIR)
        fluid_margin = 2 * sim_params.particle_radius
        block_params = self.fluid_block.to_dict()
        block_params["position"] += fluid_margin
        block_params["dimension"] -= 2 * fluid_margin

        self.add_dir(self.SCENARIO_TEMPLATE_DIR, **block_params,
                     **sim_params.to_dict())

        task = inductiva.simulators.SplishSplash().run(
            input_dir=self.get_root_dir(),
            sim_config_filename="fluid_block.json",
            machine_group=machine_group,
            storage_dir=self.SCENARIO_DIR)

        return task


class FluidBlockDualSPHysics(inductiva.mixins.FileManager):
    """FluidBlock scenario with DualSPHysics simulator."""

    SCENARIO_DIR = "fluid_block_dualsphysics"
    SCENARIO_TEMPLATE_DIR = os.path.join(TEMPLATE_DIR, "dualsphysics")

    def __init__(self, fluid_block: FluidBlock):
        """Initializes the FluidBlock scenario.

        Args:
            fluid_block: The fluid block model.
        """
        self.fluid_block = fluid_block

    def get_commands(self):
        commands = [{
            "cmd": "gencase fluid_block fluid_block -save:all",
            "prompts": []
        }, {
            "cmd":
                "dualsphysics fluid_block fluid_block -dirdataout data -svres",
            "prompts": []
        }, {
            "cmd":
                "partvtk -dirin fluid_block/data -savevtk vtk/PartFluid -onlytype:-all,+fluid",
            "prompts": []
        }]

        return commands

    def simulate(
        self,
        sim_params: SimulationParameters,
        machine_group: Optional[inductiva.resources.MachineGroup] = None
    ) -> inductiva.tasks.Task:
        self.set_root_dir(self.SCENARIO_DIR)

        parameters = sim_params.to_dict()
        parameters["particle_distance"] = 2 * sim_params.particle_radius

        self.add_file(
            os.path.join(self.SCENARIO_TEMPLATE_DIR, "fluid_block.xml.jinja"),
            "fluid_block.xml", **parameters, **self.fluid_block.to_dict())

        return inductiva.simulators.DualSPHysics().run(
            input_dir=self.get_root_dir(),
            machine_group=machine_group,
            commands=self.get_commands(),
        )
