#!/usr/bin/bash
set -e
VERSION=$(<VERSION)

echo "Tagging version $VERSION"
git tag -m "Version $VERSION" $VERSION || exit "Failed to tag!"
echo "Success"
