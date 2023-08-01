# Willmann

It is a launcher that can run (almost) everything you need. It is tested only on a machine running Arch linux.

## Install

It requires the following package: [plug](https://github.com/aotabekov91/plug) You can also simply run a bash build command:

```bash
mkdir /tmp/willmann_code
cd /tmp/willmann_code

git clone https://github.com/aotabekov91/plug
git clone https://github.com/aotabekov91/willmann

# Create a virtual environment
# python -m venv venv
# source venv/bin/activate

cd plug
pip3 install -r requirements.txt .
cd ..

# Remove previous willmann config files
# rm -rf $HOME/.config/willmann/config.ini
# Remove previous willmann modes 
# rm -rf $HOME/.config/willmann/modes
# rm -rf $HOME/.config/willmann

cd willmann
pip3 install -r requirements.txt .

cd $HOME
rm -rf /tmp/willmann_code
willmann
```

## Usage

$ willmann run # Run the app
$ willmann quit # Stop the app

The first run of the application will create a configuration folder in $HOME/.config/willmann. 
Moder. Moder lists all currently available modes. To call Moder, press Alt+m. 
To install modes, have a look at [modes](https://github.com/aotabekov91/willmann_modes). 

## Navigation

### Common

| Action              | Shortcut       |
| ------------------- | ----------     |
| Toggle command mode | .              |
| Hide window         | Escape, Ctrl+[ |
| Choose selection    | Enter, Ctrl+m  |
| Focus list field    | Ctrl+l         |
| Focus input field   | Ctrl+h         |
| Toggle input field  | Ctrl+i         |
| Move up             | Ctrl+k, Ctrl+p |
| Move down           | Ctrl+j, Ctrl+n |

### List field focused

| Action              | Shortcut   |
| ------------------- | ---------- |
| Move up             | k          |
| Move down           | j          |
| Choose selection    | m          |

### Command mode

Todo

## Generic mode

Todo

## Todos

* [ ] Run willmann with systemd at boot
* [ ] Remove i3 window size dependency
* [x] Factor out all modes in a separate git rep (except probably moder).
* [x] Implement a system-wide call shortcut, so that it does not depend on an i3 shortcut call.
