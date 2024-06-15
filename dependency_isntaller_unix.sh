#!/bin/bash

echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Check if installation was successful
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies."
    exit 1
else
    echo "Dependencies installed successfully."
fi
