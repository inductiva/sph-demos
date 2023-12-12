"""Example run of the FluidBlock scenario based on Inductiva API."""
import fluid_block
import post_processing

# Initialize the FluidBlock scenario
fluidblock = fluid_block.FluidBlock(
    density=1400,
    kinematic_viscosity=1e-4,
    dimensions=[0.3, 0.3, 0.3],
    position=[0, 0, 0.5],
    initial_velocity=[1., 0, 0],
)

# Launch the simulation
task = fluidblock.simulate(particle_radius=0.01, simulation_time=4)

# Wait for the simulation to finish and download the results
task.wait()
output_dir = task.download_outputs()

# Render a video of the simulation
simulation_output = post_processing.SPHSimulationOutput(output_dir)
simulation_output.render(fps=60)
