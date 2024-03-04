import inductiva

input_dir = "splishsplash-base-dir"

machine = inductiva.resources.MachineGroup("c3-standard-88", spot=True)
machine.start()

# Set simulation input directory
splishsplash = inductiva.simulators.SplishSplash()

task = splishsplash.run(input_dir=input_dir,
                        sim_config_filename="config.json", on=machine)

task.wait()
task.download_outputs()
