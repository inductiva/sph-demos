# Fluid Block simulation

Consider the following SPH simulation: a **fluid block** with certain physical properties
is set free under the effect of gravity.

**Drop the block:**

<div align="center">
    <img src="/assets/fluid_block.gif" width=500 alt="Fluid Block Movie">
</div>


For this simulation, we need to configure the input files with the specific properties
of the block. Imagine now that we want to change these properties, or even better, 
we want to generate a dataset with different properties. How would we do it?

One could manually change the input files and simulate for each set of parameters.
However, this is a tedious and error-prone task. Moreover, it is not scalable.

**Inductiva API** provides a simple interface to iterate over several arrangements
of parameters and run the simulations at scale. This is done by creating a **simulation scenario**.

Let's see how to run the above simulation with a **simulation scenario** with a
`FluidBlockSplishSplash` scenario. 

```python
import numpy as np
from lib import models
from lib import scenarios

# Configure a water block
fluid_block = models.FluidBlock(position=np.array([0., 0., 0.3]))

# Initialize the scenario
scenario = scenarios.FluidBlockSlishSplash(fluid_block)

# Configure the simulation parameters
sim_params = scenarios.SimulationParameters()

# Run the simulation
task = scenario.simulate(sim_params)
```

It is that simple! Want to change any of the parameters or generate a dataset,
Python is all you need! 

```python
num_samples = 100
tasks_list = []

for k in range(num_samples):
    sample_position = np.random.uniform(low=[0., 0., 0.],
                                        high=[0.5, 0.5, 0.5],
                                        size=(3,))

    # Configure a water block
    fluid_block = models.FluidBlock(position=position)
    scenario = scenarios.FluidBlockScenario(fluid_block)
    sim_params = scenarios.SimulationParameters()

    # Run the simulation
    task = scenario.simulate(sim_params)
    tasks_list.append(task)
```

Multiple simulations will be launched and you can track and download the results when
they finish, all with **Inductiva API**.

If your interest was piqued, let's see how to create a simulation scenario!

## Create the Fluid Block scenario

The `FluidBlock` is characterized by a block of fluid with certain physical properties
to be let free under the effect of gravity. The scenario allows users to configure the physical
properties of the block, namely density and kinematic viscosity, and the dimensions and position
of the tank. The initial velocity of the block is also configurable. Moreover, the simulator is
configured with only a few parameters, such as the simulation time, the particle radius,
the time step and the output export rate.

This scenario is meant to **inspire** the creation of your simulation workflows.

#### Pick your simulator

