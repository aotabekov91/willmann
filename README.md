# Willmann

It is a launcher that can run (almost) everything you need.

## Install

It requires the following package: 

1. [plugin](https://github.com/aotabekov91/plugin)
2. [tables](https://github.com/aotabekov91/tables)

Also, depending on which modes you use, you need:

1. [flashcard]()
2. [translate]()

After installing all required custom packages, run pip3 install -r requirements. It is advised first to try the application in a separate virtual enviroment. 

You can also simply run a bash build command:

```bash
git clone willmann
cd willmann
chmod +x build.sh
./build.sh
```

## Usage

### Run an application

### Look up a definition 

### Change keyboard layout

### Player control

### Bookmark create/search

### Etc.

## How to extend [i.e., creating a new mode]

Say, you want to quickly search for country-specific information [e.g., its population, location on the map, etc]. Then, you can do the following:

1. Parse needed information from the wikipedia [and probably save it in a sqlite/postgresql database using tables so that the first step is done only once]
  * I leave this step to you [not difficult but boring]
  * Assume you have the following list of dicts with country data:
  * dlist=[{'name':'Laconia', 'population': 10000000, 'flag':image_url, 'anthem':audio_url, 'etc':'etc'}, {'name': 'Auberon', 'population':100, 'flag':image_url, 'anthem':audio_url, 'etc':'etc'}

2. Create a new mode that displays this info

### 1st stage

Todo

### 2nd stage

Todo

```python
```

## Todos

* [ ] Upload flashcard package
* [ ] Upload translate package
* [ ] Remove i3 window size dependency
* [ ] Implement a system-wide call shortcut, so that it does not depend on an i3 shortcut call.
* [ ] Factor out all modes in a separate git rep (except probably moder).
