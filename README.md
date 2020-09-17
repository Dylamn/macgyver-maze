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

or, if you prefer you can use the classic,
<kbd>w</kbd> <kbd>a</kbd> <kbd>s</kbd> <kbd>d</kbd> for qwerty, 
<kbd>z</kbd> <kbd>q</kbd> <kbd>s</kbd> <kbd>d</kbd> for azerty, keyboards.

MacGyver will collect every object simply by walking on it. 
The syringe can be crafted when MacGyver gather all necessary items.

To craft the syringe:

Press <kbd>C</kbd> when the text is prompted


Hope you'll like it !