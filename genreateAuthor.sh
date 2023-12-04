#!/bin/bash

OUTPUT_FILE="AUTHORS"

echo "# The following people wrote this AirBnB_clone" > "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Use Git log to get a list of formatted names and email addresses from the commit history
git log --format='%aN <%aE>' | grep -v 'github.com' | sort -u >> "$OUTPUT_FILE"


echo "List of people contributed to this repo has been generated and saved to $OUTPUT_FILE"

