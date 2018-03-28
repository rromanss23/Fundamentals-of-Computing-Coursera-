"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
 
    result_list = []
    result_list_index = 0
    number_of_zeros = 0 
    
    for dummy_index in range(len(line)): # create an empty result list
        result_list.append(0)
            
    for dummy_value in line:  # slide all non-zero values to the left side
        if dummy_value != 0:
            result_list[result_list_index] = dummy_value
            result_list_index += 1  
            
    for dummy_index in range(len(result_list)-1):  # merge equal tiles and count the number of zeros
        if result_list[dummy_index] == result_list[dummy_index + 1]:
            result_list[dummy_index] *= 2
            result_list[dummy_index + 1] = 0 
            number_of_zeros += 1
    
    while number_of_zeros >= 0:
        for dummy_index in range(len(result_list)-1):  # slide all non-zero values to the left side one position for each
            if result_list[dummy_index] == 0:          # zero in the list (work a more efficient way)
                result_list[dummy_index] = result_list[dummy_index + 1]
                result_list[dummy_index + 1] = 0
        number_of_zeros -= 1
        
    return result_list


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.my_grid = []
        self.reset()
        self.limits = {UP : self.grid_height,
                         DOWN :self.grid_height,
                         LEFT : self.grid_width,
                         RIGHT : self.grid_width}
        self.border_index = {UP: [(0,col)for col in range(self.grid_width)] ,
                            DOWN: [(self.grid_height-1,col)for col in range(self.grid_width)],
                            LEFT: [(row,0)for row in range(self.grid_height)],
                            RIGHT: [(row,self.grid_width-1)for row in range(self.grid_height)]}

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # create a new board of HEIGHT X WIDTH dimensions
        self.my_grid = [[0 for dummy_col in range(self.grid_width)] for dummy_row in range(self.grid_height)]
        
        # add 2 initial tiles
        self.new_tile()
        self.new_tile()
        
        return self.my_grid

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        string_board = ""
        
        # iterates the board and add each row as a new character of the string
        for dummy_index in range(self.grid_height):
            string_board += str(self.my_grid[dummy_index][0:self.grid_width]) + "\n"
            
        return string_board

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.grid_width
    
    def make_list(self , start , direction , steps):
        """
        makes a list and return it
        """
        new_list = []
        for step in range(steps):
            row = start[0] + step * direction[0]
            col = start[1] + step * direction[1]
            new_list.append(self.my_grid[row][col])
        return new_list
    
    def modify(self , start , direction , steps , merged):
        """
        modifies the grid
        """
        for step in range(steps):
            row = start[0] + step * direction[0]
            col = start[1] + step * direction[1]
            self.my_grid[row][col] = merged[step]

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        
        changed = False
        steps = self.limits[direction]
        
        for dummy_index in self.border_index[direction]:
            temp_list = self.make_list(dummy_index, OFFSETS[direction], steps)
            merged = merge(temp_list)
            if temp_list != merged :
                changed = True
            self.modify(dummy_index, OFFSETS[direction], steps , merged)
        if changed:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
         
        # randomly selects a row and a column
        random_col = random.randrange(self.grid_width)
        random_row = random.randrange(self.grid_height)
        
        # if the square isn't empty, repeat the process until an empty one is selected
        while self.my_grid[random_row][random_col] != 0:
            random_col = random.randrange(self.grid_width)
            random_row = random.randrange(self.grid_height)
        
        # randomly select a number between 0 and 9
        random_tile = random.randrange(10) 
        
        # if the number is 9, the new tile's value is 4 (10% of the times)
        # in other case the new tile's value is 2 (90% of the times)
        if random_tile == 9:
            self.my_grid[random_row][random_col] = 4
        else:
            self.my_grid[random_row][random_col] = 2
        

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self.my_grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self.my_grid[row][col]
    

poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
