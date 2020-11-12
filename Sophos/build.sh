#!/bin/bash

echo "Cleaning Up..."
rm -fv Forescout-sophos.zip
echo "Removing .DS_Store files..."
find . -name .DS_Store -delete
echo "Creating zip archive..."
zip -r Forescout-sophos.zip Sophos/