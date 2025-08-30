#!/bin/bash

# Add all changes to git
git add .

# Prompt for a commit message
echo "Enter commit message: "
read commitMessage

# Commit the changes with the provided message
git commit -m "$commitMessage"

# Push to the master branch on the origin remote
git push origin master