"""X-CAVATE: Convert vascular network geometries into collision-free 3D printer toolhead pathways."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("xcavate")
except PackageNotFoundError:  # running from a source tree without install
    __version__ = "2.1.0"
