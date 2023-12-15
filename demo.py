from lib import models
from lib import scenarios, post_processing
import numpy as np

# --- Initialize Fluid Block model ---

dam_block = models.FluidBlock(models.WATER.density,
                              models.WATER.kinematic_viscosity,
                              dimension=np.array([0.3, 0.3, 0.3]))

# --- Initialize simulation parameters ---

sim_parameters = scenarios.SimulationParameters()
sim_parameters.particle_radius = models.ParticleResolution.MEDIUM.value

# --- Run Fluid block scenario with SplishSplash ---
print("Fluid block scenario with SplishSplash")

scenario = scenarios.FluidBlockSplishSplash(dam_block)
task = scenario.simulate(sim_parameters)

task.wait()
output_dir = task.download_outputs(output_dir="splishsplash_output")
post_processing.render(output_dir)

# --- Fluid block scenario with DualSPHysics ---
print("Fluid block scenario with DualSPHysics")
scenario = scenarios.FluidBlockDualSPHysics(dam_block)
task = scenario.simulate(sim_parameters)

task.wait()
output_dir = task.download_outputs()
post_processing.render(output_dir)
