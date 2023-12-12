# Smoothed Particle Hydrodynamics (SPH) via Inductiva API

[**Inductiva API**](https://github.com/inductiva/inductiva/tree/main) empowers users to run large-scale simulations. With a simple interface, users have access to several simulators and features that help manage complex simulation workflows. 

Here, we explore Smoothed Particle Hydrodynamics (SPH) with two simulators available via **Inductiva API** - [SplishSplash](https://github.com/inductiva/inductiva/wiki/SPlisHSPlasH) and [DualSPHysics](https://github.com/inductiva/inductiva/wiki/DualSPHysics). 

In this repository, we make a tour of **Inductiva API**:
- [Run a simulation](README.md#running-a-simulation);
- [Create a scenario](scenario/README.md);
- [Generate a dataset via scenario](dataset/README.md).

### Running a Simulation

For **power users** who know how to configure a specific simulator and prepare the respective simulation files, **Inductiva API** provides a simple interface to simulate on a large scale. Here, we demonstrate how to use two SPH simulators in **Inductiva API**.

##### SplishSplash

SplishSplash is simple to run and the simulator is simply configured via a few configuration files. The required one is a `.json` file that contains the parameters of the simulation. The others are extra input files that determine the geometry and properties of the objects and fluids in the simulation.

```python
import inductiva

input_dir = inductiva.utils.files.download_from_url(
    "https://storage.googleapis.com/inductiva-api-demo-files/"
    "splishsplash-input-example.zip", unzip=True)

# Set simulation input directory
splishsplash = inductiva.simulators.SplishSplash()

task = splishsplash.run(input_dir=input_dir,
                        sim_config_filename="config.json")

# Wait for the simulation to finish
task.wait()
task.download_outputs()
```

##### DualSPHysics

DualSPHysics has a more complex configuration and requires that users select the commands to be executed. The commands are defined in a list of dictionaries, where each dictionary contains the command to be executed and the prompts to be answered. The prompts are the questions that the simulator asks during the execution of the command. The main input file for this simulation is a `.xml` file that contains the parameters of the simulation. The others are extra input files that determine the geometry and properties of the objects and fluids in the simulation.

```python
import inductiva

# Download the configuration files into a folder
input_dir = inductiva.utils.files.download_from_url(
    "https://storage.googleapis.com/inductiva-api-demo-files/"
    "dualsph-duck-input-example.zip", unzip=True)

commands = [
    {"cmd": "gencase floating_duck floating_duck -save:all", "prompts": []},
    {"cmd": "dualsphysics -mdbc floating_duck floating_duck -dirdataout data -svres", "prompts": []},
    {"cmd": "boundaryvtk -loadvtk AutoActual -motiondata floating_duck/data -savevtk floating_duck/boundary/duck -onlytype:-all,floating", "prompts": []},
    {"cmd": "partvtk -dirin floating_duck/data -savevtk floating_duck/particles/PartAll", "prompts": []},
    {"cmd": "partvtk -dirin floating_duck/data -savevtk floating_duck/particles/PartFluidOut", "prompts": []},
    {"cmd": "isosurface -dirin floating_duck/data -saveiso floating_duck/Surface/surf", "prompts": []}]
    
task = simulator.run(input_dir="FloatingDuck",commands=commands)

# Initialize the Simulator
dualsphysics = inductiva.simulators.DualSPHysics()

# Run simulation with config files in the input directory
task = dualsphysics.run(input_dir=input_dir,
                        commands=commands)

task.wait()
task.download_outputs()
```

### Install

To start experimenting with these scenarios you need to clone the public GitHub repository

```bash
git clone https://github.com/inductiva/inductiva-sph-demos.git
```

and install the `inductiva` package and other extra dependencies that are useful for this scenario.

Install `inductiva` package:
```bash
pip install inductiva
```

Install extra dependencies from within the `inductiva-sph-demos`:
```bash
pip install -r requirements.txt
```

Notice, that to run visualizations you may be required to install `ffmpeg`, if it is not already installed in your setup. You can download it from
[here](https://ffmpeg.org/download.html), or if using Anaconda to manage the environment install it directly with `conda install -c conda-forge ffmpeg`.


To further learn about the `inductiva` package, check the [Inductiva API documentation](https://github.com/inductiva/inductiva/wiki).
