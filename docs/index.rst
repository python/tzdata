tzdata: Python package providing IANA time zone data
====================================================

This is a Python package containing ``zic``-compiled binaries for the IANA time
zone database. It is intended to be a fallback for systems that do not have
system time zone data installed (or don't have it installed in a standard
location), as a part of `PEP 615 <https://www.python.org/dev/peps/pep-0615/>`_

This repository generates a ``pip``-installable package, published on PyPI as
`tzdata <https://pypi.org/project/tzdata>`_.

Overview
--------

``tzdata`` is a *data-only* package, organized in such a way that its resources
are accessible via :mod:`importlib.resources` (or, in older versions of Python,
its backport `importlib_resources`_). Although ``importlib.resources`` or
equivalent is recommended, it is also possible to access the data via
:func:`pkgutil.get_data` as well.

.. TODO: Change ``zoneinfo`` to :mod:`zoneinfo` when 3.9 is released

It is primarily intended to be used by standard library's ``zoneinfo``
module (new in Python 3.9), but it is also available as a source for time zone
data for other time zone libraries. It is generally recommended that any time
zone libraries should attempt to use the system data before using the
``tzdata`` package, but some systems (notably Windows) do not deploy zoneinfo
binaries of this type, and so ``tzdata`` is necessary.

Contents
--------

The ``tzdata`` package provides the output of ``zic`` compilation (the
equivalent of something like ``/usr/share/zoneinfo``) under the
``tzdata.zoneinfo`` package unaltered. This includes the ``tzdata.zi`` file,
which is a compact text representation of the un-compiled time zone database.

The package organization looks something like this::

    src/tzdata
    ├── __init__.py
    ├── zoneinfo
    │   ├── __init__.py
    │   ├── Africa
    │   │   ├── __init__.py
    │   │   ├── Abidjan
    │   │   ├── Accra
    │   │   ├── …
    │   │   └── Windhoek
    │   ├── America
    │   │   ├── __init__.py
    │   │   ├── Adak
    │   │   ├── Anchorage
    │   │   ├── …
    │   │   └── Yellowknife
    │   ├── …
    │   ├── tzdata.zi
    │   ├── …
    │   ├── zone.tab
    │   └── Zulu
    └── zones

    21 directories, 623 files

In addition to the zoneinfo files, it also provides a small amount of extra
metadata about the time zones. The ``tzdata.zones`` file is a newline-delimited
file listing all the IANA keys for time zone files present in the
``tzdata.zoneinfo`` package. The version of the IANA data is provided as a
Python variable as ``tzdata.IANA_VERSION``.

Examples
--------

End users should generally **not** need to use this package directly and should
use a Python library  like :mod:`dateutil.tz` or `zoneinfo`_, like so:

.. code-block:: python

    # Python 3.9+
    from datetime import datetime
    from zoneinfo import ZoneInfo

    dt = datetime.now(ZoneInfo("America/New_York"))

For those writing time zone libraries, the recommended mechanism for access is
to open the relevant zoneinfo binaries with
:func:`importlib.resources.open_binary`, like so:

.. code-block:: python

    from importlib import resources

    # America/New_York
    with resources.open_binary("tzdata.zoneinfo.America", "New_York") as f:
        assert f.read(4) == b"TZif"

Note that the way this is organized, each folder in ``tzdata.zoneinfo`` is a
package with resources below it. An example function for converting IANA keys
to package names:

.. code-block:: python

    def iana_key_to_resource(key):
        package_loc, resource = key.rsplit("/", 1)
        package = "tzdata.zoneinfo." + package_loc.replace("/", ".")

        return package, resource

    assert iana_key_to_resource("America/New_York") == \
           ("tzdata.zoneinfo.America", "New_York")
    assert iana_key_to_resource("America/Indiana/Indianapolis") == \
           ("tzdata.zoneinfo.America.Indiana", "Indianapolis")

.. Links

.. _importlib_resources: https://importlib-resources.readthedocs.io/en/latest/
.. _zoneinfo: https://docs.python.org/3/library/zoneinfo.html

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   maintaining


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
