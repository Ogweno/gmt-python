"""
The main API for GMT/Python.

Functions and classes from ``gmt`` package offer access to GMT with input and
output of Python data types.
All plotting is handled through the :class:`gmt.Figure` class.

All of GMT/Python is operated on a "modern mode session" (new to GMT6). When
you import the ``gmt`` library, a new session will be started automatically.
The session will be closed when the current Python process terminates. Thus,
the Python API does not expose the ``gmt begin`` and ``gmt end`` commands.
"""
import atexit as _atexit

from ._version import get_versions as _get_versions

# Import modules to make the high-level GMT Python API
from .session_management import begin as _begin, end as _end
from .figure import Figure
from .modules import info, which


# Get the version number through versioneer
__version__ = _get_versions()['version']
__commit__ = _get_versions()['full-revisionid']

# Start our global modern mode session
_begin()
# Tell Python to run _end when shutting down
_atexit.register(_end)


def print_libgmt_info():
    """
    Print information about the currently loaded GMT shared library.

    Includes the GMT version, default values for parameters, the path to the
    ``libgmt`` shared library, and GMT directories.
    """
    import shutil
    from .clib import LibGMT

    columns = shutil.get_terminal_size().columns
    title = "Currently loaded libgmt"
    left = (columns - len(title) - 2)//2
    right = left + (columns - (2*left + len(title) + 2))
    header = ' '.join(['='*left, title, '='*right])

    with LibGMT() as lib:
        lines = [header]
        for key in sorted(lib.info):
            lines.append('{}: {}'.format(key, lib.info[key]))
    print('\n'.join(lines))


def test(doctest=True, verbose=True, coverage=False, figures=True):
    """
    Run the test suite.

    Uses `py.test <http://pytest.org/>`__ to discover and run the tests. If you
    haven't already, you can install it with `conda
    <http://conda.pydata.org/>`__ or `pip <https://pip.pypa.io/en/stable/>`__.

    Parameters
    ----------

    doctest : bool
        If ``True``, will run the doctests as well (code examples that start
        with a ``>>>`` in the docs).
    verbose : bool
        If ``True``, will print extra information during the test run.
    coverage : bool
        If ``True``, will run test coverage analysis on the code as well.
        Requires ``pytest-cov``.
    figures : bool
        If ``True``, will test generated figures against saved baseline
        figures.  Requires ``pytest-mpl`` and ``matplotlib``.

    Raises
    ------

    AssertionError
        If pytest returns a non-zero error code indicating that some tests have
        failed.

    """
    import pytest

    print_libgmt_info()

    args = []
    if verbose:
        args.append('-vv')
    if coverage:
        args.append('--cov=gmt')
        args.append('--cov-report=term-missing')
    if doctest:
        args.append('--doctest-modules')
    if figures:
        args.append('--mpl')
    args.append('--pyargs')
    args.append('gmt')
    status = pytest.main(args)
    assert status == 0, "Some tests have failed."
