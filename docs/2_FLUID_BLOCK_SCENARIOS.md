# Fluid Block simulation

The examples in this section extend upon the straightforward API calls from the
[previous section](SPH_SIMULATIONS.md) and show how the user can abstract the
scientific problem into scenarios that use the API's robust templating mechanism
to dynamically generate input files for their simulations.

## Dropping the block

The examples herein aim at simulating the fluid dynamics of a falling fluid block
with variable dimensions, initial position and velocity, into an empty cubic
container. The following clip illustrates the problem:

<div align="center">
    <img src="/assets/fluid_block.gif" width=500 alt="Fluid Block Movie">
</div>

In what follows, we show how the simulation problem can be broken into
manageable components that allow different configurations of the problem to be
simulated at scale.

### The model

The characteristics of the fluid block can be efficiently encapsulated inside a
Python class that describes the physical invariants of the problem as follows
(see `lib/models.py`):

```python
class FluidBlock:
    density: float
    kinematic_viscosity: float
    dimension: np.array
    position: np.array = np.zeros(3)
    velocity: np.array = np.zeros(3)

    def to_dict(self):
        return asdict(self)
```

Similarly, fluids can easily be described using the following abstraction:

```python
class FluidType:
    density: float
    kinematic_viscosity: float

WATER = FluidType(density=1000, kinematic_viscosity=1e-6)
```

With this, a specific fluid block can be created as follows (e.g. static water
block at rest in the xy-plane):

```python
water_block = FluidBlock(
    density=WATER.density,
    kinematic_viscosity=WATER.kinematic_viscosity,
    dimension=np.array([0.5, 0.5, 0.5]), # meters
)
```

### From models to input files

These abstractions allow for an easy way to characterize the simulation system.
However, the physical model they describe needs to be translated into the input
files required by the simulator.

The **Inductiva API** library provides a powerful mechanism to generate input
files from these parameters using a templating engine. This mechanism allows users
to define template files containing tags that get replaced with specific values
upon rendering. The templating mechanism is integrated into a file packing
interface - the `FileManager` class - that allows users to easily manage the
rendering of the template files.

Consider a simple template file (`template.txt.jinja`) containing the following
content:

```jinja
# content of template.txt.jinja
ParticleRadius = {{ particle_radius }}
```

Using a `FileManager` object, this file can be easily rendered and stored in a
user-specified folder:

```python
from inductiva import mixins

manager = mixins.FileManager()

# specify the user-specific folder where files are to be stored
manager.set_root_dir('myfiles')

# render template.txt.jinja by setting the `particle_radius` to 10
# and specifying the name of the rendered file
manager.add_file('template.txt.jinja', 'rendered.txt', {"particle_radius": 10})
```

Execution of the above snippet yields a newly created `myfiles/` folder
in the current working directory, containing the rendered file `rendered.txt`
with the following content:

```
# content of rendered.txt
ParticleRadius = 10
```

> **NOTE**: `FileManager.add_file` also allows non-template files to be added to
> the manager. Files are considered to be templates when ending with the `.jinja`
> extension.
> `FileManager` also provides an `add_dir` method that behaves pretty much as
> `add_file` by copying and rendering all files inside a directory.

### Building the scenarios

Using the tools above, one can devise another level of abstraction that allows the
user to easily configure parameters and/or model details to deploy multiple 
simulations at scale, without having to manually manage input file content
and job orchestration.

In this section, we introduce the concept of a *Scenario*, the abstraction that
wraps the model, simulation parameters and job deployment into a single interface.

#### SplishSplashScenario

The following snippet shows the implementation of the `FluidBlockSplishSplash`
scenario which is used to run fluid block simulations with SPlisHSPlasH:

```python
class FluidBlockSplishSplash(mixins.FileManager):
    """FluidBlock scenario with SplishSplash simulator."""

    SCENARIO_DIR = "fluid_block_splishsplash"
    SCENARIO_TEMPLATE_DIR = os.path.join(TEMPLATE_DIR, "splishsplash")

    def __init__(self, fluid_block: FluidBlock):
        self.fluid_block = fluid_block

    def simulate(self,
                 sim_params: SimulationParameters,
                 on: Optional[resources.MachineGroup] = None):

        self.set_root_dir(self.SCENARIO_DIR)
        fluid_margin = 2 * sim_params.particle_radius
        block_params = self.fluid_block.to_dict()
        block_params["position"] += fluid_margin
        block_params["dimension"] -= 2 * fluid_margin

        self.add_dir(self.SCENARIO_TEMPLATE_DIR,
                     **block_params,
                     **sim_params.to_dict())

        task = simulators.SplishSplash().run(
            input_dir=self.get_root_dir(),
            sim_config_filename="fluid_block.json",
            on=machine_group,
            storage_dir=self.SCENARIO_DIR)

        return task
```

The `FluidBlockSplishSplash` inherits from `FileManager` all the file management
and rendering tools previously discussed. Each `FluidBlockSplishSplash` instance
is initialized with a fluid model object. This is merely a design choice, based
on the fact that the fluid block should be invariant between different simulation
runs, that can be configured with different simulation parameters. Note, however,
that users need not follow this pattern when implementing their own scenarios.

The `FluidBlockSplishSplash` exposes the `simulate` method that implements all the
required logic to render the template files and deploy the simulation.

In this case, additional logic is required to manipulate the model parameters by
ensuring the fluid block is completely inside the container, according to the
particle radius (specific to SPlisHSPlasH). It aims at showing how derived
parameters can be used to render input files.

The `simulate` method consumes 2 arguments: a `SimulationParameters` and 
`MachineGroup` objects. The former is another convenience class that aggregates
all simulation parameters into a single object, which the user can change
to test different simulation configurations using the same fluid model:

