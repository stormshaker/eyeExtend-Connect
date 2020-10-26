#!/bin/bash

echo "Cleaning Up..."
rm -fv Forescout-nutanix.zip
echo "Removing .DS_Store files..."
find . -name .DS_Store -delete
echo "Creating zip archive..."
zip -r Forescout-nutanix.zip Nutanix/

