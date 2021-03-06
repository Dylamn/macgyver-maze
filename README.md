# Macgyver-maze

## Overview
macgyver-maze is a game written in python where the player is the famous MacGyver, lost inside a maze. 

The exit is protected by a guardian and MacGyver needs to bypass him in order to escape. To do this, MacGyver 
must combine three components (a plastic tube, a needle and a bottle of ether) to make a syringe 
that can put the guard into a deep sleep.

## Installation
This application needs the `pygame` module installed. To do that, you must the module via pip. I recommend to use a
virtual environment. You can either use the integrated library [venv](https://docs.python.org/3.8/library/venv.html) 
since python 3.3, [virtualenv](https://virtualenv.pypa.io/en/latest/) or any tool you want.

For example with venv, you can create and activate with the following:
```shell script
$ python3 -m venv venv
$ source venv/bin/activate
```

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

## Game settings
There's a default settings file which the game use that can be changed (you must change them when the game isn't running)

The game is provided with a minimum resolution of 640x640, therefore, 
it is not recommended to save a lower resolution than the one mentioned above to ensure proper working of the game.

## Game controls

First, if you want to go back to the previous menu, you can press the <kbd>echap</kbd> key (your game session is not reset)
The game play musics and sounds.

If you want to decrease/increase the volume, 
you can press either <kbd>-</kbd> or <kbd>+</kbd> keys of the numeric keypad.
If you simply want to mute/unmute the audio, press <kbd>F1</kbd>.

To move MacGyver, use the keyboard arrows:

<kbd>←</kbd> <kbd>↑</kbd> <kbd>→</kbd> <kbd>↓</kbd>

or, if you prefer you can use the classic 
<kbd>z</kbd> <kbd>q</kbd> <kbd>s</kbd> <kbd>d</kbd> with an azerty keyboard layout.

MacGyver will collect every object simply by walking on it. 
The syringe can be crafted when MacGyver gather all necessary items.

To craft the syringe:

Press <kbd>C</kbd> when the text is prompted


Hope you'll like it !

## Compilation

A setup.py file is present at the root of the project which is correctly configured for compilation 
**using [cx_freeze](https://cx-freeze.readthedocs.io/en/latest/overview.html)**.
To start a compilation with, use :
````shell script
$ python setup.py build
````

## Error with SDL

At some times, you can get an error when installing `pygame` like this one:
```
Unable to run "sdl-config". Please make sure a development version of SDL is installed.
```
If you use python3.8, try to install `pygame` with another python version.
If the problem is still there, try to install (globally) the following packages:
```shell script
sudo apt-get install python-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsdl1.2-dev libsmpeg-dev python-numpy subversion libportmidi-dev ffmpeg libswscale-dev libavformat-dev libavcodec-dev libfreetype6-dev
```

You can also check [this question](https://stackoverflow.com/questions/19579528/pygame-installation-sdl-config-command-not-found)
asked on Stack Overflow which can help you a lot.


