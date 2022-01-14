# DnD Character Analyzer

A proof of concept for a D&D 5e character build analyzer, developed as the final project for the Fall 2020 COMP 1405 Z course at Carleton University, Ottawa.

Currently supports minimal options, including 3 races with 2 subraces each, 1 class with 2 subclasses, and 13 weapons. 

The aim of the program is to calculate a graph of average damage per level, simulating the growth of a player character from level 1 to 20 by prompting the user for decisions on features. Many details have been abstracted due to the game's complexity, but further extensions to the program would make it more accurate to real results.

## Usage
Clone to local directory with `git clone https://github.com/willKip/dnd_analyzer`; run `dnd_analysis.py`. The program is operated on the command line, and outputs graphs in a separate window. The graph window must be closed in order to shut the program down properly.

All character and game data is stored as JSON files, read and modified by the Python script. Character JSON files hold example characters, and the data calculated with their parameters.

`input1.txt` has example input to update the character JSONs with build data.

## Example
The following example makes use of the given `fake_gimli.json` and `frodo_froggins.json` character data files to output a comparison graph.

```
Options: 
1: Create Character
2: Load Character and Initialize Potential Damage
3: Load Character Damage Curve
4: Load and Compare two character damage curves  
5: Exit Program
What will you do? > 4

First character.
Choose a character file to load. > fake_gimli.json

Second character.
Choose a character file to load. > frodo_froggins.json
Graph updated.

Options:
1: Create Character
...
```
![Graph showing character damage comparisons.](/running_example.png)

## Acknowledgements
Project makes use of the [SimpleGraphics](https://pages.cpsc.ucalgary.ca/~bdstephe/217_F15/SimpleGraphics.py) wrapper for the [tkinter](https://docs.python.org/3/library/tkinter.html) standard Python package.

[Dungeons & Dragons](https://dnd.wizards.com/) belongs to Wizards of the Coast.
