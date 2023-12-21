"""Low-level example of running SPlisHSPlasH with Inductiva's Python API."""
import inductiva

# Initialize a SPlisHSPlasH proxy
splishsplash = inductiva.simulators.SplishSplash()

# Submit the task to the default resource pool
task = splishsplash.run(input_dir="sph-example-dirs/simple-splishsplash",
                        sim_config_filename="config.json")

# Wait for the simulation to finish and Download all generated output files
task.wait()
task.download_outputs()
