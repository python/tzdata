#!/bin/sh
echo "DSM7 zoneinfo update"
/bin/pwd
echo $$
cd /usr/share/zoneinfo
/bin/7z x /volume1/Media/scripts/zonetimeinfo.zip -y
