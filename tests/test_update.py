import io
import pathlib
import sys
import tarfile

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import update


def _write_tarball(path, member_name, data):
    with tarfile.open(path, "w:gz") as tf:
        info = tarfile.TarInfo(member_name)
        info.size = len(data)
        tf.addfile(info, io.BytesIO(data))


def test_unpack_tzdb_tarballs_accepts_local_tarballs_without_signatures(tmp_path):
    download_dir = tmp_path / "2020a" / "download"
    download_dir.mkdir(parents=True)

    tzdata_tar = download_dir / "tzdata2020a.tar.gz"
    tzcode_tar = download_dir / "tzcode2020a.tar.gz"

    _write_tarball(tzdata_tar, "tzdata-file", b"tzdata")
    _write_tarball(tzcode_tar, "tzcode-file", b"tzcode")

    target_dir = update.unpack_tzdb_tarballs([tzdata_tar, tzcode_tar])

    assert target_dir == tmp_path / "2020a" / "tzdb"
    assert (target_dir / "tzdata-file").is_file()
    assert (target_dir / "tzcode-file").is_file()


def test_read_news_accepts_multi_letter_version(tmp_path):
    news_file = tmp_path / "NEWS"
    news_file.write_text(
        "Release 2030za - 2030-12-31 00:00:00 +0000\n"
        "\n"
        "Changes to data\n"
        "  - Example update\n"
    )

    news_entry = update.read_news(tmp_path, version="2030za")

    assert news_entry.version == "2030za"


def test_read_news_raises_for_empty_release_block(tmp_path):
    news_file = tmp_path / "NEWS"
    news_file.write_text("Release 2031a - 2031-01-01 00:00:00 +0000\n")

    with pytest.raises(ValueError, match="has no contents in NEWS file"):
        update.read_news(tmp_path, version="2031a")