```python
class SimulationParameters:
    simulation_time: float = 1
    particle_radius: float = 0.02
    time_step: float = 0.001
    output_export_rate: float = 60
```

The latter is an **Inductiva API** construct that allows the user to configure
the computational resources used to run the simulations.
By default (`on = None`), the user does not need to configure this
parameter and resources will be managed by default pool (see the
[MachineGroup](https://github.com/inductiva/inductiva/wiki/Machines) documentation
for details on how to configure and use machine groups).

With the scenario and models ready, one can `simulate` a scenario as follows:

```python
import numpy as np

from lib import models
from lib import scenarios

# water block 0.3x0.3x0.3 m^3 at rest in the xy plane
water_block = models.FluidBlock(
    density=models.WATER.density,
    kinematic_viscosity=models.WATER.kinematic_viscosity,
    dimension=np.array([0.3, 0.3, 0.3]))

sim_parameters = scenarios.SimulationParameters()

scenario = scenarios.FluidBlockSplishSplash(water_block)
task = scenario.simulate(sim_parameters)

# wait for it to finish and get the results
task.wait()
output = task.download_outputs()
```

This script creates a SPlisHSPlasH scenario with a water block, submits the
simulation using the default submission queue and waits for the associated task
to finish. Upon completion, all output files are downloaded locally,
(check the [Tasks wiki](https://github.com/inductiva/inductiva/wiki/Tasks) for more
details about tasks).

With the results of the simulation at hand, one can perform post-processing tasks
such as rendering a movie of the simulation. The `lib.post_processing` module
has code to read the `vtk` output files and render the movie of the
simulation shown below:

```python
from lib import post_processing

post_processing.render(output, fps=60)
```

<div align="center">
    <img src="/assets/fluid_block_2.gif" width=500 alt="Fluid Block Movie">
</div>

#### DualSPHysics scenario

With the same logic, one can quickly show how to implement the same scenario
using the DualSPHysics simulator. All methods in the `FluidBlockDualSPHysics`
have the same argument signature as the `FluidBlockSplishSplash` case.
The `DualSPHysics` works differently from `SPlisHSPlasH`. It requires a
set of sequential commands to run the simulation and differs in the way the
particles are configured. These simulator-specific details change the way how the
`simulate` method reads: it implements simulator-specific logic for parameter
manipulation and feeds a set of commands that get passed on to the simulator 
and executed remotely. 

```python
class FluidBlockDualSPHysics(mixins.FileManager):
    ...
    def get_commands(self):
        commands = [
            {
                "cmd": "gencase fluid_block fluid_block -save:all",
                "prompts": []},
            {
                "cmd": "dualsphysics fluid_block fluid_block -dirdataout data -svres",
                "prompts": []},
            {
                "cmd": "partvtk -dirin fluid_block/data -savevtk vtk/PartFluid -onlytype:-all,+fluid",
                "prompts": []
            }]

        return commands

    def simulate(self,
                 sim_params: SimulationParameters,
                 on: Optional[resources.MachineGroup] = None):
        self.set_root_dir(self.SCENARIO_DIR)

        parameters = sim_params.to_dict()
        parameters["particle_distance"] = 2 * sim_params.particle_radius

        # scenario of DualSPHysics is configured with a single file. 
        self.add_file(
            os.path.join(self.SCENARIO_TEMPLATE_DIR, "fluid_block.xml.jinja"),
            "fluid_block.xml", **parameters, **self.fluid_block.to_dict())

        return simulators.DualSPHysics().run(
            input_dir=self.get_root_dir(),
            on=machine_group,
            commands=self.get_commands(),
        )
```

This scenario can now be executed in the same way as the
`FluidBlockSplishSplash`, but using an instance of `FluidBlockDualSPHysics`:

```diff
sim_parameters = scenarios.SimulationParameters()

-  scenario = scenarios.FluidBlockSplishSplash(water_block)
+  scenario = scenarios.FluidBlockDualSPHysics(water_block)
task = scenario.simulate(sim_parameters)

# wait for it to finish and get the results
task.wait()
```


## Running multiple `FluidBlock` simulation

The main reason to work with scenarios is to simplify iteration over multiple
models and configuration parameters to generate data sets or explore design
spaces. **Inductiva API** makes large-scale exploration simple by allowing
multiple simulations to be spawned in parallel.

The user can configure a dedicated group of resources to run a set of simulations
by creating a `MachineGroup` that specifies the type and number of machines.
In the following snippet, we allocate **4 machines** of type **c2-standard-16**
to generate a dataset of 100 simulations, each having a random initial position
of the fluid block. Once the tasks are complete, the associated outputs get
downloaded to a local folder.

```python
import numpy as np
from lib import models
from lib import scenarios

import inductiva

DATASET_SIZE = 100

# allocate and start remote resources
machines = inductiva.resources.MachineGroup(
    machine_type="c2-standard-16",
    num_machines=4)

machines.start()

sim_params = scenarios.SimulationParameters()

tasks = []

for k in range(DATASET_SIZE):
    # model with random position
    position = np.random.uniform(low=0.0, high=0.5, size=3)
    fluid_block = models.FluidBlock(position=position)

    # spawn simulations
    scenario = scenarios.FluidBlockSplishSplash(fluid_block)
    task = scenario.simulate(sim_params, on=machines)
    tasks.append(task)

# wait for tasks to finish and download outputs to a local folder
for task in tasks_list:
    task.wait()
    output = task.download_outputs(output_dir='mydataset')
```

If your interest was piqued, go deeper into the creation of these scenarios by
exploring the `lib` folder.
