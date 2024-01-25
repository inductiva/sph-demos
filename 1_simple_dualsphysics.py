"""Low-level example of running DualSPHysics with Inductiva's Python API."""
import inductiva

commands = [
    "gencase flow_cylinder flow_cylinder -save:all",
    "dualsphysics flow_cylinder flow_cylinder -dirdataout data -svres",
    "partvtk -dirin flow_cylinder/data -savevtk vtk/PartFluid -onlytype:+fluid",
]

# Initialize the Simulator
dualsphysics = inductiva.simulators.DualSPHysics()

# Run simulation with config files in the input directory
task = dualsphysics.run(input_dir="sph-example-dirs/simple-dualsphysics",
                        commands=commands)

task.wait()
task.download_outputs()
