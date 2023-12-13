"""Example run of the FluidBlock scenario based on Inductiva API."""
import fluid_block
import post_processing
import inductiva

machine = inductiva.resources.MachineGroup(
    machine_type="c2d-standard-16"
)
machine.start()
# Initialize the FluidBlock scenario
fluidblock = fluid_block.FluidBlock(
    density=1200,
    kinematic_viscosity=1e-4,
    dimensions=[0.3, 0.3, 0.3],
    position=[0, 0, 0.5],
    initial_velocity=[1., 0, 0],
)

# Launch the simulation
task = fluidblock.simulate(
    simulator=inductiva.simulators.SplishSplash(),
    particle_radius=0.01, simulation_time=4,
    machine_group=machine)

# Wait for the simulation to finish and download the results
task.wait()
output_dir = task.download_outputs()

# Render a video of the simulation
simulation_output = post_processing.SPHSimulationOutput(output_dir)
simulation_output.render(fps=60)

machine.terminate()