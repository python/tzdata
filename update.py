import io
import logging
import os
import pathlib
import re
import shutil
import subprocess
import tarfile
import tempfile
import typing

import click

import requests

IANA_LATEST_LOCATION = "https://www.iana.org/time-zones/repository/tzdata-latest.tar.gz"
SOURCE = "https://data.iana.org/time-zones/releases"
WORKING_DIR = pathlib.Path("tmp")
REPO_ROOT = pathlib.Path(__file__).parent
PKG_BASE = REPO_ROOT / "src"
TEMPLATES_DIR = REPO_ROOT / "templates"


def download_tzdb_tarballs(
    version: str, base_url: str = SOURCE, working_dir: pathlib.Path = WORKING_DIR
) -> typing.List[pathlib.Path]:
    """Download the tzdata and tzcode tarballs."""
    tzdata_file = f"tzdata{version}.tar.gz"
    tzcode_file = f"tzcode{version}.tar.gz"

    target_dir = working_dir / version / "download"
    # mkdir -p target_dir
    target_dir.mkdir(parents=True, exist_ok=True)

    download_locations = []
    for filename in [tzdata_file, tzcode_file]:
        download_location = target_dir / filename
        download_locations.append(download_location)

        if download_location.exists():
            logging.info("File %s already exists, skipping", download_location)
            continue

        url = f"{base_url}/{filename}"
        logging.info("Downloading %s from %s", filename, url)

        r = requests.get(url)
        with open(download_location, "wb") as f:
            f.write(r.content)

    return download_locations


def unpack_tzdb_tarballs(download_locations: typing.List[pathlib.Path]) -> pathlib.Path:
    assert len(download_locations) == 2
    assert download_locations[0].parent == download_locations[1].parent
    base_dir = download_locations[0].parent.parent
    target_dir = base_dir / "tzdb"

    # Remove the directory and re-create it if it does not exist
    if target_dir.exists():
        shutil.rmtree(target_dir)

    target_dir.mkdir()

    for tarball in download_locations:
        logging.info("Unpacking %s to %s", tarball, target_dir)
        subprocess.run(
            ["tar", "-xf", os.fspath(tarball.absolute())], cwd=target_dir, check=True,
        )

    return target_dir


def load_zonefiles(
    base_dir: pathlib.Path,
) -> typing.Tuple[typing.List[str], pathlib.Path]:
    target_dir = base_dir.parent / "zoneinfo"
    if target_dir.exists():
        shutil.rmtree(target_dir)

    with tempfile.TemporaryDirectory() as td:
        td_path = pathlib.Path(td)

        # First run the makefile, which does all kinds of other random stuff
        subprocess.run(
            ["make", f"DESTDIR={td}", "ZFLAGS=-b slim", "install"],
            cwd=base_dir,
            check=True,
        )

        proc = subprocess.run(
            ["make", "zonenames"], cwd=base_dir, stdout=subprocess.PIPE, check=True
        )
        zonenames = list(map(str.strip, proc.stdout.decode("utf-8").split("\n")))

        # Move the zoneinfo files into the target directory
        src_dir = td_path / "usr" / "share" / "zoneinfo"
        shutil.move(os.fspath(src_dir), os.fspath(target_dir))

    return zonenames, target_dir


def create_package(
    version: str, zonenames: typing.List[str], zoneinfo_dir: pathlib.Path
):
    """Creates the tzdata package."""
    package_version = translate_version(version)

    # First remove the existing package contents
    target_dir = PKG_BASE / "tzdata"
    if target_dir.exists():
        shutil.rmtree(target_dir)

    data_dir = target_dir / "zoneinfo"

    # Next move the zoneinfo file to the target location
    shutil.move(os.fspath(zoneinfo_dir), data_dir)

    # Generate the base __init__.py from a template
    with open(TEMPLATES_DIR / "__init__.py.in", "r") as f_in:
        contents = f_in.read()
        contents = contents.replace("%%IANA_VERSION%%", f'"{version}"')
        contents = contents.replace("%%PACKAGE_VERSION%%", f'"{package_version}"')

        with open(target_dir / "__init__.py", "w") as f_out:
            f_out.write(contents)

    # Generate the "zones" file as a newline-delimited list
    with open(target_dir / "zones", "w") as f:
        f.write("\n".join(zonenames))

    # Now recursively create __init__.py files in every directory we need to
    for dirpath, _, filenames in os.walk(data_dir):
        if "__init__.py" not in filenames:
            init_file = pathlib.Path(dirpath) / "__init__.py"
            init_file.touch()


def find_latest_version() -> str:
    r = requests.get(IANA_LATEST_LOCATION)
    fobj = io.BytesIO(r.content)
    with tarfile.open(fileobj=fobj, mode="r:gz") as tf:
        vfile = tf.extractfile("version")

        assert vfile is not None, "version file is not a regular file"
        version = vfile.read().decode("utf-8").strip()

    assert re.match("\d{4}[a-z]$", version), version

    target_dir = WORKING_DIR / version / "download"
    target_dir.mkdir(parents=True, exist_ok=True)

    fobj.seek(0)
    with open(target_dir / f"tzdata{version}.tar.gz", "wb") as f:
        f.write(fobj.read())

    return version


def translate_version(iana_version: str) -> str:
    """Translates from an IANA version to a PEP 440 version string.

    E.g. 2020a -> 2020.1
    """

    if (
        len(iana_version) < 5
        or not iana_version[0:4].isdigit()
        or not iana_version[4:].isalpha()
    ):
        raise ValueError(
            "IANA version string must be of the format YYYYx where YYYY represents the "
            f"year and x is in [a-z], found: {iana_version}"
        )

    version_year = iana_version[0:4]
    patch_letters = iana_version[4:]

    # From tz-link.html:
    #
    # Since 1996, each version has been a four-digit year followed by
    # lower-case letter (a through z, then za through zz, then zza through zzz,
    # and so on).
    if len(patch_letters) > 1 and not all(c == "z" for c in patch_letters[0:-1]):
        raise ValueError(
            f"Invalid IANA version number (only the last character may be a letter "
            f"other than z), found: {iana_version}"
        )

    final_patch_number = ord(patch_letters[-1]) - ord("a") + 1
    patch_number = (26 * (len(patch_letters) - 1)) + final_patch_number

    return f"{version_year}.{patch_number:d}"


@click.command()
@click.option(
    "--version", "-v", default=None, help="The version of the tzdata file to download"
)
def main(version: str):
    logging.basicConfig(level=logging.INFO)

    if version is None:
        version = find_latest_version()

    download_locations = download_tzdb_tarballs(version)
    tzdb_location = unpack_tzdb_tarballs(download_locations)

    zonenames, zonefile_path = load_zonefiles(tzdb_location)

    create_package(version, zonenames, zonefile_path)


if __name__ == "__main__":
    main()
