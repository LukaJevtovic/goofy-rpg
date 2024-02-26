Very simple and probably extremely unoptimized rpg game made using pygame (and numpy). You can find .zip files with prepackaged executable files for both windows and linux, made with pyinstaller. These you can run or send to someone even if they don't have python or any of its libraries.

I'm aiming to build a "roguelike dnd" at some point, with randomly selected dungeons and randomly generated encounters, bosses, items, loot, etc. Still very early in development.

INSTALLATION:

1.1 Windows: Download and extract the game_win.zip file. Run game.exe. This was created using pyinstaller on Windows 11, within the Anaconda environment. Windows defender will probably warn you that you're running an app from an unrecognized publisher. I can give you no more than my honest promise that there isn't anything malicious in my game :) If you believe me, click More Info, and then Run Anyway to start the game. At some point I might come back to this and try to make an installer that won't cause this issue with Windows Defender.

1.2 Windows: Alternatively, clone this repository, and make sure you have python, pygame and numpy installed, alongiside any python IDE (VSCode or whatever). Compile game.py within your IDE and enjoy the game.

2.1 Ubuntu-based Linux distros: Download and extract the game_linux.zip file. This was created using pyinstaller on Pop!-OS, which is a Ubuntu-based distro. This means that it should work on any other Ubuntu-based distro, although I haven't tested it outside pop-os. If you try it out on a different distro, feel free to let me know if it worked or not. Run the 'game' executable.

2.2 Ubuntu-based Linux distros: Alternatively, make sure you have the latest versions of python, pygame and numpy installed, then clone the entire repository and compile game.py (either directly from terminal using python3, or from an IDE).

CREDITS:

Game Mechanics:
The basis of this game is currently a slightly modified version of fifth edition rules for Dungeons and Dragons, by Wizards of the Coast. Legally I am obliged to include their Open Gaming License, which you can find in the main repository, named 'SRD-OGL_v5.1.pdf'. I plan to further modify and adapt the basic DnD rules for the purposes of the game in the future.

Music and SFX:
Music during adventure - created by ZHRØ on Freesound (https://freesound.org/people/ZHR%C3%98/sounds/527321/)
