Text Based Adventure Game 
This is a Project for CS-515 subject. It's a text-based adventure game. Navigate through different sorts of rooms and play with items. Your choices shape the outcome in this captivating journey.
How to Play
	1. Run the game with python3 adventure.py [map filename].
	2. Use commands like go, look, get, inventory, and quit to navigate and interact.
Made By
 Name: Smit Mhatre
 CWID: 20027642
 Stevens Login: smhatre@stevens.edu
GitHub Repo URL: https://github.com/smit0801/Text-Adventure-Game
Estimated Time Spent: 
Time spent 7 hours of actual programming(much more on youtube figuring how to make it)

Code Testing
I tested our code by:
	• Performing manual testing of various game scenarios, making various maps and running all possible commands on those maps
Known Bugs/Issues
	• Theres an issue with loading map which I discovered after uploading on gradescope. In general functionality i couldnt find it but the failed test cases on autograder found it.Couldnt reslove it because of the time constraints. 
Issue Resolution
One issue I encountered was during imlementation of "help" verb extension. Earlier, I just hard coded the print statements and it wans't reflective of the functions. I had to manually add a command to help, everytime I wanted to implement it. I talked to seniiors and he hinted me about the way and so I implemented a reflective "help" verb functionality.
Extensions Implemented

1)Abbreviations for verbs, directions, and items
Description: This extension allows the player to use abbreviated forms of commands, directions, and item names. For example, g for go, n for north, and mag for magazine.
How to exercise: Try using abbreviated forms of verbs, directions, and item names in your gameplay.
Map usage: The provided map loop.map can be used to test this extension.


2)A help verb
Description: This extension adds a help verb that displays a list of valid commands that the player can use.
How to exercise: Type help during gameplay to see the list of valid commands.
Map usage: The provided map loop.map can be used to test this extension.


3)Directions become verbs
Description: This extension allows the player to use directions as verbs instead of using the go command. For example, n instead of go north.
How to exercise: Try using directions as verbs during gameplay.
Map usage: The provided map loop.map can be used to test this extension.

Map for Extensions
The provided map loop.map can be used to test all the applicable extensions (abbreviations, help verb, and directions as verbs).

You can run the following commands:
 go <direction>
 get <item>
 drop <item>
 drop_all
 look
 inventory
 quit
 help
Instructions to check functioning of extensions on the map provided
Run the commands in the following order. Ignore the text inside square brackets
1)python3 adventure.py map.json
2)get magazine
3)west [Extension:Directions become verbs ]
4)inventory [this will show you that you have the rose with you in the new room too ]
5)drop magazine [Extension:Drop verb ]
6)inventory [this will show you that the rose is no more with you]
7)look [this will show you that the rose is in the items list of the current room]
8)help [Extension:Help verb]
9)quit

 How to Run
 To run the game, navigate to the base directory of the cloned repo and use the following command:
   codepython3 adventure.py [map_filename]
 Replace [map_filename] with the name of the map file you want to use (e.g., loop.map).
