#!/bin/bash

# Exit if any command fails
set -e

# Create virtual environment named 'venv' if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment 'venv'..."
    python3 -m venv venv
else
    echo "Virtual environment 'venv' already exists."
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install required packages
echo "Installing required packages..."
pip install \
    blinker \
    certifi \
    charset-normalizer \
    click \
    Flask \
    idna \
    itsdangerous \
    Jinja2 \
    MarkupSafe \
    pystun3 \
    requests \
    urllib3 \
    sseclient \
    Werkzeug \
    cryptography

echo "All packages installed successfully."
