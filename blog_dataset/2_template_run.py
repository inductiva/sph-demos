import inductiva
from inductiva import mixins

# Launch a machine group with a c2-standard-30
machine_group = inductiva.resources.MachineGroup("c2-standard-60")
machine_group.start()

# Download the input files mentioned above
input_dir = "splishsplash-template-dir"

# Set the honey properties at room temperature and the initial velocity
honey_density = 2500 # kg/m^3
honey_kinematic_viscosity = 2 # m^2/s
initial_velocity = [4, 0, 0] # m/s

# Initialize the simulator and run the simulation
splishsplash = inductiva.simulators.SplishSplash()

# Initialize the templating engine
file_manager = mixins.FileManager()
file_manager.set_root_dir("splishsplash-honey")
file_manager.add_dir(input_dir,
                     density=honey_density,
                     viscosity=honey_kinematic_viscosity,
                     initial_velocity=initial_velocity)

task = splishsplash.run(
    input_dir=file_manager.get_root_dir(),
    sim_config_filename="config.json",
    on=machine_group)

# Wait for the simulation to finish and Download all generated output files
task.wait()
task.download_outputs()
