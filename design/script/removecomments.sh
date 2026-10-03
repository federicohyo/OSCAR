#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 inputfile outputfile"
    exit 1
fi

# Assign input and output file arguments to variables
inputfile="$1"
outputfile="$2"

# Read the input file and remove lines starting with "*", then write to output file
grep -v '^\*' "$inputfile" > "$outputfile"

# Print a message indicating that the process is complete
echo "Comments removed and content copied to $outputfile"
