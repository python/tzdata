#!/usr/bin/bash
set -e
VERSION=$(<VERSION)

echo "Tagging version $VERSION"
git tag -s -m "Version $VERSION" $VERSION || exit "Failed to tag!"
echo "Success"
