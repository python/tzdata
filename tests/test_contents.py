import sys

import pytest

try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources


def get_magic(zone_name):
    components = zone_name.split("/")
    package_name = ".".join(["tzdata.zoneinfo"] + components[:-1])
    resource_name = components[-1]

    with resources.open_binary(package_name, resource_name) as f:
        return f.read(4)


@pytest.mark.parametrize(
    "zone_name",
    [
        "Africa/Cairo",
        "Africa/Casablanca",
        "Africa/Lome",
        "America/Argentina/San_Luis",
        "America/Denver",
        "America/Los_Angeles",
        "America/New_York",
        "America/Thunder_Bay",
        "Antarctica/South_Pole",
        "Asia/Calcutta",
        "Asia/Damascus",
        "Asia/Seoul",
        "Atlantic/Reykjavik",
        "Australia/Perth",
        "Egypt",
        "Etc/GMT-9",
        "Europe/Dublin",
        "Europe/London",
        "Europe/Prague",
        "Hongkong",
        "Indian/Cocos",
        "Indian/Mayotte",
        "Mexico/BajaNorte",
        "Pacific/Guam",
        "Pacific/Kiritimati",
        "US/Eastern",
        "UTC",
    ],
)
def test_zone_valid(zone_name):
    """Test an assortment of hard-coded zone names.

    This test checks that the zone resource can be loaded and that it starts
    with the 4-byte magic indicating a TZif file.
    """
    magic = get_magic(zone_name)
    assert magic == b"TZif"


def test_no_posixrules():
    assert not resources.is_resource("tzdata.zoneinfo", "posixrules")


def test_load_zones(subtests):
    with resources.open_text("tzdata", "zones") as f:
        zones = [z.strip() for z in f]

    for zone in zones:
        with subtests.test(zone=zone):
            magic = get_magic(zone)
            assert magic == b"TZif"
