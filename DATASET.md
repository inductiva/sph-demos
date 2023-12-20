## Generate a Dataset via Inductiva API

Whether you want to explore a design space or generate a dataset for machine learning,
**Inductiva API** has you covered. Now, that you know how to run an SPH simulation and build
a scenario, all that is required is to select the range of parameters you want to explore
and add a `for` loop to your workflow.

Of course, running one simulation at a time would be a pain. **Inductiva API** simplifies it and
you can generate a dataset with the simulations distributed over multiple machines.

Let's see an example for 100 simulations with different parameters and with
the simulations distributed over 10 machines!

If you are a solo adventurer, you can get started with the script `generate_dataset.py`
in the `scenario` folder. Otherwise, let's go step by step. Our starting point is the `FluidBlock`
scenario we have created previously, to make this exploration.

In this dataset, we want to vary the position, dimensions and velocity of the fluid block,
as well as the viscosity of the fluid. The other variables will be kept constant.

```python
import inductiva
import fluid_block

# Constant parameters for all simulations
DENSITY = 1e3  # in kg/m^3
TANK_DIMENSIONS = [1., 1., 1.]  # in meters
SIMULATION_TIME = 3.  # in seconds
PARTICLE_RADIUS = 0.008  # in meters
N_SIMULATIONS = 100
```

We assume the following ranges for the parameters we want to vary:
- position: each coordinate varies over $[0., 0.5]$;
- dimensions: this depends on the position and varies in the range $[0.05, `distance_to_wall`]$;
- velocity: each coordinate varies over $[-1., 1.]$;
- viscosity: varies over $[1e-6, 1e1]$.

Randomly varying over these parameters and submitting the simulations will be troublesome,
therefore we will launch now the 10 machines that we use to generate the dataset.
We will use the `inductiva` package to launch the machines.

```python
dataset_machines = inductiva.resources.MachineGroup(machine_type="c2-standard-4",
                                                    num_machines=10)

# Start your engines!
dataset_machines.start()
```

Now, we are ready to generate the dataset with a simple `for` loop. 

```python

dataset_tasks = []

# Create the simulation parameters
simulation_parameters = scenarios.SimulationParameters(
simulation_time=SIMULATION_TIME, particle_radius=PARTICLE_RADIUS)

for n in range(N_SIMULATIONS):

    # Randomly select the parameters
    position = np.random.uniform(low=[0., 0., 0.],
                                 high=[0.5, 0.5, 0.5],
                                 size=(3,))

    # Compute vector of distance to the walls
    wall_distance = TANK_DIMENSIONS - position

    dimensions = np.random.uniform(low=0.05, high=wall_distance, size=(3,))
    velocity = np.random.uniform(low=-1., high=1., size=(3,))
    viscosity = 10**np.random.uniform(low=-6., high=1.)  
    
    # Initialize the Block parameters
    block = models.FluidBlock(DENSITY, viscosity, dimensions, position,
                              velocity)

    # Create the scenario
    scenario = scenarios.FluidBlockSplishSplash(block)
    task = scenario.simulate(sim_params=simulation_parameters,
                             machine_group=dataset_machines)
    dataset_tasks.append(task)

```

All simulations are submitted with random block properties! 


### Manage your tasks

With all simulations submitted to your pool of machines, we can now monitor
their progress. The `dataset_tasks` list contains all tasks submitted to the machines.
With each task, we can check the status and wait for the simulation to finish before
downloading the results.

```python
for index, task in enumerate(dataset_tasks):
    # Wait for the task to finish
    task.wait()
    sim_name = "sim_" + str(index).zfill(4)
    output_directory = os.path.join("dataset", sim_name)

    if task.get_status() == "success":
        output_dir = task.download_outputs(output_dir=output_directory)
    else:
        print(f"Simulation {index} failed with {task.get_status()}.")
```

As each simulation finishes with success, we download the results to the dataset
directory on your local computer.

That is all: we have just generated a dataset of 100 simulations with different
parameters and with the simulations distributed over 10 machines!
Don't forget to terminate your machines, to avoid surprises:

```python
dataset_machines.terminate()
```