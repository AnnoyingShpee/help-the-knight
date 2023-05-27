# Knight's Tour Finder
This project contains 2 Python applications that tries to solve the Knight's Tour Problem using the Backtracking Algorithm and Warnsdorff's Heuristic. The applications were developed in the Pycharm IDE. 

## How It Works 
1. The project contains 2 applications: A game-like Graphical User Interface (GUI) application named 'main' and a console line application named 'Simulations'. 
3. The applications can be run using the executable files located in the 'dist' folder, or by running the code in 'main.py' or 'Simulations.py'. main.py requires Components.py in order to run.
4. In the both applications, the user can:
    - Select the type of algorithm to find a Knight's Tour. (Backtrack, Warnsdorff)
    - Select the dimensions for the chessboard. 
    - Select the square where the knight starts from to find the tour.
5. In the game application, the user can:
    - See the step-by-step Knight's Tour generation process. 
    - Select the speed at which the Knight's Tour generation is done. (FPS)
    - Choose the colour of the Knight's Tour sequence. (Red, Green, Blue, Colour Blind)
    - Save an incomplete tour to resume at a later time.
6. In the console line application, the user can: 
    - Select how many successful tours to find before stopping. 
    - Select how the tour shall be found. (Find a tour using every square on the board, Find a tour using a random square on the board, or Find a tour using a specified square)
    - Specify whether the tours and duration of tour generation will be saved into a file
7. To create the executable file for main and Simulations, in a command line window, go to the directory containing main.py or Simulations.py. 
8. Type [pyinstaller --onefile main.py Components.py] to create an executable file for the game application.
9. Type [pyinstaller --onefile Simulations.py] to create an executable file for the console line application.

## How to Use 
### main
![GUI application](https://github.com/AnnoyingShpee/help-the-knight/blob/main/img/gui.png)
1. To choose the algorithm for solving the Knight's Tour, click on Algorithms. This will show buttons labeled with the algorithms that can be selected. Click on the button that you wish to use. 
2. To change the dimensions of the chessboard, click on '-1' or '+1' to change the number of rows and/or columns of the board. Minimum size is 3 x 3 and maximum size is 20 x 20. Note that a knight's tour cannot be found in a 3 x 3 board and is only used for showcasing a situation where a knight's tour cannot be found. The minimum size to find a knight's tour on a chessboard is 4 x 3 or 3 x 4.
3. Click on a square on the chessboard to choose the starting position of the Knight. This will be the starting square of the Knight's Tour.
4. Click on the 'Start' button to start the tour. The 'Start' button will then change to 'Pause'. Click on that to pause the tour generation.
5. If the tour generation is paused, the incomplete tour can be saved by clicking on the 'Save Tour' button.
6. To load the saved tour, make sure there is no tour being generated. Click on the 'Reset' button. This will clear the board and return the game to the default state. 

### Simulations
![GUI application](https://github.com/AnnoyingShpee/help-the-knight/blob/main/img/simulation.png)
1. The console line application can only accept keyboard inputs and has some error handling.
2. The application will first ask for the number of rows and columns for the chessboard. Input a number between 3 and 20 for both dimensions. 
3. Input the type of tour to find the knight's tour. The available tours will be listed.
4. Input the type of 'simulation'. 
    - all = Find a tour using every square on the board 
    - random = Find a tour using a random square on the board
    - specific = Find a tour using a specified square
6. If the type of simulation is 'specific', input row and column number of the first square of the knight's tour.
7. If the type of simulation is 'random' or 'specific', input the total number of tours to create.
8. Input Yes or No to save the tours created or not.
9. Input Yes or No to save the time taken to create the tours or not.
10. Input Yes or No to separate open and closed tours into different files or not.
11. Input Yes or No to separate structured and unstructured tours into different files or not.
