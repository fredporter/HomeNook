"""uHOME server package."""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _distribution_version

__all__ = ["__version__"]

try:
    # pyproject.toml is the single source of truth; an installed distribution
    # reports it through the package metadata, so the runtime version and the
    # wheel metadata cannot drift apart.
    __version__ = _distribution_version("uhome-server")
except PackageNotFoundError:  # source checkout that has not been installed
    __version__ = "0.1.0.dev0"
