# Scenarios

**Inductiva API** provides a framework for users to create personalized scenarios. Scenarios describe a physical model of a process in nature, that can be simulated. With a scenario, the complexity of configuring the simulators is abstracted and allows users to configure only a few parameters to make an exploration of the physical model.

As a **user**, you will have the ability to create your own scenarios. A few fundamental blocks are required to create a scenario:
- Choose the simulators you want to use;
- Template the input files for the simulators;
- Construct the Python code based on Inductiva API.

In this repository, we present two examples of scenarios that simulate the motion of fluid in a cubic tank: the `DamBreak` and the `FluidBlock` scenarios.

The scenarios are meant to **inspire** the creation of personalized scenarios.
Together, with the scenarios we also show how the outputs can be handled by post-processing methods and visualize the results.

To learn more on how to create your scenarios, check the [documentation](https://github.com/inductiva/inductiva/wiki/Build-your-own-scenario).

### Dam break scenario

This scenario simulate the motion of a fluid block under the effect of gravity.
The simulators available are [SPlisHSPlasH](https://github.com/inductiva/inductiva/blob/main/inductiva/simulators/splishsplash.py) and [DualSPHysics](https://github.com/inductiva/inductiva/blob/main/inductiva/simulators/dualsphysics.py), which use the [Smoothed Particle Hydrodynamics](https://en.wikipedia.org/wiki/Smoothed-particle_hydrodynamics) formulation to model the fluid.

One can initialize the scenario with different fluids (Water, Honey, Olive oil) and with fluid blocks of different dimensions and initial positions. Then, users can further configure the simulation time and resolution.

##### Example

We have prepared a Python script to directly run this scenario. Get inside the scenario folder and run the following command:

```bash
python3 dam_break_run.py
```

Or, prepare your own and start changing the parameters. The script should be inside the scenario folder. Copy the code snippet and get started:

```python
import dam_break
import post_processing
from utils import fluid_types

# Initialize the DamBreak scenario
dam_break = dam_break.DamBreak(fluid=fluid_types.WATER)

# Launch the simulation
task = dam_break.simulate(
    simulation_time=4,
    resolution="medium")

# Wait for the simulation to finish and download the results
task.wait()
output_dir = task.download_outputs()

# Post-process the results and render a video of the simulation
simulation_output = post_processing.SPHSimulationOutput(output_dir)
simulation_output.render(fps=60)
```

<p align="center">
  <img src="assets/dam_break.gif" alt="Centered Image" width="400" height="300">


### Fluid Block

This scenario is an extension of the DamBreak scenario, where the fluid can have an initial velocity and the simulation can be configured with more parameters. 

To initialize the scenario users can set the density and kinematic viscosity of the fluid, the dimensions of the fluid block, the initial position and the initial velocity. 

The simulation can be configured with the following parameters: the `particle_radius` (float), the `simulation_time` (float), the `adaptive_time_step` (bool), the `time_step` (float) and the `output_export_rate` (int).

Again, the scenario can be run with both `SplishSplash` and `DualSPHysics` simulators via Inductiva API.

##### Example

We have prepared a Python script to directly run this scenario. Get inside the scenario folder and run the following command:

```bash
python3 fluid_block_example.py
```

Or, prepare your own and start changing the parameters. The script should be inside the scenario folder. Copy the code snippet and get started:

```python
import fluid_block
import post_processing

# Initialize the FluidBlock scenario
fluidblock = fluid_block.FluidBlock(
    density=1000,
    kinematic_viscosity=1e-6,
    dimensions=[0.5, 0.5, 0.5],
    position=[0, 0, 0],
    initial_velocity=[0, 0, 0],
)

# Launch the simulation
task = fluidblock.simulate(
    particle_radius=0.02,
    simulation_time=2)

# Wait for the simulation to finish and download the results
task.wait()
output_dir = task.download_outputs()

# Render a video of the simulation
simulation_output = post_processing.SPHSimulationOutput(output_dir)
simulation_output.render()
```

<p align="center">
  <img src="assets/fluid_block.gif" alt="Centered Image" width="400" height="300">
