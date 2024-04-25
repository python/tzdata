tzdata: Python package providing IANA time zone data
====================================================

This is a **FORK** of the Python package containing ``zic``-compiled binaries for the IANA time
zone database. It is intended to be a fallback for systems that do not have
system time zone data installed (or don't have it installed in a standard
location), as a part of `PEP 615 <https://www.python.org/dev/peps/pep-0615/>`_

This repository generates a ``pip``-installable package, published on PyPI as
`tzdata <https://pypi.org/project/tzdata>`_.

For more information, see `the documentation <https://tzdata.readthedocs.io>`_.

----

This fork is done for myself and Syno DSM 7 to function with SickChill as only SLIM files were available.

The files to do this are in `src/tzdata <src/tzdata/DSM_task_scheduler.md>`_ folder and includes ZoneInfoDSM.sh bash file to link to scheduler and zip file of the required files.
