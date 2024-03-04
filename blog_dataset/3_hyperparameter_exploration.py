import inductiva
from inductiva import mixins

# Launch a machine group with a c2-standard-30
machine_group = inductiva.resources.MachineGroup("c2-standard-60", num_machines=3)
machine_group.start()

# Download the input files mentioned above
input_dir = "splishsplash-hyperparameter-dir"

# Set the honey properties at room temperature and the initial velocity
particle_radius = [0.008, 0.006, 0.004]

# Initialize the simulator and run the simulation
splishsplash = inductiva.simulators.SplishSplash()

tasks_list = []

# Initialize the templating engine
file_manager = mixins.FileManager()
for radius in particle_radius:
    file_manager.set_root_dir("splishsplash-hyperparameter-search")
    file_manager.add_dir(input_dir,
                         particle_radius=radius)

    task = splishsplash.run(
        input_dir=file_manager.get_root_dir(),
        sim_config_filename="config.json",
        on=machine_group)
    tasks_list.append(task)
