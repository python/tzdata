import os
import re

from setuptools import setup
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

ROOT = os.path.dirname(os.path.abspath(__file__))


def generate_sbom():
    with open(os.path.join(ROOT, "VERSION")) as f:
        version = f.read().strip()
    with open(os.path.join(ROOT, "src", "tzdata", "__init__.py")) as f:
        init_text = f.read()
    iana_version = re.search(r'IANA_VERSION\s*=\s*"([^"]+)"', init_text).group(1)
    with open(os.path.join(ROOT, "templates", "sbom.cdx.json.in")) as f:
        template = f.read()
    return template.replace("%%PACKAGE_VERSION%%", version).replace(
        "%%IANA_VERSION%%", iana_version
    )


class bdist_wheel(_bdist_wheel):
    def write_wheelfile(self, wheelfile_base, *args, **kwargs):
        _bdist_wheel.write_wheelfile(self, wheelfile_base, *args, **kwargs)
        sboms_dir = os.path.join(wheelfile_base, "sboms")
        if not os.path.isdir(sboms_dir):
            os.makedirs(sboms_dir)
        with open(os.path.join(sboms_dir, "sbom.cdx.json"), "w") as f:
            f.write(generate_sbom())


cmdclass = {"bdist_wheel": bdist_wheel}
setup(cmdclass=cmdclass)
