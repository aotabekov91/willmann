#!/usr/bin/bash

# Create a virtual environment for willmann
python -m venv .willman_env

# Activate the virtual environment
source .willmann_env/bin/activate

# Get and install :plugin:
git clone https://github.com/aotabekov91/plugin
cd plugin; pip install -r requirements; cd ..

# Get and install :tables:
git clone https://github.com/aotabekov91/tables
cd plugin; pip install -r requirements; cd ..

# Get and install :willmann:
git clone https://github.com/aotabekov91/willmann
cd plugin; pip install -r requirements; cd ..
