# File:         proj3.py
# Author:       Ekele Ogbadu
# Date:         2 MAY 2019
# Section:      09
# E-mail:       eogbadu1@umbc.edu
# Description:  A simplified version of the game minesweeper

# Constants used in printing output
INTRO              = "\t This program allows you to play Minesweeper. \n \t The object of the game is to flag every mine, \n \t using clues about the number of neighboring \n \t mines in each field. To win the game, flag \n \t all of the mines (and don't incorrectly flag \n \t any non-mine fields).   Good luck!"

FILE_INPUT         = "Enter the file to load the board from: "
ERROR_MSG_POSITION = "That number is not allowed.  Please try again!"
ERROR_MSG_CHOICE   = "That's not a valid action."
INPUT_CHOICE_MSG   = "Enter 'r' to reveal the space, or \n enter 'f' to mark the space with a flag: "

LOSE_MSG           = "You detonated a mine!  Game Over!"

# Constants for positions in the board
FLAG               = "F"
MINE               = "*"
DETONATED_MINE     = "X"
BORDER             = "#"
SPACE              = " "
UNKNOWN            = "."
CLUES              = ["1", "2", "3", "4", "5", "6", "7", "8"]

# Used to find the end of the line when creating the initial board
END_OF_LINE        = 2


# prettyPrintBoard() prints the board with row and column labels,
#                    and spaces the board out so that it looks square
# Input:             board;   the rectangular 2d gameboard to print
# Output:            None;    prints the board in a pretty way
def prettyPrintBoard(board):

    print() # empty line

    # if enough columns, print a "tens column" line above
    if len(board[0])-2 >= 10:
        print("{:25s}".format(""), end="")  # empty space for 1 - 9
        for i in range(10, len(board[0])-1 ):
            print( str(i // 10), end =" ")
        print()

    # create and print top numbered line
    print("       ", end="")
    # only go from 1 to len - 1, so we don't number the borders
    for i in range(1, len(board[0])-1 ):
        # only print the last digit (so 15 --> 5)
        print(str(i % 10), end = " ")
    print()

    # create the border row
    borderRow = "     "
    for col in range(len(board[0])):
        borderRow += board[0][col] + " "

    # print the top border row
    print(borderRow)

    # print all the interior rows
    for row in range(1, len(board) - 1):
        # print the row label
        print("{:3d}  ".format(row), end="")

        # print the row contents
        for col in range(len(board[row])):
            if str(board[row][col]) == FLAG:
                # this will print the flag in black and green
                print("\033[1;30;42m" + "F" + "\033[0m", end =" ")
            elif str(board[row][col]) == DETONATED_MINE:
                # this will print the detonated Mine in white and red
                print("\033[1;37;41m" + "X" + "\033[0m", end =" ")
            else:
                print(str(board[row][col]), end = " ")
        print()

    # print the bottom border row and an empty line
    print(borderRow, "\n")

#####################################################################
# createBoard()      used to create initial game board from file
# Input:             fileName; the file name entered by the user 
# Output:            board;    the board it got from the file

def createBoard(fileName):
    
    row = []
    board = []
    i = 0
    j = 0

    # open the file and read in contents
    gameFile = open(fileName)
    fileContent = gameFile.read()

    # close the file
    gameFile.close()

    # put contents of file that was read into a 2-d list
    while i < len(fileContent):
        row.append(fileContent[i:i+1])
        if fileContent[i+1:i+2] == "\n":
            board.append(row[j:i+1])
            j = i + 2
        i += 1

    return board

########################################################################
# validateRow()      used to validate row input from the user
# Input:             rowInput; integer entered by the user
#                    board; 2-D board of chars that represents the game
# Output:            isValid; a boolean stating if the input is valid
def validateRow(rowInput, board):
    if rowInput < 1 or rowInput > len(board) - END_OF_LINE:
        isValid = False
    else:
        isValid = True

    return isValid

########################################################################
# validateColumn()   used to validate column input from the user
# Input:             columnInput; integer entered by the user
#                    board; 2-D board of chars that represents the game
# Output:            isValid; a boolean stating if the input is valid

def validateColumn(columnInput, board):
    if columnInput < 1 or columnInput > len(board) - END_OF_LINE:
        isValid = False
    else:
        isValid = True

    return isValid


########################################################################
# processInput()     processes the input entered by the user with the
#                    game board
# Input:             row; integer entered by the user for row input
#                    col; integer entered by the user for column
#                                 input
#                    choice; a char representing a validated choice
#                                 entered by the user
#                    numOfMines; an integer stating number of mines left
#                    board; 2-D board of chars that represents the game
#                    prettyBoard; a 2-D board of chars that is shown to
#                                 the player after each play
# Output:            numOfMines; an integer stating number of mines left
def processInput(row, col, choice, numOfMines, board, prettyBoard):
    # If player chooses to place a flag
    if choice == "f":
        # If position already flagged, unflag it
        if prettyBoard[row][col] == FLAG:
            prettyBoard[row][col] = UNKNOWN
            numOfMines += 1
            prettyPrintBoard(prettyBoard)

            # check if the game is complete after removing a flag
            isComplete  = checkGameComplete(board, prettyBoard, numOfMines)
            if numOfMines == 0 and isComplete == True:
                print()
            else:
                print("\t Flag removed from " + str(row) + ", " + str(col))
                print("\t There are", numOfMines, "mines left to find")
                print()

        # If position is a revealed empty space, do nothing
        elif prettyBoard[row][col] == SPACE:
            prettyPrintBoard(prettyBoard)
            print("\t Already been revealed")
            print()

        # If position is unknown, place a flag
        elif prettyBoard[row][col] == UNKNOWN:
            prettyBoard[row][col] = FLAG
            numOfMines -= 1
            prettyPrintBoard(prettyBoard)
            print("\t There are", numOfMines, "mines left to find")
            print()

    # If the user chooses to reveal 
    else:
        # if position has been revealed already, let user know
        if prettyBoard[row][col] == SPACE or prettyBoard[row][col] in CLUES:
            prettyPrintBoard(prettyBoard)
            print("\t Has been revealed already")
            print("\t There are", numOfMines, "mines left to find")
            print()

        # if position has been flagged
        elif prettyBoard[row][col] == FLAG:
            prettyPrintBoard(prettyBoard)
            print("\t Field " + str(row) + ", " + str(col) + " must be unflagged before it can be revealed")
            print("\t There are", numOfMines, "mines left to find")
            print()
            
        # if position has a mine, let user know and print game over message
        elif board[row][col] == MINE:
            prettyBoard[row][col] = DETONATED_MINE
            prettyPrintBoard(prettyBoard)
            print(LOSE_MSG)
            print()

        # if there is nothing at that poition, then reveal the empty fields(islands)
        elif board[row][col] != MINE and prettyBoard[row][col] == UNKNOWN:
            revealIsland(board, prettyBoard, row, col)
            prettyPrintBoard(prettyBoard)
            print("\t There are", numOfMines, "mines left to find")
            print()
        
    return numOfMines

##########################################################################
# checkGameComplete()  Checks if the user has won the game
# Input:               board; 2-D board of chars that represents the game
#                      prettyBoard; a 2-D board of chars that is shown to
#                                   the player after each play
#                      numMines; an integer holding number of mines left
# Output:              isComplete; a boolean showing if the game is won
def checkGameComplete(board, prettyBoard, numMines):
    isComplete = True

    # if there are any mines left, then  the game is not over
    if numMines != 0:
        isComplete = False
        
    for i in range(len(board)):
        for j in range(len(board)):

            # if the two boards mine and flag location do not match
            # then the game is not over
            if prettyBoard[i][j] == FLAG:
                if board[i][j] != MINE:
                    isComplete = False
            elif board[i][j] == MINE:
                if prettyBoard[i][j] != FLAG:
                    isComplete = False

    return isComplete
                   

#############################################################################
# checkMineDetonated()  Checks if the user has detonated a mine
# Input:                board; 2-D board of chars that represents the game
#                       rowInput; integer entered by the user for row input
#                       columnInput; integer entered by the user for column
#                                    input
# Output:               isDetonated; a boolean showing if a mine has been
#                                    detonated
def checkMineDetonated(board, rowInput, columnInput):
    isDetonated = False
    if board[rowInput][columnInput] == DETONATED_MINE:
        isDetonated = True

    return isDetonated

##############################################################################
# createPrettyBoard()   used to create the gameboard shown to the player
# Input:                fileName; a string variable - the name of the file
#                                 to read the board from.
# Output:               prettyBoard; a 2-D board of chars that is shown to
#                                    the player after each play

def createPrettyBoard(fileName):

    row = []
    prettyBoard = []
    i = 0
    j = 0

    # open the file to read
    gameFile = open(fileName)
    fileContent = gameFile.read()

    # close the file
    gameFile.close()

    # create 2-d list using contents of the file
    while i < len(fileContent):
        row.append(fileContent[i:i+1])
        if fileContent[i+1:i+2] == "\n":
            prettyBoard.append(row[j:i+1])
            j = i + 2
        i += 1

    # fill the empty spaces in the board with dots
    for i in range(len(prettyBoard)):
        for j in range(len(prettyBoard)):
            if prettyBoard[i][j] != BORDER:
                prettyBoard[i][j] = UNKNOWN
                

    return prettyBoard

##############################################################################
# numOfMinesAround()    used to find how many mines in contact with each
#                       location
# Input:                row; integer entered by the user for row input
#                       col; integer entered by the user for column
#                       board; 2-D board of chars that represents the game
#                    
# Output                numOfMines; an integer representing the number of
#                                   mines around a location
def numOfMinesAround(row, col, board):
    numOfMines = 0

    # check if there are mines at each location around the position entered
    if board[row - 1][col] == MINE:
        numOfMines += 1

    if board[row + 1][col] == MINE:
        numOfMines += 1

    if board[row][col - 1] == MINE:
        numOfMines += 1

    if board[row][col + 1] == MINE:
        numOfMines += 1

    if board[row - 1][col - 1] == MINE:
        numOfMines += 1

    if board[row + 1][col - 1] == MINE:
        numOfMines += 1

    if board[row - 1][col + 1] == MINE:
        numOfMines += 1

    if board[row + 1][col + 1] == MINE:
        numOfMines += 1

    return numOfMines


##############################################################################
# numOfMines()    used to find how many mines in the game
# Input:          board; 2-D board of chars that represents the game
# Output          numOfMines; an integer representing the number of mines
#
def numOfMines(board):
    count = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == MINE:
                count += 1
    return count
        

#######################################################################
# revealIsland()    checks if there are islands and calls recursive
#                   functions when needed
# Input:            board; 2-D board of chars that represents the game
#                   prettyBoard; a 2-D board of chars that is shown to
#                                the player after each play
#                   row; integer entered by the user for row input
#                   col; integer entered by the user for column
#                        input
# Output:           none; used to call recursive functions when required
def revealIsland(board, prettyBoard, row, col):
    # if the position is not empty, do nothing
    if board[row][col] == MINE or board[row][col] == BORDER or prettyBoard[row][col] in CLUES or prettyBoard[row][col] == FLAG:
        return
    else:
        if board[row][col] == SPACE:

            # if position is empty, check number of mines around the position
            # and assign the position a value
            clue = numOfMinesAround(row, col, board)
            if clue == 0:
                prettyBoard[row][col] = SPACE
            else:
                prettyBoard[row][col] = str(clue)

            # if position is a space after the check above, call recursive
            # functions to reveal the empty fields (islands)
            if prettyBoard[row][col] == SPACE:    
                revealUp(board, prettyBoard, row, col)
                revealDown(board, prettyBoard, row, col)
                revealLeft(board, prettyBoard, row, col)
                revealRight(board, prettyBoard, row, col)
                revealUpperRight(board, prettyBoard, row, col)
                revealLowerRight(board, prettyBoard, row, col)
                revealUpperLeft(board, prettyBoard, row, col)
                revealLowerLeft(board, prettyBoard, row, col)
            

#######################################################################
# revealLeft()      recursive function used to reveal all empty spaces
#                   to the left of a position.
# Input:            board; 2-D board of chars that represents the game
#                   prettyBoard; a 2-D board of chars that is shown to
#                                the player after each play
#                   row; integer entered by the user for row input
#                   col; integer entered by the user for column
#                        input
# Output:           none; recursive call until base staement is reached
def revealLeft(board, prettyBoard, row, col):
    
    # if the position is not empty, do nothing
    if board[row][col] == MINE or board[row][col] == BORDER or prettyBoard[row][col] in CLUES or prettyBoard[row][col] == FLAG:
        return

    # if position to the left is a mine, border, flag or space.
    # Do nothing
    elif board[row][col - 1] == MINE or board[row][col - 1] == BORDER or prettyBoard[row][col - 1] == FLAG or prettyBoard[row][col - 1] == SPACE:
        return
    else:

        # find number of mines around position to the left and assign
        # value to position
        clue = numOfMinesAround(row, col - 1, board)
        if clue == 0:
            prettyBoard[row][col - 1] = SPACE
        else:
            prettyBoard[row][col - 1] = str(clue)

        # if value assigned after statement above is a space, recursively call
        # recursive functions
        if prettyBoard[row][col - 1] == SPACE:
            revealUp(board, prettyBoard, row, col - 1)
            revealDown(board, prettyBoard, row, col - 1)
            revealLeft(board, prettyBoard, row, col - 1)
            revealRight(board, prettyBoard, row, col - 1)
            revealUpperRight(board, prettyBoard, row, col - 1)
            revealLowerRight(board, prettyBoard, row, col - 1)
            revealUpperLeft(board, prettyBoard, row, col - 1)
            revealLowerLeft(board, prettyBoard, row, col - 1)
        else:
            return

#######################################################################
# revealRight()     recursive function used to reveal all empty spaces
#                   to the right of a position.
# Input:            board; 2-D board of chars that represents the game
#                   prettyBoard; a 2-D board of chars that is shown to
#                                the player after each play
#                   row; integer entered by the user for row input
#                   col; integer entered by the user for column
#                        input
# Output:           none; recursive call until base staement is reached
def revealRight(board, prettyBoard, row, col):

    # if the position is not empty, do nothing
    if board[row][col] == MINE or board[row][col] == BORDER or prettyBoard[row][col] in CLUES or prettyBoard[row][col] == FLAG:
        return

    # if position to the right is a mine, border, flag or space.
    # Do nothing
    elif board[row][col + 1] == MINE or board[row][col + 1] == BORDER or prettyBoard[row][col + 1] == FLAG or prettyBoard[row][col + 1] == SPACE:
        return
    else:

        # find number of mines around position to the right and assign
        # value to position
        clue = numOfMinesAround(row, col + 1, board)
        if clue == 0:
             prettyBoard[row][col + 1] = SPACE
        else:
            prettyBoard[row][col + 1] = str(clue)

        # if value assigned after statement above is a space, recursively call
        # recursive functions
        if prettyBoard[row][col + 1] == SPACE:
            revealUp(board, prettyBoard, row, col + 1)
            revealDown(board, prettyBoard, row, col + 1)
            revealLeft(board, prettyBoard, row, col + 1)
            revealRight(board, prettyBoard, row, col + 1)
            revealUpperRight(board, prettyBoard, row, col + 1)
            revealLowerRight(board, prettyBoard, row, col + 1)
            revealUpperLeft(board, prettyBoard, row, col + 1)
            revealLowerLeft(board, prettyBoard, row, col + 1)
        else:
            return

#######################################################################
# revealUp()        recursive function used to reveal all empty spaces
#                   to the top of a position.
# Input:            board; 2-D board of chars that represents the game
#                   prettyBoard; a 2-D board of chars that is shown to
#                                the player after each play
#                   row; integer entered by the user for row input
#                   col; integer entered by the user for column
#                        input
# Output:           none; recursive call until base staement is reached
def revealUp(board, prettyBoard, row, col):

    # if the position is not empty, do nothing
    if board[row][col] == MINE or board[row][col] == BORDER or prettyBoard[row][col] in CLUES or prettyBoard[row][col] == FLAG:
        return

    # if position to the top is a mine, border, flag or space.
    # Do nothing
    elif board[row - 1][col] == MINE or board[row - 1][col] == BORDER or prettyBoard[row - 1][col] == FLAG or prettyBoard[row - 1][col] == SPACE:
        return
    else:

        # find number of mines around position to the top and assign
        # value to position
        clue = numOfMinesAround(row - 1, col, board)
        if clue == 0:
            prettyBoard[row - 1][col] = SPACE
        else:
            prettyBoard[row - 1][col] = str(clue)

        # if value assigned after statement above is a space, recursively call
        # recursive functions
        if prettyBoard[row - 1][col] == SPACE:
            revealUp(board, prettyBoard, row - 1, col)
            revealDown(board, prettyBoard, row - 1, col)
            revealLeft(board, prettyBoard, row - 1, col)
            revealRight(board, prettyBoard, row - 1, col)
            revealUpperRight(board, prettyBoard, row - 1, col)
            revealLowerRight(board, prettyBoard, row - 1, col)
            revealUpperLeft(board, prettyBoard, row - 1, col)
            revealLowerLeft(board, prettyBoard, row - 1, col)
        else:
            return

#######################################################################
# revealDown()      recursive function used to reveal all empty spaces
#                   to the bottom of a position.
# Input:            board; 2-D board of chars that represents the game
#                   prettyBoard; a 2-D board of chars that is shown to
#                                the player after each play
#                   row; integer entered by the user for row input
#                   col; integer entered by the user for column
#                        input
# Output:           none; recursive call until base staement is reached
def revealDown(board, prettyBoard, row, col):

    # if the position is not empty, do nothing
    if board[row][col] == MINE or board[row][col] == BORDER or prettyBoard[row][col] in CLUES or prettyBoard[row][col] == FLAG:
        return

    # if position to the bottom is a mine, border, flag or space.
    # Do nothing
    elif board[row + 1][col] == MINE or board[row + 1][col] == BORDER or prettyBoard[row + 1][col] == FLAG or prettyBoard[row + 1][col] == SPACE:
        return
    else:
        # find number of mines around position to the bottom and assign
        # value to position
        clue = numOfMinesAround(row + 1, col, board)
        if clue == 0:
            prettyBoard[row + 1][col] = SPACE
        else:
            prettyBoard[row + 1][col] = str(clue)

        # if value assigned after statement above is a space, recursively call
        # recursive functions
        if prettyBoard[row + 1][col] == SPACE:
            revealUp(board, prettyBoard, row + 1, col)
            revealDown(board, prettyBoard, row + 1, col)
            revealLeft(board, prettyBoard, row + 1, col)
            revealRight(board, prettyBoard, row + 1, col)
            revealUpperRight(board, prettyBoard, row + 1, col)
            revealLowerRight(board, prettyBoard, row + 1, col)
            revealUpperLeft(board, prettyBoard, row + 1, col)
            revealLowerLeft(board, prettyBoard, row + 1, col)
        else:
            return

#########################################################################
# revealUpperRight()  recursive function used to reveal all empty spaces
#                     to the upper-right of a position.
# Input:              board; 2-D board of chars that represents the game
#                     prettyBoard; a 2-D board of chars that is shown to
#                                  the player after each play
#                     row; integer entered by the user for row input
#                     col; integer entered by the user for column
#                          input
# Output:             none; recursive call until base staement is reached
def revealUpperRight(board, prettyBoard, row, col):

    # if the position is not empty, do nothing
    if board[row][col] == MINE or board[row][col] == BORDER or prettyBoard[row][col] in CLUES or prettyBoard[row][col] == FLAG:
        return

    # if position to the upper-right is a mine, border, flag or space.
    # Do nothing
    elif board[row - 1][col + 1] == MINE or board[row - 1][col + 1] == BORDER or prettyBoard[row - 1][col + 1] == FLAG or prettyBoard[row - 1][col + 1] == SPACE:
        return
    else:

        # find number of mines around position to the upper-right and assign
        # value to position
        clue = numOfMinesAround(row - 1, col + 1, board)
        if clue == 0:
            prettyBoard[row - 1][col + 1] = SPACE
        else:
            prettyBoard[row - 1][col + 1] = str(clue)

        # if value assigned after statement above is a space, recursively call
        # recursive functions
        if prettyBoard[row - 1][col + 1] == SPACE:
            revealUp(board, prettyBoard, row - 1, col + 1)
            revealDown(board, prettyBoard, row - 1, col + 1)
            revealLeft(board, prettyBoard, row - 1, col + 1)
            revealRight(board, prettyBoard, row - 1, col + 1)
            revealUpperRight(board, prettyBoard, row - 1, col + 1)
            revealLowerRight(board, prettyBoard, row - 1, col + 1)
            revealUpperLeft(board, prettyBoard, row - 1, col + 1)
            revealLowerLeft(board, prettyBoard, row - 1, col + 1)
        else:
            return


#######################################################################
# revealLowerRight()  recursive function used to reveal all empty spaces
#                     to the lower-right of a position.
# Input:              board; 2-D board of chars that represents the game
#                     prettyBoard; a 2-D board of chars that is shown to
#                                  the player after each play
#                     row; integer entered by the user for row input
#                     col; integer entered by the user for column
#                          input
# Output:             none; recursive call until base staement is reached
def revealLowerRight(board, prettyBoard, row, col):

    # if the position is not empty, do nothing
    if board[row][col] == MINE or board[row][col] == BORDER or prettyBoard[row][col] in CLUES or prettyBoard[row][col] == FLAG:
        return

    # if position to the lower-right is a mine, border, flag or space.
    # Do nothing
    elif board[row + 1][col + 1] == MINE or board[row + 1][col + 1] == BORDER or prettyBoard[row + 1][col + 1] == FLAG or prettyBoard[row + 1][col + 1] == SPACE:
        return
    else:

        # find number of mines around position to the lower-right and assign
        # value to position
        clue = numOfMinesAround(row + 1, col + 1, board)
        if clue == 0:
            prettyBoard[row + 1][col + 1] = SPACE
        else:
            prettyBoard[row + 1][col + 1] = str(clue)

        # if value assigned after statement above is a space, recursively call
        # recursive functions
        if prettyBoard[row + 1][col + 1] == SPACE:
            revealUp(board, prettyBoard, row + 1, col + 1)
            revealDown(board, prettyBoard, row + 1, col + 1)
            revealLeft(board, prettyBoard, row + 1, col + 1)
            revealRight(board, prettyBoard, row + 1, col + 1)
            revealUpperRight(board, prettyBoard, row + 1, col + 1)
            revealLowerRight(board, prettyBoard, row + 1, col + 1)
            revealUpperLeft(board, prettyBoard, row + 1, col + 1)
            revealLowerLeft(board, prettyBoard, row + 1, col + 1)
        else:
            return

#######################################################################
# revealUpperLeft() recursive function used to reveal all empty spaces
#                   to the upper-left of a position.
# Input:            board; 2-D board of chars that represents the game
#                   prettyBoard; a 2-D board of chars that is shown to
#                                the player after each play
#                   row; integer entered by the user for row input
#                   col; integer entered by the user for column
#                        input
# Output:           none; recursive call until base staement is reached
def revealUpperLeft(board, prettyBoard, row, col):
    
    # if position is not empty, do nothing
    if board[row][col] == MINE or board[row][col] == BORDER or prettyBoard[row][col] in CLUES or prettyBoard[row][col] == FLAG:
        return

    # if position to the upper-left is a mine, border, flag or space.
    # Do nothing
    elif board[row - 1][col - 1] == MINE or board[row - 1][col - 1] == BORDER or prettyBoard[row - 1][col - 1] == FLAG or prettyBoard[row - 1][col - 1] == SPACE:
        return
    else:
        # find number of mines around position to the upper-left and assign
        # value to position
        clue = numOfMinesAround(row - 1, col - 1, board)
        if clue == 0:
            prettyBoard[row - 1][col - 1] = SPACE
        else:
            prettyBoard[row - 1][col - 1] = str(clue)

        # if value assigned after statement above is a space, recursively call
        # recursive functions
        if prettyBoard[row - 1][col - 1] == SPACE:
            revealUp(board, prettyBoard, row - 1, col - 1)
            revealDown(board, prettyBoard, row - 1, col - 1)
            revealLeft(board, prettyBoard, row - 1, col - 1)
            revealRight(board, prettyBoard, row - 1, col - 1)
            revealUpperRight(board, prettyBoard, row - 1, col - 1)
            revealLowerRight(board, prettyBoard, row - 1, col - 1)
            revealUpperLeft(board, prettyBoard, row - 1, col - 1)
            revealLowerLeft(board, prettyBoard, row - 1, col - 1)
        else:
            return

#######################################################################
# revealLowerLeft() recursive function used to reveal all empty spaces
#                   to the lower-left of a position.
# Input:            board; 2-D board of chars that represents the game
#                   prettyBoard; a 2-D board of chars that is shown to
#                                the player after each play
#                   row; integer entered by the user for row input
#                   col; integer entered by the user for column
#                        input
# Output:           none; recursive call until base staement is reached
def revealLowerLeft(board, prettyBoard, row, col):
    
    # if position is not empty, do nothing
    if board[row][col] == MINE or board[row][col] == BORDER or prettyBoard[row][col] in CLUES or prettyBoard[row][col] == FLAG:
        return

    # if position to the lower-left is a mine, border, flag or space.
    # Do nothing
    elif board[row + 1][col - 1] == MINE or board[row + 1][col - 1] == BORDER or prettyBoard[row + 1][col - 1] == FLAG or prettyBoard[row + 1][col - 1] == SPACE:
        return
    else:
        # find number of mines around position to the lower-left and assign
        # value to position
        clue = numOfMinesAround(row + 1, col - 1, board)
        if clue == 0:
            prettyBoard[row + 1][col - 1] = SPACE
        else:
            prettyBoard[row + 1][col - 1] = str(clue)

        # if value assigned after statement above is a space, recursively call
        # recursive functions
        if prettyBoard[row + 1][col - 1] == SPACE:
            revealUp(board, prettyBoard, row + 1, col - 1)
            revealDown(board, prettyBoard, row + 1, col - 1)
            revealLeft(board, prettyBoard, row + 1, col - 1)
            revealRight(board, prettyBoard, row + 1, col - 1)
            revealUpperRight(board, prettyBoard, row + 1, col - 1)
            revealLowerRight(board, prettyBoard, row + 1, col - 1)
            revealUpperLeft(board, prettyBoard, row + 1, col - 1)
            revealLowerLeft(board, prettyBoard, row + 1, col - 1)
        else:
            return
        
#######################################################################
# getRow()        used to get and the row input from the user
# Input:          board; 2-D board of chars that represents the game
# Output:         rowInput; integer - validated row input
def getRow(board):
    # get row from user
    print ("Please choose the row:")
    rowInput = int(input("Enter a number between 1 and " + str(len(board) - END_OF_LINE) + "(inclusive): "))

    # check if the row entered is a valid row
    isRowValid = validateRow(rowInput, board)

    # keep asking till valid row is entered
    while isRowValid == False:
        print(ERROR_MSG_POSITION)
        rowInput = int(input("Enter a number between 1 and " + str(len(board) - END_OF_LINE) + "(inclusive): "))
        isRowValid = validateRow(rowInput, board)

    return rowInput

#######################################################################
# getColumn()     used to get and the column input from the user
# Input:          board; 2-D board of chars that represents the game
# Output:         columnInput; integer - validated column input
def getColumn(board):
    # Get the column                                                           
    print ("Please choose the column:")

    columnInput = int(input("Enter a number between 1 and " + str(len(board) - END_OF_LINE) + "(inclusive): "))

    # check if column value entered is valid
    isColumnValid = validateColumn(columnInput, board)

    # keep asking until valid input is entered
    while isColumnValid == False:
        print(ERROR_MSG_POSITION)
        columnInput = int(input("Enter a number between 1 and " + str(len(board) - END_OF_LINE) + "(inclusive): "))
        isColumnValid = validateColumn(columnInput, board)

    return columnInput


############################################################################
# getChoice()     used to get reveal or flag choice from the user
# Input:          board; 2-D board of chars that represents the game
# Output:         userChoice; single char string -  validated choice input
def getChoice(board):
    
    # Get choice to reveal or flag
    userChoice = input(INPUT_CHOICE_MSG)
    while userChoice != "f" and userChoice != "r":
        print(ERROR_MSG_CHOICE)
        userChoice = input(INPUT_CHOICE_MSG)

    return userChoice



def main():

    numMines    = 0
    isDetonated = False
    isComplete  = False

    print()
    print(INTRO)
    print()

    # Get the file name from the user
    fileName = input("Enter the file to load the board from: ")

    # create the board used by the game to keep track of mines
    board = createBoard(fileName)

    # Create the board that will be displayed to the user
    prettyBoard = createPrettyBoard(fileName)

    # Get initial number of mines in the field
    numMines = numOfMines(board)

    # print the initial board for debugging
    prettyPrintBoard(prettyBoard)

    # Print number of mines in the field
    print("\t There are", numMines, "mines left to find")
    print()

    # Start while loop to play game till it is over
    while isDetonated == False and isComplete == False:
        # Get inputs from the user and validate
        rowInput    = getRow(board)
        columnInput = getColumn(board)
        userChoice  = getChoice(board)

        numMines = processInput(rowInput, columnInput, userChoice, numMines, board, prettyBoard)

        isDetonated = checkMineDetonated(prettyBoard, rowInput, columnInput)
        isComplete  = checkGameComplete(board, prettyBoard, numMines)

    # print message when the user wins the game
    if isDetonated == False and isComplete == True:
        print("You won! Congratulations, and good game!")
    
main()
