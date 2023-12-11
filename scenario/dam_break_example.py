"""Example run of the DamBreak scenario based on Inductiva API."""
import dam_break
import post_processing
from utils import fluid_types

dam_break = dam_break.DamBreak(fluid=fluid_types.WATER)

task = dam_break.simulate(simulation_time=4, resolution="medium")

task.wait()
output_dir = task.download_outputs()

simulation_output = post_processing.SPHSimulationOutput(output_dir)
simulation_output.render(fps=60)
