# ECEN 2703 Project, Spring 2021, Kyle Shi 
# SUDOKU GENERATOR WITH DIFFERENT DIFFICULTIES. 
# Includes several helper functions to solve sudoku, check validity of guesses, etc. 

# RULES: 
# Each square must contain a number between 1 and 9.
# Each number 1-9 can only appear once in each row, column and box.
# A proper Sudoku has only one unique solution.
# There must be at least 17 clues in order to have a puzzle with one unique solution.

"""
IMPLEMENTED SOLUTION: 
1. Generate an empty grid // done!
2. Using backtracking algorithm, generate solution to this grid. // done!
   I've added an element of "randomness" in the solver algorithm to generate different grid solutions each time. // done!
3. Remove 1 number from the grid at a time // done!
4. After removing the number, check that the solution is unique and still solvable. // done!
5. If the board stil have a unique solution after removing one number, then another value may be removed, and check the solution again. // done!
   If the board no longer has a unique solution, put the removed value back in the grid. // done!
   Repeat this process. // done!

EXTRA CREDIT: 
  Repeat the process from 3-5 with different value each time and remove additional numbers, changing the difficulty of the grid. // done!
  This value is based off the user's input for how many clues they'd like to have. // done!
  The amount of times this process is repeated will alter the difficulty of the final grid. // done!
"""

"""
BACKTRACKING ALGORITHM: 
1. Choose number starting from 1-9. If this number is valid, i.e. not in the same box, row, column, then assign to that square.
2. Using recursion, see if that chosen number will lead to a valid unique solution. 
3. If no valid unique solution is found, remove that number from the square and try the next number choice. 

"""
from random import randint, shuffle
import pprint

# creating empty grid
grid = [
        [0, 0, 0,   0, 0, 0,   0, 0, 0],
        [0, 0, 0,   0, 0, 0,   0, 0, 0],
        [0, 0, 0,   0, 0, 0,   0, 0, 0],

        [0, 0, 0,   0, 0, 0,   0, 0, 0],
        [0, 0, 0,   0, 0, 0,   0, 0, 0],
        [0, 0, 0,   0, 0, 0,   0, 0, 0],

        [0, 0, 0,   0, 0, 0,   0, 0, 0],
        [0, 0, 0,   0, 0, 0,   0, 0, 0],
        [0, 0, 0,   0, 0, 0,   0, 0, 0]
    ]
grid_2 = [
        [0, 0, 0,   0, 0, 0,   0, 0, 0],
        [0, 0, 0,   0, 0, 0,   0, 0, 0],
        [0, 0, 0,   0, 0, 0,   0, 0, 0],

        [0, 0, 0,   0, 0, 0,   0, 0, 0],
        [0, 0, 0,   0, 0, 0,   0, 0, 0],
        [0, 0, 0,   0, 0, 0,   0, 0, 0],

        [0, 0, 0,   0, 0, 0,   0, 0, 0],
        [0, 0, 0,   0, 0, 0,   0, 0, 0],
        [0, 0, 0,   0, 0, 0,   0, 0, 0]
    ]
solution_counter = 0 # there are no solutions yet, as no grid's been solved 

# Function that finds the next empty square in the grid, returns its position (row, col)
def find_next_empty(grid):
  # finds the next empty square,  row, col in the grid 
  # return row, col  
  for r in range(9):
      for c in range(9): # range(9) is 0, 1, 2, ... 8
          if grid[r][c] == 0:
              return r, c

  return None, None  # if no spaces in the puzzle are empty 

