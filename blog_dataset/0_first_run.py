import inductiva

input_dir = "splishsplash-base-dir"

# Set simulation input directory
splishsplash = inductiva.simulators.SplishSplash()

task = splishsplash.run(input_dir=input_dir,
                        sim_config_filename="config.json")

task.wait()
task.download_outputs()
