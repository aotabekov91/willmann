# Willmann

It is a launcher that can run (almost) everything you need. It is tested only on a machine running Arch linux.

## Install

TODO

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
