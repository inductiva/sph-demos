"""Post process SPH simulation outputs."""
import os

from absl import logging

from post_processing.utils import visualization


class SPHSimulationOutput:
    """Post process SPH simulation outputs."""

    def __init__(self, sim_output_path: str):
        """Initializes a `SimulationOutput` object.

        Args:
            sim_output_path: Path to simulation output files.
            """
        self.sim_output_dir = sim_output_path

    def render(self,
               virtual_display: bool = False,
               movie_path: str = "movie.mp4",
               fps: int = 10,
               color: str = "blue"):
        """Render the simulation as a movie.

        Args:
        fps: Number of frames per second to use in the movie. Renders a
            subset of the vtk files to create the movie.
            Default: 10.
        color: The color of the markers in the simulation.
          If None, the default color is used.
        """

        vtk_dir = os.path.join(self.sim_output_dir, "vtk")
        movie_path = os.path.join(self.sim_output_dir, movie_path)

        logging.info("Rendering movie to %s with %d fps.", movie_path, fps)
        visualization.create_movie_from_vtk(vtk_dir,
                                            movie_path,
                                            virtual_display=virtual_display,
                                            camera=[(3., 3., 2.), (0., 0., 0.),
                                                    (1., 1., 2.)],
                                            fps=fps,
                                            color=color)
