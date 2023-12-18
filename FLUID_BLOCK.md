# Build custom simulation scenarios with Inductiva API

**Inductiva API** provides a framework for users to create personalized simulation scenarios. These scenarios describe a physical model of a process in nature, that can be simulated. The configuration of the simulator is complex and takes a lot of work. 

The goal is to abstract this complexity and explore the physical model by changing only a few parameters. All of the other ones are fixed and stored within the scenario.

**Developers** can create personalized simulation scenarios with the following fundamental blocks:
- Choose a simulator among the available ones in the Inductiva API;
- Template the input files for the simulators;
- Construct a Python class or method based on Inductiva API to manage your workflow.

## Fluid Block simulation scenario

In this repository, we present an approach for creating a simulation scenario for the motion of fluid in a cubic tank using SPH: the `FluidBlock` scenario.

The `FluidBlock` is characterized by a block of fluid with certain physical properties to be let free under the effect of gravity. For simplicity, we assume this block will be inside a cubic tank. We will allow users to configure the physical properties of the block, namely density and kinematic viscosity, and the dimensions and position of the tank. The initial velocity of the block will also be configurable.
Moreover, the simulator can also be configured with only a few parameters, such as the simulation time, the particle radius, the time step and the output export rate.

This scenario is meant to **inspire** the creation of your simulation workflows. Together, with the scenarios we also show how the outputs can be handled by post-processing methods and visualize the results.

## Building your simulation scenario

The first step is simple, **pick your simulator** of choice. For this example, we will use the [SplishSplash simulator](SPH_SIMULATIONS.md#splishsplash) via Inductiva API.

Let's prepare the template files and directory.

#### Template the input files

Templating is the act of substituting some variables in your input files with tags that identify the parameters you want to change. With **Inductiva API** you can substitute these parameters on the fly when selecting different values.

###### Example of template file

To template a file one needs to substitute the variables with `{{ parameter_name }}`. For example, the `fluid_block.json` file can be templated as:
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

With the parameters templated, we can now create the `FluidBlock` scenario.

These templated files are set in a single directory. For this scenario, we have the following template directory:

```
   templates/splishsplash
    |
    |- fluid_block.json.jinja
    |- unit_box.obj
```

In this directory, we set all of the files (templated or not) required to run the simulation: `fluid_block.json.jinja` and `unit_box.obj`.

We remark that templated files need to contain the suffix `.jinja`. Otherwise they won't be modified. Other extra files can be added as you wish to the template directory.


#### Create the simulation scenario class

With the above setup, we are now ready to create the Python interface for the `FluidBlock` scenario via **Inductiva API**.

We break this scenario into three classes: `FluidBlock`, `SimulationParameters` and `FluidBlockSplishSplash`. The first two classes will define the parameters that will be set in the template files, with the same exact name.

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

The `to_dict` method converts the parameters of the class into a dictionary that will be used as input in the templating method. 

The `FluidBlockSplishSplash` class contains the simulation workflow, which uses the `inductiva.mixin.FileManager` class to manage and template the input files.

##### Simulation Workflow

Let's go over it step by step! The first block is the initialization of the class. For this scenario we initialize with a `FluidBlock` object, as follows:

```python
class FluidBlockSplishSplash(inductiva.mixins.FileManager):

    def __init__(self, fluid_block: FluidBlock):
        self.fluid_block = fluid_block
```

Now, the magic is set in the `simulate` method, where the user can use the templating tools present in the `inductiva.mixin.FileManager` class to:
- Set up the root directory for the simulation;
- Add general files or directories;
- Render them on the spot with the parameters provided by the user.

The two last points are both done with `add_file` and `add_dir` methods. In case the `render_args` (`dict`) are passed the template occurs on the spot. Otherwise, the file or directory is copied as is.

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

The method contains several steps:
- **Set the root directory**: we configure the root directory for the simulation, set the parameters of the fluid block and render the template directory with the parameters of the fluid block and simulation. Finally, we run the simulation with the `SplishSplash` simulator.
- **Fluid block parameters**: Some parameters need to be further configured for the purpose of the simulation.
- **Render template directory**: The `add_dir` method renders the template directory with the parameters of the fluid block and simulation. The `**` operator unpacks the dictionaries into a single one.
- **Run the simulation**: Finally, we run the simulation with the `SplishSplash` simulator.
