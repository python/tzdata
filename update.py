import dataclasses
import io
import itertools
import logging
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import textwrap
from collections.abc import Iterable, Iterator, Mapping, Sequence
from datetime import datetime, timezone

import click
import parver  # type: ignore
import requests

IANA_LATEST_LOCATION = "https://www.iana.org/time-zones/repository/tzdata-latest.tar.gz"
SOURCE = "https://data.iana.org/time-zones/releases"
WORKING_DIR = pathlib.Path("tmp")
REPO_ROOT = pathlib.Path(__file__).parent
PKG_BASE = REPO_ROOT / "src"
TEMPLATES_DIR = REPO_ROOT / "templates"

SKIP_NEWS_HEADINGS = {
    "Changes to code",
    "Changes to build procedure",
}


def download_tzdb_tarballs(
    version: str, base_url: str = SOURCE, working_dir: pathlib.Path = WORKING_DIR
) -> Sequence[pathlib.Path]:
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


def retrieve_local_tarballs(
    version: str, source_dir: pathlib.Path, working_dir: pathlib.Path = WORKING_DIR
) -> Sequence[pathlib.Path]:
    """Retrieve the tzdata and tzcode tarballs from a folder.

    This is useful when building against a local, patched version of tzdb.
    """
    tzdata_file = f"tzdata{version}.tar.gz"
    tzcode_file = f"tzcode{version}.tar.gz"

    target_dir = working_dir / version / "download"

    # mkdir -p target_dir
    target_dir.mkdir(parents=True, exist_ok=True)

    dest_locations = []

    for filename in [tzdata_file, tzcode_file]:
        source_location = source_dir / filename
        dest_location = target_dir / filename

        if dest_location.exists():
            logging.info("File %s exists, overwriting", dest_location)

        shutil.copy(source_location, dest_location)

        dest_locations.append(dest_location)

    return dest_locations


def unpack_tzdb_tarballs(
    download_locations: Sequence[pathlib.Path],
) -> pathlib.Path:
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
            ["tar", "-xf", os.fspath(tarball.absolute())],
            cwd=target_dir,
            check=True,
        )

    return target_dir


def load_zonefiles(
    base_dir: pathlib.Path,
) -> tuple[Sequence[str], pathlib.Path]:
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


def create_package(version: str, zonenames: Sequence[str], zoneinfo_dir: pathlib.Path):
    """Creates the tzdata package."""
    # Start out at rc0
    base_version = parver.Version.parse(translate_version(version))
    rc_version = base_version.replace(pre_tag="rc", pre=0)
    package_version = str(rc_version)

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

    with open(REPO_ROOT / "VERSION", "w") as f:
        f.write(package_version)

    # Generate the "zones" file as a newline-delimited list
    with open(target_dir / "zones", "w") as f:
        f.write("\n".join(zonenames))

    # Now recursively create __init__.py files in every directory we need to
    for dirpath, _, filenames in os.walk(data_dir):
        if "__init__.py" not in filenames:
            init_file = pathlib.Path(dirpath) / "__init__.py"
            init_file.touch()


def get_current_package_version() -> str:
    with open(PKG_BASE / "tzdata/__init__.py", "rt") as f:
        for line in f:
            if line.startswith("IANA_VERSION"):
                return line.split("=", 1)[1].strip(' "\n')

    raise ValueError("IANA version not found!")


def find_latest_version() -> str:
    r = requests.get(IANA_LATEST_LOCATION)
    fobj = io.BytesIO(r.content)
    with tarfile.open(fileobj=fobj, mode="r:gz") as tf:
        vfile = tf.extractfile("version")

        assert vfile is not None, "version file is not a regular file"
        version = vfile.read().decode("utf-8").strip()

    assert re.match(r"\d{4}[a-z]$", version), version

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


##
# News entry handling
@dataclasses.dataclass
class NewsEntry:
    version: str
    release_date: datetime
    categories: Mapping[str, str]

    def to_file(self) -> None:
        fpath = pathlib.Path("news.d") / (self.version + ".md")
        release_date = self.release_date.astimezone(timezone.utc)
        translated_version = translate_version(self.version)

        contents = [f"# Version {translated_version}"]
        contents.append(
            f"Upstream version {self.version} released {release_date.isoformat()}"
        )
        contents.append("")

        for category, entry in self.categories.items():
            contents.append(f"## {category}")
            contents.append("")
            contents.append(entry)
            contents.append("")

        with open(fpath, "wt") as f:
            f.write(("\n".join(contents)).strip())


INDENT_RE = re.compile("[^ ]")


def get_indent(s: str) -> int:
    s = s.rstrip()
    if not s:
        return 0

    m = INDENT_RE.search(s)
    assert m is not None
    return m.span()[0]


