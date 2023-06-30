#!/usr/bin/bash

# Create a virtual environment for willmann
python -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Get and install :plugin:
git clone https://github.com/aotabekov91/plugin
cd plugin; pip install -r requirements; cd ..

# Get and install :tables:
git clone https://github.com/aotabekov91/tables
cd tables; pip install -r requirements; cd ..

# Get and install :willmann:
pip install -r requirements
