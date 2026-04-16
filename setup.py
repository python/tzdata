import re
from pathlib import Path

from setuptools import setup
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

ROOT = Path(__file__).parent


def generate_sbom():
    version = (ROOT / "VERSION").read_text().strip()
    init_text = (ROOT / "src" / "tzdata" / "__init__.py").read_text()
    iana_version = re.search(r'IANA_VERSION\s*=\s*"([^"]+)"', init_text).group(1)
    template = (ROOT / "templates" / "sbom.cdx.json.in").read_text()
    return template.replace("%%PACKAGE_VERSION%%", version).replace(
        "%%IANA_VERSION%%", iana_version
    )


class bdist_wheel(_bdist_wheel):
    def write_wheelfile(self, wheelfile_base, *args, **kwargs):
        super().write_wheelfile(wheelfile_base, *args, **kwargs)
        (Path(wheelfile_base) / "sboms").mkdir(exist_ok=True)
        (Path(wheelfile_base) / "sboms" / "sbom.cdx.json").write_text(generate_sbom())


cmdclass = {"bdist_wheel": bdist_wheel}
setup(cmdclass=cmdclass)