def read_block(
    lines: Iterator[str],
) -> tuple[Sequence[str], Iterator[str]]:
    lines, peek = itertools.tee(lines)
    while not (first_line := next(peek)):
        next(lines)

    block_indent = get_indent(first_line)
    block = []

    # The way this loop works: `peek` is always one line ahead of `lines`. It
    # starts out where `lines` is pointing to the first non-empty line, and
    # peek is the line after that. We know that if the body of the loop is
    # reached, the next value in `lines` is part of the block.
    #
    # It is done this way so that we can return an iterable pointing at the
    # first line *after* the block that we just read.
    for line in peek:
        block.append(next(lines))

        if not line:
            block.append(line)
            continue

        line_indent = get_indent(line)
        if line_indent < block_indent:
            # We've dedented, so this is the end of the block.
            break
    else:
        # If we've exhausted `peek` because we're reading the last block in the
        # file, we won't hit the `break` condition, but we'll still have a
        # valid line in the `lines` queue.
        block.append(next(lines))

    return block, lines


def parse_categories(news_block: Sequence[str]) -> Mapping[str, str]:
    blocks = iter(news_block)

    output = {}
    while True:
        try:
            while not (heading := next(blocks)):
                pass
        except StopIteration:
            break

        content_lines, blocks = read_block(blocks)

        heading = heading.strip()
        if heading in SKIP_NEWS_HEADINGS:
            continue

        # Merge the contents into paragraphs by grouping into consecutive blocks
        # of non-empty lines, then joining those lines on a newline.
        content_paragraphs: Iterable[str] = (
            "\n".join(paragraph)
            for _, paragraph in itertools.groupby(content_lines, key=bool)
        )

        # Now dedent each paragraph and wrap it to 80 characters. This needs to
        # be done at the per-paragraph level, because `textwrap.wrap` doesn't
        # recognize paragraph breaks.
        content_paragraphs = map(textwrap.dedent, content_paragraphs)
        content_paragraphs = map(
            "\n".join,
            (textwrap.wrap(paragraph, width=80) for paragraph in content_paragraphs),
        )

        # Finally we can join the paragraphs into a single string and trim
        # whitespace from it
        contents = "\n".join(content_paragraphs)
        contents = contents.strip()

        output[heading] = contents

    return output


def read_news(tzdb_loc: pathlib.Path, version: str | None = None) -> NewsEntry:
    release_re = re.compile(r"^Release (?P<version>\d{4}[a-z]) - (?P<date>.*$)")
    with open(tzdb_loc / "NEWS", "rt") as f:
        f_lines = map(str.rstrip, f)
        for line in f_lines:
            if ((m := release_re.match(line)) is not None) and (
                version is None or m.group("version") == version
            ):
                break
        else:
            if version is None:
                message = "No releases found!"
            else:
                message = f"No release found with version {version}"

        assert m is not None
        version_date = datetime.strptime(m.group("date"), "%Y-%m-%d %H:%M:%S %z")
        release_version = m.group("version")
        release_contents, _ = read_block(f_lines)

    # Now we further parse the contents of the news and filter out some
    # irrelevant categories.
    categories = parse_categories(release_contents)

    return NewsEntry(release_version, version_date, categories)


def update_news(news_entry: NewsEntry):
    # news.d contains fragments for each tzdata version, and the NEWS file
    # is assembled by stitching these together each time. First thing we'll do
    # is add a new fragment.
    news_entry.to_file()

    # Now go through and join all the files together
    news_fragment_files = sorted(
        pathlib.Path("news.d").glob("*.md"), key=lambda p: p.name, reverse=True
    )

    news_fragments = [p.read_text() for p in news_fragment_files]

    with open("NEWS.md", "wt") as f:
        f.write("\n\n---\n\n".join(news_fragments))


@click.command()
@click.option(
    "--version", "-v", default=None, help="The version of the tzdata file to download"
)
@click.option(
    "--source-dir",
    "-s",
    default=None,
    help="A local source directory containing tarballs (must be used together with --version)",
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True, path_type=pathlib.Path
    ),  # type: ignore
)
@click.option(
    "--news-only/--no-news-only",
    help="Flag to disable data updates and only update the news entry",
)
@click.option(
    "--skip-existing/--no-skip-existing",
    default=True,
    help="Whether to skip the update if we're already at the current value.",
)
def main(
    version: str | None,
    news_only: bool,
    skip_existing: bool,
    source_dir: pathlib.Path | None,
):
    logging.basicConfig(level=logging.INFO)

    if skip_existing:
        existing_version: str | None = get_current_package_version()
    else:
        existing_version = None

    if version is None or version != existing_version:
        if source_dir is not None:
            if version is None:
                logging.error(
                    "--source-dir specified without --version: "
                    "If using --source-dir, --version must also be used."
                )
                sys.exit(-1)
            download_locations: Sequence[pathlib.Path] | None = retrieve_local_tarballs(
                version, source_dir
            )
        else:
            if version is None:
                version = find_latest_version()

            if version != existing_version or not skip_existing:
                download_locations = download_tzdb_tarballs(version)
            else:
                download_locations = None
    else:
        download_locations = None

    if skip_existing and version == existing_version:
        logging.info(
            f"Selected version {version} is identical "
            f"to existing version {existing_version}; nothing to do!"
        )
        sys.exit(0)

    assert download_locations is not None
    tzdb_location = unpack_tzdb_tarballs(download_locations)

    # Update the news entry
    news_entry = read_news(tzdb_location, version=version)
    update_news(news_entry)

    if not news_only:
        zonenames, zonefile_path = load_zonefiles(tzdb_location)
        create_package(version, zonenames, zonefile_path)


if __name__ == "__main__":
    main()