# Function that checks if a guess is valid, returns True or False. 
def valid_guess(grid, guess, row, col):
  # returns true or false for a guess
  # if a number guessed isn't in the row/column/box, returns true. else returns false

  # checking the row first, creates a list from the current row being checked 
  row_vals = grid[row]
  if guess in row_vals:
      return False # if the guess is already in the row, it's not valid

  # col_vals = []
  # for i in range(9):
  #     col_vals.append(puzzle[i][col])
  # creates a list of the values in the column being checked
  col_vals = [grid[i][col] for i in range(9)]
  if guess in col_vals:
      return False # if the guess is in the column... it's not valid

  # checking to make sure the value isn't in the square
  row_start = (row // 3) * 3 # 10 // 3 = 3, 5 // 3 = 1, 1 // 3 = 0
  col_start = (col // 3) * 3
  # this for loop runs through each element in the square, 
  # for example, row is 2, column is 1, then row_start = 0 * 3 = 0, col_start = 0 * 3 = 0. 
  # and the loop checks these positions in the square (row position from 0 to 2, col position from 0 to 2)
  #           (0,0) -> (0,1) -> (0,2)
  #           (1,0) -> (1,1) -> (1,2)
  #           (2,0) -> (2,1) -> (2,2)

  for r in range(row_start, row_start + 3):
      for c in range(col_start, col_start + 3):
          if grid[r][c] == guess:
              return False

  return True



# returns a list of the number of non empty squares in the grid
def get_non_empty(grid):
  non_empty = []
  for rows in range(len(grid)):
    for cols in range(len(grid)):
      if grid[rows][cols] != 0:
        non_empty.append((rows,cols)) # appends the non empty element to the non_empty list
  return non_empty

# returns True or False depending on whether or not a grid is solveable. 
# also alters the grid that's being checked (the inputted grid will be solved if it's solvable)
def solve_sudoku(grid):
  global solution_counter
  # main solver function 
  # the input is a list of lists
  # returns true if a solution exists as well as solves the grid 
  # don't input an empty grid, it will generate a filled grid but it will be the same each time..
  
  # choosing position on the puzzle to guess from 
  row, col = find_next_empty(grid) 

  # checking to see if there are no empty spaces left
  if row is None and col is None:  # find_next_empty returns None if there is no position in the grid that's empty
    solution_counter += 1
    return True  # if this is true, then the puzzle is solved 

   # if row isn't None, make a guess between 1 and 9 and place that number 
  for guess in range(1, 10): # range(1, 10) is 1, 2, 3, ... 9
    # check if guess valid
    if valid_guess(grid, guess, row, col):
      # if valid, place guess
      grid[row][col] = guess

      if solve_sudoku(grid): # recursive call to solver function 
        return True

    #if nothing is valid, try a new number (set that square back to empty)
    grid[row][col] = 0
  
  # grid is not solvable if none of the tried numbers work 
  return False

"""
AS IT IS NOW, solve_sudoku WILL SOLVE A BOARD BUT IF GIVEN A COMPLETELY EMPTY BOARD, IT WILL FILL THE SAME BOARD EACH TIME
In the next part of this code, I implement "randomness" into the solver so that a different filled board is generated each time
"""
number_list = [1,2,3,4,5,6,7,8,9]

# THIS FUNCTION CREATES A RANDOMIZED FULLY SOLVED SUDOKU GRID USING AN EMPTY GRID, this is NOT meant to be a solver function, it will not tell you whether or not a board is solveable
def fill_sudoku(grid):
  # choosing position on the puzzle to guess from 
  row, col = find_next_empty(grid)
  
  # checking to see if there are no empty spaces left
  if row is None and col is None:  # find_next_empty returns None if there is no position in the grid that's empty
      return grid  # if this is true, then the puzzle is solved

  if grid[row][col] == 0:
    shuffle(number_list) # this shuffles the list everytime there is an empty grid, this makes the new guesses randomized so each filled grid is random
  # if row isn't None, make a guess between 1 and 9 and place that number 
    for guess in number_list: # range(1, 10) is 1, 2, 3, ... 9
    # check if guess valid
     if valid_guess(grid, guess, row, col):
        # if valid, place guess
        grid[row][col] = guess
        
        # recursive call to solver function 
        if fill_sudoku(grid):
            return grid
      
      # if nothing is valid, try a new number (set that square back to empty)
     grid[row][col] = 0

  # grid is not solvable if none of the tried numbers work 
  return False


# This function returns a sudoku board with only 17 clues, takes in the input of a fully solved board
def grid_remove_17(grid):
  global solution_counter

  # this is the number of iterations that are going to be ran through 
  iterations = 5 
  solution_counter = 1 # before we remove from the grid, there is exactly 1 solution
  non_empty = get_non_empty(grid)
  non_empty_count = len(non_empty)
  while iterations > 0 and non_empty_count > 17: 
  # selecting random cell that's not already empty
    row = randint(0,8)
    col = randint(0,8)
    while grid[row][col]==0:
      row = randint(0,8)
      col = randint(0,8)
    # removing a value from the value of non_empty (since we are removing a value from the grid)
    non_empty_count -= 1
    # store the value where the number was replaced
    store_replaced = grid[row][col]
    grid[row][col] = 0

    # copying the entire current grid
    grid_copy = []
    for rows in range(0,9):
      grid_copy.append([])
      for cols in range(0,9): # filling out the copy of the grid from left to right, up to down. (row 1 (left to right) -> row 2 -> row 3 -> ...)
        grid_copy[rows].append(grid[rows][cols])

    # counting number of solutions this grid has
    solution_counter = 0
    solve_sudoku(grid_copy) # this will produce a value for the global variable "solution_counter". it will also solve the grid to make sure it still works. if the grid doesn't work, then the function will return false
    # if number of solutions is != 1, put back in original number (store)
    if solution_counter != 1:
      grid[row][col] = store_replaced
      iterations -= 1 
  return grid


# function works the same as the grid_remove_17 function, except you get to pick how many clues you'd like between 17 and 80 (inclusive)
# if you put in an invalid number the function obviously won't work so please don't. 
def grid_remove_diff(grid, clues: int):
  global solution_counter
  # Put in a high number for difficulty if you would like a more difficult board. 

  # this is the number of iterations that are going to be ran through 
  # while removing numbers from the board. Higher iterations will result
  # in a more difficult board. 
  iterations = 5 # set how hard you want board to be 
  clue_number = clues # THESE ARE THE NUMBER OF CLUES THAT YOU WANT TO HAVE IN THE BOARD, the minimum you can put is 17 and the max is 80
  solution_counter = 1 # before we remove from the grid, there is exactly 1 solution
  non_empty = get_non_empty(grid)
  non_empty_count = len(non_empty)

  # returns false if you enter an invalid clue size
  if clue_number < 17:
    return False
  elif clue_number > 80:
    return False

  elif clue_number >= 17 and clue_number <=80: # the program won't run if your number of clues isn't within this range
    while iterations > 0 and non_empty_count > clue_number: 
    # selecting random cell that's not already empty
      row = randint(0,8)
      col = randint(0,8)
      while grid[row][col]==0:
        row = randint(0,8)
        col = randint(0,8)
      # removing a value from the value of non_empty (since we are removing a value from the grid)
      non_empty_count -= 1     

      # store the value where the number was replaced
      store_replaced = grid[row][col]
      grid[row][col] = 0

      # copying the entire current grid
      grid_copy = []
      for rows in range(0,9):
        grid_copy.append([])
        for cols in range(0,9): # filling out the copy of the grid from left to right, up to down. (row 1 (left to right) -> row 2 -> row 3 -> ...)
          grid_copy[rows].append(grid[rows][cols])

      # counting number of solutions this grid has
      solution_counter = 0
      solve_sudoku(grid_copy) # this will produce a value for the global variable "solution_counter". it will also solve the grid to make sure it still works. if the grid doesn't work, then the function will return false
      # if number of solutions is != 1, put back in original number (store)
      if solution_counter != 1:
        grid[row][col] = store_replaced
        iterations -= 1 
    return grid




# FILLING NEW RANDOM GRIDS
new_grid = fill_sudoku(grid) # randomly filled out completed grid (follows all sudoku rules...)
new_grid_2 = fill_sudoku(grid_2) # grid 2 


# PRINTS THAT SAME GRID WITH NUMBERS REMOVED
# it will take a few seconds or more to print the grid, please wait
# I have also included 2 boards of different difficulties here to demonstrate that the extra credit portion of this assignment works! 
# Please look closely to see that clue_17_Board always returns a board with 17 clues and that the difficulty_Board will return however many clues you set. I have it defaulted to 30. 

# Here a grid is printed with 17 clues. its solutions are printed afterwards
print("This is the 17 clues sudoku board: ")
print("")
clue_17_Board = grid_remove_17(new_grid)
pprint.pprint(clue_17_Board) # new board with 17 clues
print("Solvability check: ", solve_sudoku(clue_17_Board)) # checking solvability
print("")
print("Here's the solution to the board, don't peak! :")
pprint.pprint(clue_17_Board) # solution to the board
print("")

# Here a grid is printed with a "difficulty" of 30 (30 clues). The higher the number, the lower the difficulty. The lower the number, the higher the difficulty. 
# the input that grid_remove_diff(grid, clues) takes is the number of clues that you want remaining in the board. So if you set this number higher, the board is easier.
# If you set it lower, the board is harder. The minimum is 17 clues and the maximum is 80 otherwise the function will not work because the board will not have a unique solution. 
print("Here's the board with changeable difficulty : ")
print("")
difficulty_Board = grid_remove_diff(new_grid_2, 30) # new board with 30 clues, you can change this 
pprint.pprint(difficulty_Board)
print("Solvability check : ", solve_sudoku(difficulty_Board)) #checking solvability
print("")
print("Here's the solution to the board, don't peak! :")
pprint.pprint(difficulty_Board) # printing answer


# EXAMPLES: 
# Demonstrating that solve_sudoku works on 3 example cases: 
""" board #823, easy sudoku https://www.puzzles.ca/sudoku_puzzles/sudoku_easy_823.html
    board solution: https://www.puzzles.ca/sudoku_puzzles/sudoku_easy_823_solution.html 
""" 
test_1 = [
        [0, 6, 0,   0, 0, 0,   0, 7, 1],
        [0, 0, 0,   0, 0, 0,   3, 5, 8],
        [0, 2, 3,   0, 0, 0,   9, 0, 6],

        [0, 0, 0,   0, 0, 5,   0, 0, 0],
        [0, 0, 0,   9, 0, 0,   1, 0, 0],
        [0, 3, 4,   0, 0, 0,   7, 2, 0],

        [0, 0, 6,   0, 8, 4,   0, 0, 0],
        [7, 1, 0,   0, 0, 0,   0, 0, 0],
        [8, 4, 0,   0, 1, 3,   0, 0, 2]
    ]

""" board #817, hard sudoku https://www.puzzles.ca/sudoku_puzzles/sudoku_hard_817.html
    board solution: https://www.puzzles.ca/sudoku_puzzles/sudoku_hard_817_solution.html
""" 
test_2 = [
        [0, 0, 0,   2, 7, 0,   9, 0, 6],
        [0, 0, 5,   6, 0, 8,   0, 0, 0],
        [0, 0, 0,   0, 0, 0,   0, 0, 0],

        [0, 0, 6,   3, 0, 0,   0, 0, 8],
        [0, 0, 2,   0, 9, 0,   5, 0, 0],
        [0, 0, 0,   0, 0, 0,   0, 7, 1],

        [0, 8, 9,   0, 0, 0,   7, 0, 0],
        [0, 1, 0,   0, 0, 0,   8, 0, 9],
        [0, 0, 0,   0, 4, 0,   0, 5, 0]
    ]

# this is an unsolveable board, look at the first 2 elements of the board, they are both 2. this means no matter what this board can have no solution
# 2, 0, 0, 2 - there are 2 2's in the first row! not solvable!!
fail_test_row = [ 
        [2, 0, 0,   2, 7, 0,   9, 0, 6],
        [0, 0, 5,   6, 0, 8,   0, 0, 0],
        [0, 0, 0,   0, 0, 0,   0, 0, 0],

        [0, 0, 6,   3, 0, 0,   0, 0, 8],
        [0, 0, 2,   0, 9, 0,   5, 0, 0],
        [0, 0, 0,   0, 0, 0,   0, 7, 1],

        [0, 8, 9,   0, 0, 0,   7, 0, 0],
        [0, 1, 0,   0, 0, 0,   8, 0, 9],
        [0, 0, 0,   0, 4, 0,   0, 5, 0]
    ]

# if you look at the 4th column, there is a 2 in the 1st and 3rd row. 
fail_test_col = [ 
        [0, 0, 0,   2, 7, 0,   9, 0, 6],
        [0, 0, 5,   6, 0, 8,   0, 0, 0],
        [0, 0, 0,   2, 0, 0,   0, 0, 0],

        [0, 0, 6,   3, 0, 0,   0, 0, 8],
        [0, 0, 2,   0, 9, 0,   5, 0, 0],
        [0, 0, 0,   0, 0, 0,   0, 7, 1],

        [0, 8, 9,   0, 0, 0,   7, 0, 0],
        [0, 1, 0,   0, 0, 0,   8, 0, 9],
        [0, 0, 0,   0, 4, 0,   0, 5, 0]
    ]

# look at the 2nd subgrid, the subgrid in the top middle, 2 appears twice. 
fail_test_square = [ 
        [0, 0, 0,   2, 7, 0,   9, 0, 6],
        [0, 0, 5,   6, 0, 8,   0, 0, 0],
        [0, 0, 0,   0, 0, 2,   0, 0, 0],

        [0, 0, 6,   3, 0, 0,   0, 0, 8],
        [0, 0, 2,   0, 9, 0,   5, 0, 0],
        [0, 0, 0,   0, 0, 0,   0, 7, 1],

        [0, 8, 9,   0, 0, 0,   7, 0, 0],
        [0, 1, 0,   0, 0, 0,   8, 0, 9],
        [0, 0, 0,   0, 4, 0,   0, 5, 0]
    ]

# checking easy board 823's solvability, and printing solution
print("")
print("Running solve_sudoku on easy board 823 from puzzles.ca : ")
print(solve_sudoku(test_1))
print("Solution to easy board 823: ")
pprint.pprint(test_1) # check the solution on the website, they are the same!

# checking hard board 817's solvability, and printing solution
print("")
print("Running solve_sudoku on hard board 817 : ")
print(solve_sudoku(test_2))
print("Solution to hard board 817: ")
pprint.pprint(test_2) # same as solution from the website, again!

# checking solvability of unsolvable boards... 
print("")
print("Running solve_sudoku on fail_test_row : ")
print(solve_sudoku(fail_test_row))
print("")
print("Running solve_sudoku on fail_test_col : ")
print(solve_sudoku(fail_test_col))
print("")
print("Running solve_sudoku on fail_test_square : ")
print(solve_sudoku(fail_test_square))
print("")
print("Ta-dah! Try it on some other boards if you don't believe me still!")

