import os

import tzdata

REPO_ROOT = os.path.split(os.path.split(__file__)[0])[0]
VERSION_FILE = os.path.join(REPO_ROOT, "VERSION")


def test_version():
    with open(VERSION_FILE, "rt") as f:
        version_from_file = f.read()

    assert version_from_file == tzdata.__version__