The first step is simple, **pick your simulator** of choice. For this example, we will
use the [SplishSplash simulator](SPH_SIMULATIONS.md#splishsplash) via Inductiva API.

The mechanism that allows the creation a simulation scenario is the **templating** of the
simulation input files.

#### Template the input files

Templating is the act of substituting some variables in your input files with tags that
identify the parameters you want to change. With **Inductiva API** you can substitute
these parameters on the fly when selecting different values.

##### Example of template file

To template a file one needs to substitute the variables with `{{ parameter_name }}`.
For example, the `fluid_block.json` file can be templated as:

<div style="display: flex; justify-content: space-between;">
<div>
    <h7>Input File</h7>
    <img src="/assets/file_example.png" alt="File Example">
</div>
<div>
    <h7>Template file</h7>
    <img src="/assets/template_file_example.png" alt="Template Example">
</div>
</div>

These templated files are set in a single directory. For this scenario, we have the
following template directory:

```
   templates/splishsplash
    |
    |- fluid_block.json.jinja
    |- unit_box.obj
```

In this directory, we set all of the files (templated or not) required to run the
simulation: `fluid_block.json.jinja` and `unit_box.obj`.

We remark that templated files need to contain the suffix `.jinja`. Otherwise they won't be
modified. Other extra files can be added as you wish to the template directory.

With the parameters templated, we can now create the `FluidBlock` scenario.


#### `FluidBlock` class

The `FluidBlock` class configures the template files as you wish and runs the
simulation via **Inductiva API**.

We break this scenario into three classes: `FluidBlock`, `SimulationParameters` and
`FluidBlockSplishSplash`. The first two classes define the parameters that are
set with the same name in the template files.

##### Input Parameters

The `FluidBlock` contains the properties of the block:

```python
@dataclass
class FluidBlock:
    density: float
    kinematic_viscosity: float
    dimension: np.array
    position: np.array = np.zeros(3)
    velocity: np.array = np.zeros(3)

    def to_dict(self):
        return asdict(self)
```

The `SimulationParameters` hold the simulation parameters:

```python
@dataclass
class SimulationParameters:
    output_export_rate: float = 60
    particle_radius: float = 0.02
    simulation_time: float = 1
    time_step: float = 0.001

    def to_dict(self):
        return asdict(self)
```

The `to_dict` method converts the parameters of the class into a dictionary that
will be used as input in the templating method. 

The `FluidBlockSplishSplash` class contains the simulation workflow, which uses the
`inductiva.mixin.FileManager` class to manage and template the input files.

##### Simulation Workflow

Let's go over it step by step! The first block is the initialization of the class. For this
scenario we initialize with a `FluidBlock` object, as follows:

```python
class FluidBlockSplishSplash(inductiva.mixins.FileManager):

    def __init__(self, fluid_block: FluidBlock):
        self.fluid_block = fluid_block
```

Now, the magic is set in the `simulate` method, where the user can use the templating tools
present in the `inductiva.mixin.FileManager` class to:
- Set up the root directory for the simulation;
- Add general files or directories;
- Render them on the spot with the parameters provided by the user.

The two last points are both done with `add_file` and `add_dir` methods. In case the `render_args`
(`dict`) are passed the template occurs on the spot. Otherwise, the file or directory is
copied as is.

Let's go through the `simulate` method for our current scenario.

```python

    def simulate(
        self,
        sim_params: SimulationParameters,
        machine_group = None
    ):
    # 1 - Set the root directory. 
    # The add_file and add_dir methods use it by default.
    self.set_root_dir("fluid_block_scenario")

    # 2 - Configure the Fluid Block params
    fluid_margin = 2 * sim_params.particle_radius
    block_params = self.fluid_block.to_dict()
    block_params["position"] += fluid_margin
    block_params["dimension"] -= 2 * fluid_margin

    # 3 - Render template directory with the
    # parameters of the fluid block and simulation. 
    self.add_dir("templates/splishsplash",  
                 **block_params, **sim_params.to_dict())

    # 4 - Run the simulation
    task = inductiva.simulators.SplishSplash().run(
        input_dir = self.get_root_dir(),
        sim_config_filename="fluid_block.json",
        machine_group=machine_group
    )

    return task
```

###### `simulate()` break down

The `simulate` method encapsulates several steps to simplify the workflow!
We set the root directory for the file manager - the `add_file` and `add_dir`
methods use it as their base directory. Next, we configure the render parameters further.
In some simulation scenarios, the parameters we expose to the user aren't the
ones in the template files. Here, for example, we translate the block so that it is
inside the container.
The goal is to free the user from all nuances of setting up the simulator. 

With all the parameters prepared, the input directory of the simulation is created
in the `root_dir`. We directly render the template directory with the `FluidBlock` 
and `SimulationParameters` into the root directory. 

This is the core of the creation of a simulation scenario. The final step is to
use the **Inductiva API** to run the abstracted simulator with the prepared
configurations. In this case, we use the `SplishSplash` simulator and run it
with the `fluid_block.json` file as input.

#### Explore other variations

The workflow is already implemented (with a few tweaks) within the `models.py` file -
which contains the `FluidBlock` -  and the `scenarios.py` file - with the `SimulationParameters`
and `FluidBlockSplishSplash`.

Go over them now by yourself and soon you will be a power developer of your simulation
scenarios! You also learn how to integrate other SPH simulators with the same parameters.

To finish let's run a scenario simulation!

#### Run the scenario

To run the scenario, we first initialize the fluid block and the simulation parameters.
To get things going, we have already prepared a method to create a movie for this
specific simulation!

```python
import numpy as np

from lib import models
from lib import scenarios
from lib import post_processing

# Set the FluidBlock parameters
dam_block = models.FluidBlock(density=1000, kinematic_viscosity=1e-6,
                              dimension=np.array([0.3, 0.3, 0.3]))

# Set the Simulation parameters
sim_params = scenarios.SimulationParameters()
```

Then, we can start with initializing the scenario itself with the fluid block:

```python
scenario = scenarios.FluidBlockSplishSplash(dam_block)
```

For the final trick, we run the simulation:
```python
task = scenario.simulate(sim_parameters)

# Wait for it to finish and get the results
task.wait()
output = task.download_outputs()

# Render the movie
post_processing.render(output, fps=60)
```

When running this script you will obtain the following logs in the terminal:

<div>
<img src="/assets/simulation_logs.png" alt="Simulation Logs">
</div>

At the end, a video will be ready in the output folder:

<div style="display: flex; justify-content: center;">
    <img src="/assets/fluid_block_2.gif" width=500 alt="Fluid Block Movie">
</div>
