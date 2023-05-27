# Knight's Tour Finder
This project contains 2 Python applications that tries to solve the Knight's Tour Problem using the Backtracking Algorithm and Warnsdorff's Heuristic. The applications were developed in the Pycharm IDE. 



## How It Works 
1. The project contains 2 applications: A game-like Graphical User Interface (GUI) application named 'main' and a console line application named 'Simulations'. 
2. The applications can be run using the executable files located in the 'dist' folder, or by running the code in 'main.py' or 'Simulations.py'.
3. In the both applications, the user can:
    - Select the type of algorithm to find a Knight's Tour. (Backtrack, Warnsdorff)
    - Select the dimensions for the chessboard. Minimum size is 3 x 3 and maximum size is 20 x 20. Note that a knight's tour cannot be found in a 3 x 3 board and is only used for showcasing a situation where a knight's tour cannot be found. The minimum size to find a knight's tour on a chessboard is 4 x 3 or 3 x 4.
    - Select the square where the knight starts from to find the tour.
4. In the game application, the user can:
    - See the step-by-step Knight's Tour generation process. 
    - Select the speed at which the Knight's Tour generation is done. (FPS)
    - Choose the colour of the Knight's Tour sequence. (Red, Green, Blue, Colour Blind)
    - Save an incomplete tour to resume at a later time.
5. In the console line application, the user can: 
    - Select how many successful tours to find before stopping. 
    - Select how the tour shall be found. (Find a tour using every square on the board, Find a tour using a random square on the board, or Find a tour using a specified square)
    - Specify whether the tours and duration of tour generation will be saved into a file

## How to Use 
### main
![GUI application]{https://github.com/AnnoyingShpee/help-the-knight/tree/main/img/gui.png}
1. Select the type of 
