# Sudoku
## Objective

There are 81 squares, divided into 9 blocks, each containing 9 squares. To win the game, each nine block section must contain all number 1-9 within its squares, without any duplicates in any one row, column or 9 block sub-section.

## Game Rules

    -Use your mouse to click on the block you'd like to select.
    -Once your block is selected, you may type using the numpad, any number from 1-9.
    -Your initial number will be "sketched" in, meaning it will not be registered until you hit the "ENTER" button. Doing so will return whether this move is valid or                   invalid. 
    -You may sketch as many numbers as you like, however, you'll need to go back and manually enter every number once you're ready.
    -The "Solve" button will use a backtracking, recursive algorithm to solve the board for you. 
    -The "Verify" button uses a brute-force, algorithm to verify your board solution, or the solution provided from the "Solve" button.
    -The "Reset" button generates a random new board. 
    -Once you've filled in all squares, you may hit the "Verify" button which will then verify your solution, if the solution is allowed you'll get a "Valid Solution" message on the bottom left of the Sudoku board. If it is not a valid solution you'll get a "Invalid Solution" message instead.

# How to play
## Repl.it

The game is hosted on repl.it here: https://repl.it/@BryanRodriguez5/SUHDoku

## Terminal

The alternative approach has a better UI experience but requires some set-up:
1. Install the latest version of Python
2. Install pip and Pygame

    To install pygame, type: python -m pip install pygame in your terminal

 3. On GitHub, click the Code button, download the zip file to the desktop and in your termial:

    -cd Desktop
    
    then type:
    
    -cd CS325SUHdoku-main
    
 4. In your terminal type python3 sudoku_GUI.py
 
 Thanks for playing!

    Enter python Sudoku.py and begin playing.
