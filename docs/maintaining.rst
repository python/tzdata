Maintainer's Guide
==================

The ``tzdata`` repo is intended to be very low-maintenance and highly
automated. This document serves as a reference guide for various maintenance
actions that a maintainer may need to take. End users do not need to be
concerned with the contents of this document.

Requirements
------------

Maintenance scripts are orchestrated using |tox|_ environments to manage the
requirements of each script. The details of each environment can be found in
the ``tox.ini`` file in the repository root.

The repository also has pre-commit configured to automatically enforce various
code formatting rules on commit. To use it, install `pre-commit
<https://pre-commit.com/>`_ and run ``pre-commit install`` in the repository
root to install the git commit hooks.

Updating to new tz releases
---------------------------

When the ``update`` environment is run, it will automatically detect whether
the current version of the IANA time zone database in the repository matches
the latest release available from `iana.org
<https://www.iana.org/time-zones>`_. If a new release is available, ``tox -e
update`` will download and install it into the repository.

After running ``tox -e update``, the base version should be set to the current
version of the upstream database, translated into :pep:`440`. The package
version will start as a release candidate (``rc0``), and will need to be bumped
to a full release before the final upload to PyPI. For example, when updating
from 2019c to 2020a::

    $ tox -e update -- --version=2020a
    ...
    $ git diff VERSION
    -2019.3
    +2020.1rc0

Once this is done, commit all the changed or added files and make a pull
request.

Updating the version
--------------------

The canonical location for the version is the ``VERSION`` file in the
repository root, and it is updated in two ways:

1. The "base version" (e.g. 2020.1) is set by ``tox -e update``.
2. The additional markers such as pre (release candidate), post and dev are
   managed by ``tox -e bump_version``.

The version follows the scheme::

    YYYY.minor[rcX][.postY][.devZ]

Bumping any component removes all values to its right as well, so for example,
if the base version were ``20201rc1.post2.dev0``::

    $ tox -e bump -- --dev --dry-run
    ...
    2020.1rc1.post2.dev0 → 2020.1rc1.post2.dev1

    $ tox -e bump -- --post --dry-run
    ...
    2020.1rc1.post2.dev0 → 2020.1rc1.post3

    $ tox -e bump -- --rc --dry-run
    ...
    2020.1rc1.post2.dev0 → 2020.1rc2

To remove all additional markers and get a simple "release" version, use
``--release``::

    $ tox -e bump -- --release
    ...
    2020.1rc1.post2.dev0 → 2020.1

For more information on how to use ``bump_version``, run ``tox -e bump_version
-- -help``.

.. Links
.. |tox| replace:: ``tox``
.. _tox: https://tox.readthedocs.io/en/latest/
