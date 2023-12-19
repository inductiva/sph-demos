"""Visualization utils to create movie from VTK files."""
import os
import tempfile
from typing import List, Optional

from absl import logging
import pyvista as pv
import moviepy.video.io.ImageSequenceClip as moviepy_io


def render(source_dir,
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

    vtk_dir = os.path.join(source_dir, "vtk")
    movie_path = os.path.join(source_dir, movie_path)

    logging.info("Rendering movie to %s with %d fps.", movie_path, fps)
    create_movie_from_vtk(vtk_dir,
                          movie_path,
                          virtual_display=virtual_display,
                          camera=[(3., 3., 2.), (0., 0., 0.), (1., 1., 2.)],
                          fps=fps,
                          color=color)


def create_movie_from_vtk(vtk_output_dir: str,
                          movie_path: str,
                          virtual_display: bool = True,
                          scalars: str = None,
                          scalar_limits: Optional[List[float]] = None,
                          camera=None,
                          color: str = "blue",
                          cmap: str = None,
                          fps: int = 10) -> None:
    """Creates movie from a series of vtk files.

    The order of the vtk file name determines the order with which they
    are rendered in the movie. For example, vtk file 'frame_001.vtk' will
    appear before 'frame_002.vtk'.

    Args:
        vtk_output_dir: Directory containing the vtk files.
        movie_path: Path to save the movie.
        virtual_display: Whether to use a virtual display to render
            the movie.
        scalar: Scalars used to “color” the mesh. Accepts a string name
            of an array that is present on the mesh or an array equal to
            the number of cells or the number of points in the mesh.
            Array should be sized as a single vector.
        scalar_bounds: Color bar range for scalars. Defaults to minimum
            and maximum of scalars array. Example: [-1, 2].
        objects: Object of pyvista.PolyData type describing the domain or
            an object inside.
        camera: Camera description must be one of the following:
          - List of three tuples describing the position, focal-point
          and view-up: [(2.0, 5.0, 13.0), (0.0, 0.0, 0.0), (-0.7, -0.5, 0.3)]
          - List with a view-vector: [-1.0, 2.0, -5.0]
          - A string with the plane orthogonal to the view direction: 'xy'.
          https://docs.pyvista.org/api/plotting/_autosummary/pyvista.CameraPosition.html
        color: Color of the points used to represent particles. Default: "blue".
        cmap: string with the name of the matplotlib colormap to use
            when mapping the scalars. See available Matplotlib colormaps.
        fps: Number of frames per second to use in the movie. Renders only a
            subset of the vtk files to create the movie. This is done for
            speed purposes.
            Default: 10.
    """
    if virtual_display:
        pv.start_xvfb()

    vtk_files = os.listdir(vtk_output_dir)
    frames = []

    plt = pv.Plotter(off_screen=True)
    plt.camera_position = camera

    with tempfile.TemporaryDirectory() as tmp_dir:
        for frame_file in vtk_files:
            frame_path = os.path.join(vtk_output_dir, frame_file)

            # frame_file = "ParticleData_Fluid_13.vtk" -> frame_index = 13
            frame_index = frame_file.split("_")[-1].split(".")[0]
            image_frame_path = os.path.join(
                tmp_dir, "frame_" + str(frame_index).zfill(5) + ".png")

            # Read mesh and create a snapshot with Pyvista
            mesh = pv.read(frame_path)
            plt.add_mesh(mesh,
                         name="fluid_block_snapshot",
                         scalars=scalars,
                         clim=scalar_limits,
                         render_points_as_spheres=True,
                         color=color,
                         cmap=cmap)
            plt.screenshot(image_frame_path, return_img=False)
            frames.append(image_frame_path)

        plt.close()

        # Sort frames and render the movie
        frames = sorted(frames)
        clip = moviepy_io.ImageSequenceClip(frames, fps=fps)
        clip.write_videofile(movie_path)
