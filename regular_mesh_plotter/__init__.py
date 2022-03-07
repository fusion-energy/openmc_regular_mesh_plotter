try:
    from importlib.metadata import version, PackageNotFoundError
except (ModuleNotFoundError, ImportError):
    from importlib_metadata import version, PackageNotFoundError
try:
    __version__ = version("paramak")
except PackageNotFoundError:
    from setuptools_scm import get_version

    __version__ = get_version(root="..", relative_to=__file__)

__all__ = ["__version__"]

from .core import plot_regular_mesh_values
from .core import plot_regular_mesh_values_with_geometry

from .core import plot_regular_mesh_tally
from .core import plot_regular_mesh_tally_with_geometry

from .core import plot_regular_mesh_dose_tally
from .core import plot_regular_mesh_dose_tally_with_geometry

from .utils import reshape_values_to_mesh_shape
from .utils import get_tally_extent
from .utils import get_values_from_tally
from .utils import get_std_dev_or_value_from_tally
