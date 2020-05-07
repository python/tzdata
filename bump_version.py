import argparse
import io
import pathlib

import parver

REPO_ROOT = pathlib.Path(__file__).parent
VERSION = REPO_ROOT / pathlib.Path("VERSION")


def get_current_version() -> parver.Version:
    with open(VERSION, "rt") as f:
        return parver.Version.parse(f.read().strip())


def write_version(version: parver.Version):
    with open(VERSION, "wt") as f:
        f.write(str(version))


def update_package_version(version: parver.Version):
    new_init = io.StringIO()
    version_set = False
    init = REPO_ROOT / "src" / "tzdata" / "__init__.py"
    with open(init, "rt") as f:
        for line in f:
            if not version_set and line.startswith("__version__"):
                line = f'__version__ = "{version}"\n'
                version_set = True
            new_init.write(line)

    if not version_set:
        raise ValueError("Version not found in __init__.py!")

    new_init.seek(0)

    with open(init, "wt") as f:
        f.write(new_init.read())


def bump_version(version: parver.Version, args) -> parver.Version:
    if args.release:
        return version.base_version()

    if args.dev:
        if args.to is not None:
            return version.replace(dev=args.to)
        else:
            return version.bump_dev()

    version = version.replace(dev=None)

    if args.post:
        if args.to is not None:
            return version.replace(post=args.to)
        else:
            return version.bump_post()

    if args.rc:
        if version.is_postrelease:
            version = version.replace(post=None)

        if args.to is not None:
            return version.replace(pre_tag="rc", pre=args.to)
        else:
            return version.bump_pre("rc")


def main(args):
    original_version = get_current_version()
    bumped_version = bump_version(original_version, args)

    print(f"{original_version} → {bumped_version}")
    if not args.dry_run:
        write_version(bumped_version)
        update_package_version(bumped_version)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manipulate the package version")

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("--rc", action="store_true", help="Bump the release candidate")
    group.add_argument("--dev", action="store_true", help="Bump the dev version")
    group.add_argument(
        "--release",
        action="store_true",
        help="Bump from release candidate / dev to release",
    )
    group.add_argument(
        "--post", action="store_true", help="Bump the post release version"
    )
    parser.add_argument(
        "--to",
        type=int,
        default=None,
        help="Set the specified component to a specific number",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what the new version will be without writing any files.",
    )

    args = parser.parse_args()

    if args.to is not None and args.release:
        raise ValueError("Cannot combine --to and --release")

    main(args)
