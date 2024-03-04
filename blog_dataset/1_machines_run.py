import inductiva

# Configure and start a dedicated machine group
my_machine_group = inductiva.resources.MachineGroup(
    machine_type="c2-standard-60")
my_machine_group.start()

input_dir = "splishsplash-base-dir"

splishsplash = inductiva.simulators.SplishSplash()

task = splishsplash.run(input_dir=input_dir,
                        sim_config_filename="config.json",
                        on=my_machine_group)

task.wait()
task.download_outputs()

# Terminate the machine group
my_machine_group.terminate()