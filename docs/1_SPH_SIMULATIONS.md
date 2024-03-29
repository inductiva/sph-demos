## Running an SPH Simulation

This section assumes users know how to configure a SplishSplash and/or DualSPHysics
simulation, in which case our **Inductiva API client** provides a simple
interface to run those simulations at scale. Users are, in any case, invited to
consult the relevant documentation for each of those simulation engines (links
[here](https://github.com/InteractiveComputerGraphics/SPlisHSPlasH) and
[here](https://github.com/DualSPHysics/DualSPHysics), respectively). 

Let's demonstrate how to use two SPH simulators with **Inductiva API**.

### Falling fluid block with [SplishSplash](https://github.com/InteractiveComputerGraphics/SPlisHSPlasH)

This example uses a straightforward call to SplishSplash via **Inductiva API**
to simulate a cube of fluid falling under the effect of gravity.
The simulator is configured with a `config.json` containing the configuration
parameters of the simulation and with a `unit_box.obj` file defining the geometry
on a unit cube (used to describe the shape of both the falling fluid cube and
container box).

All input files are within the `sph-example-dirs/simple-splishsplash` folder,
which gets passed to the `run` method of a `SPlisHSPlasH` instance, along with
the name of the file configuring the simulation.

Simulations are submitted as tasks to the queue of a remote default pool of
machines.
Hence, the user needs to wait for the task to finish before retrieving the output
files generated by the simulator. The following snippets exemplify how this flow
can be achieved.

1. Inspect the content of the input folder for this simulation:

```bash
$ ls -l1 sph-demos/simple-splishsplash
config.json
unit_box.obj
```

2. Inspect the python script:

```bash
$ cat simple_splishsplash.py
import inductiva

# Initialize a SPlisHSPlasH proxy
splishsplash = inductiva.simulators.SplishSplash()

# Submit the task to the default resource pool
task = splishsplash.run(input_dir="sph-example-dirs/simple-splishsplash",
                        sim_config_filename="config.json")

# Wait for the simulation to finish and Download all generated output files
task.wait()
task.download_outputs()
```

3. Running the Python script, you should see logs similar to the following:

```bash
$ python simple_splishsplash.py
2023-12-20 14:51:06 INFO Task ID: 1703083865802376474
2023-12-20 14:51:06 INFO Packing input archive to upload to inductiva.ai.
2023-12-20 14:51:06 INFO Uploading packed input archive with size 1.07 KB.
2023-12-20 14:51:06 INFO Input archive uploaded.
2023-12-20 14:51:06 INFO Task submitted to the default resource pool.
2023-12-20 14:51:21 INFO Task completed successfully.

2023-12-20 14:51:30 INFO Downloading simulation outputs to inductiva_output/1703083865802376474/output.zip.
100%|██████████████████████| 261k/261k [00:00<00:00, 5.15MB/s]
2023-12-20 14:51:31 INFO Uncompressing the outputs to inductiva_output/1703083865802376474.
```

Note that the task ID for your simulation will be different from the one shown
above. Therefore, copy it and use it in the next step.

4. Check the outputs of the simulation in `inductiva_output/{TASK_ID}`:

```bash
$ ls -l1 inductiva_output/{TASK_ID}
log
stderr.txt
stdout.txt
vtk
```

### Flow over Cylinder with [DualSPHysics](https://github.com/DualSPHysics/DualSPHysics)

For this example, we use the same approach as before, but with a different
simulator. In this case, we make a call to DualSPHysics via **Inductiva API** to
simulate the fluid flow over a cylinder in 2D. The simulator is configured with
a single `.xml` file containing both the simulation parameters and a description
of the geometry.

DualSPHysics uses multiple commands to prepare, run and post-process a simulation.
These commands are set by us in a list of dictionaries, where each dictionary
contains the command to be executed and possible simulator prompts to be
answered. 
The input file for this simulation is within the `sph-demos/simple-dualsphysics`
folder. This folder is passed to the `run` method of a `DualSPHysics` instance
together with the list of commands to be executed.

The following snippets exemplify how this flow can be achieved.

1. Inspect the content of the input folder for this simulation:

```bash
$ ls -l1 sph-example-dirs/simple-dualsphysics
flow_cylinder.xml
```

2. Inspect the python script:

```bash
$ cat simple_dualsphysics.py
import inductiva

commands = [
    "gencase flow_cylinder flow_cylinder -save:all",
    "dualsphysics flow_cylinder flow_cylinder -dirdataout data -svres",
    "partvtk -dirin flow_cylinder/data -savevtk vtk/PartFluid -onlytype:+fluid"
    ]

# Initialize the Simulator
dualsphysics = inductiva.simulators.DualSPHysics()
# Run simulation with config files in the input directory
task = dualsphysics.run(input_dir="sph-example-dirs/simple-dualsphysics",
                        commands=commands)

task.wait()
task.download_outputs()
```

3. Running the Python script, you should see logs similar to the ones for
DualSPHysics. Copy the Task ID and use it in the next step.

4. Check the outputs of the simulation in `inductiva_output/{TASK_ID}`:

```bash
$ ls -l1 inductiva_output/{TASK_ID}
flow_cylinder
flow_cylinder.bi4
flow_cylinder.out
flow_cylinder.xml
flow_cylinder_All.vtk
flow_cylinder_Bound.vtk
flow_cylinder_Fluid.vtk
flow_cylinder_MkCells.vtk
flow_cylinder__Dp.vtk
stderr.txt
stdout.txt
vtk
```


**Inductiva API** is all you need to run SPH simulations at scale.
Now submit your simulations!
