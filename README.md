# Macgyver-maze

## Overview
macgyver-maze is a python application game where the player is the famous MacGyver, lost inside a maze. 

The exit is protected by a guardian and MacGyver needs to bypass him in order to escape. To do this, MacGyver 
must combine three components (a plastic tube, a needle and a bottle of ether) to make a syringe 
that can put the guard into a deep sleep.

## Installation
This application needs the `pygame` module installed. To do that, you must the module via pip. I recommend to use a
virtual environment. You can either use the integrated library [venv](https://docs.python.org/3.8/library/venv.html) 
since python 3.3, [virtualenv](https://virtualenv.pypa.io/en/latest/) or any tool you want.

All dependencies of the projects are listed in the requirements.txt file at the root of the project. 
After you have created your virtual environment and activate it, use the following command to install dependencies:

```shell script
$ python3 -m pip install -r requirements.txt
```

## Run the game
After the pygame package is installed. The entry point of the application is the `main.py` file.
You have to run the file as a script with the python interpreter:

```shell script
$ python3 main.py
```

## Game controls
To move MacGyver, use the keyboard arrows 🡩 🡪 🡫 🡨.

MacGyver will collect every object simply by walking on it. The syringe will automatically be made by MacGyver when
all necessary items will be collected.
