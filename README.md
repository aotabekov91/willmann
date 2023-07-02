# Willmann

It is a launcher that can run (almost) everything you need.

## Install

It requires the following package: [plugin](https://github.com/aotabekov91/plugin) You can also simply run a bash build command:

```bash
mkdir /tmp/willmann_code
cd /tmp/willmann_code

git clone https://github.com/aotabekov91/plugin
git clone https://github.com/aotabekov91/willmann

# Create a virtual environment
# python -m venv venv
# source venv/bin/activate

cd plugin
pip3 install -r requirements.txt .
cd ..

cd willmann
pip3 install -r requirements.txt .

cd $HOME
rm -rf /tmp/willmann_code
willmann
```

## Usage

The first run of the application will create a configuration folder in $HOME/.config/willmann. Initially, willmann comes only with a single mode, Moder. Moder just lists all available modes. So, initially it is going to empty. To call Moder, press Alt+m. To install modes, have a look at [modes](https://github.com/aotabekov91/willmann_modes). 

## Todos

* [ ] Run willmann with systemd at boot
* [ ] Remove i3 window size dependency
* [x] Factor out all modes in a separate git rep (except probably moder).
* [x] Implement a system-wide call shortcut, so that it does not depend on an i3 shortcut call.
