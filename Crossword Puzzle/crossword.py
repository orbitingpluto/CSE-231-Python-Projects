#######################################
# CSE 231 Project 7
#
# Contains Clue and Crossword classes to implement in a crossword puzzle game program
#
# Clue class represents an individual crossword clue and info about it
#
# Crossword class manages puzzle
#   Initializes puzzle from file
#   String representation of board
#   Loads puzzle from file and stores clue info with Clue
#   Updates user guess
#   Reveals individual answer specified by user
#   Identifies first wrong letter in a word specified by user
#   Determines if entire puzzle has been solved
#
#######################################

import csv

CROSSWORD_DIMENSION = 5

GUESS_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"


class Clue:
    def __init__(self, indices, down_across, answer, clue):
        """
        Puzzle clue constructor
        :param indices: row,column indices of the first letter of the answer
        :param down_across: A for across, D for down
        :param answer: The answer to the clue
        :param clue: The clue description
        """
        self.indices = indices
        self.down_across = down_across
        self.answer = answer
        self.clue = clue

    def __str__(self):
        """
        Return a representation of the clue (does not include the answer)
        :return: String representation of the clue
        """
        return f"{self.indices} {'Across' if self.down_across == 'A' else 'Down'}: {self.clue}"

    def __repr__(self):
        """
        Return a representation of the clue including the answer
        :return: String representation of the clue
        """
        return str(self) + f" --- {self.answer}"

    def __lt__(self, other):
        """
        Returns true if self should come before other in order. Across clues come first,
        and within each group clues are sorted by row index then column index
        :param other: Clue object being compared to self
        :return: True if self comes before other, False otherwise
        """
        return ((self.down_across,) + self.indices) < ((other.down_across,) + other.indices)


class Crossword:
    def __init__(self, filename):
        """
        Crossword constructor
        :param filename: Name of the csv file to load from. If a file with
        this name cannot be found, a FileNotFoundError will be raised
        """
        self.clues = dict()
        self.board = [['■' for _ in range(CROSSWORD_DIMENSION)] for __ in range(CROSSWORD_DIMENSION)]
        self._load(filename)

    def _load(self, filename):
        """
        Load a crossword puzzle from a csv file
        :param filename: Name of the csv file to load from
        """
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                indices = tuple(map(int, (row['Row Index'], row['Column Index'])))
                down_across, answer = row['Down/Across'], row['Answer']
                clue_description = row['Clue']
                clue = Clue(indices, down_across, answer, clue_description)

                key = indices + (down_across,)
                self.clues[key] = clue

                i = 0
                while i < len(answer):
                    if down_across == 'A':
                        self.board[indices[0]][indices[1] + i] = '_'
                    else:
                        self.board[indices[0] + i][indices[1]] = '_'
                    i += 1

    def __str__(self):
        """
        Return a string representation of the crossword puzzle,
        where the first row and column are labeled with indices
        :return: String representation of the crossword puzzle
        """
        board_str = '     ' + '    '.join([str(i) for i in range(CROSSWORD_DIMENSION)])
        board_str += "\n  |" + "-"*(6*CROSSWORD_DIMENSION - 3) + '\n'
        for i in range(CROSSWORD_DIMENSION):
            board_str += f"{i} |"
            for j in range(CROSSWORD_DIMENSION):
                board_str += f"  {self.board[i][j]}  "
            board_str += '\n'

        return board_str

    def __repr__(self):
        """
        Return a string representation of the crossword puzzle,
        where the first row and column are labeled with indices
        :return: String representation of the crossword puzzle
        """
        return str(self)

    def change_guess(self, clue, new_guess):  # fill out the parameters
        '''
        Updates crossword board for a new guess. Accounts for errors.
        :param clue: Clue for which the user is making a guess (obj)
        :param new_guess: User guess (str)
        :return: nothing
        '''
        new_guess = new_guess.strip().upper()

        for c in new_guess:
            if c in GUESS_CHARS:
                continue
            else:
                raise RuntimeError("Guess contains invalid characters.\n")

        if len(new_guess) != len(clue.answer):
            raise RuntimeError("Guess length does not match the length of the clue.\n")

        # iterate through rows and columns to check for appropriate indices
        for x, row in enumerate(self.board):
            for y, column in enumerate(row):
                if x == clue.indices[0] and y == clue.indices[1]:
                    for i, c in enumerate(new_guess):
                        # update board accounting for orientation
                        if clue.down_across == "D":
                            self.board[x + i][y] = c
                        else:
                            self.board[x][y + i] = c



    def reveal_answer(self, clue):  # fill out the parameters
        '''
        Reveals answer in position and orientation specified by user.
        :param clue: Clue for which the user wants the answer revealed (obj)
        :return: nothing
        '''
        for x, row in enumerate(self.board):
            for y, column in enumerate(row):
                if x == clue.indices[0] and y == clue.indices[1]:
                    for i, c in enumerate(clue.answer):
                        if clue.down_across == "D":
                            self.board[x + i][y] = c
                        else:
                            self.board[x][y + i] = c

    def find_wrong_letter(self, clue):  # fill out the parameters
        '''
        Reveals the position of an incorrect letter for a specific word.
        :param clue: Clue for which the user wants to be notified of an incorrect guess (obj)
        :return: index of the incorrect letter. -1 if all correct (int)
        '''
        current_answer = ''
        for x, row in enumerate(self.board):
            for y, column in enumerate(row):
                if x == clue.indices[0] and y == clue.indices[1]:
                    if clue.down_across == "D":

                        # determines user's current answer
                        for x2, row2 in enumerate(self.board):
                            for y2, column2 in enumerate(row2):
                                if y2 == clue.indices[1]:
                                    if column2 == "■":
                                        continue
                                    current_answer += column2

                        # finds position of incorrect letter
                        for i, c in enumerate(current_answer):
                            for index, char in enumerate(clue.answer):
                                if current_answer == clue.answer:
                                    return -1
                                if index == i:
                                    if char != c:
                                        return index

                    if clue.down_across == "A":

                        # determines user's current answer
                        for x2, row2 in enumerate(self.board):
                            for y2, column2 in enumerate(row2):
                                if x2 == clue.indices[0]:
                                    if column2 == "■":
                                        continue
                                    current_answer += column2

                        # finds position of incorrect letter
                        for i, c in enumerate(current_answer):
                            for index, char in enumerate(clue.answer):
                                if current_answer == clue.answer:
                                    return -1
                                if index == i:
                                    if char != c:
                                        return index

    def is_solved(self):  # fill out the parameters
        '''
        Determines if the puzzle is fully solved.
        :return: False if not solved, True if solved (bool)
        '''
        for k in self.clues.keys():
            # iterates through all words
            column = self.clues[k].indices[1]
            row = self.clues[k].indices[0]
            # compares all words to current board
            for letter in range(len(self.clues[k].answer)):
                if self.clues[k].down_across == "D":
                    if self.board[row + letter][column] == self.clues[k].answer[letter]:
                        pass  # do nothing if correct
                    else:
                        return False  # if incorrect, stop function and return False
                elif self.clues[k].down_across == "A":
                    if self.board[row][column + letter] == self.clues[k].answer[letter]:
                        pass  # do nothing if correct
                    else:
                        return False  # if incorrect, stop function and return False
                else:
                    pass
        # if correct, return True
        return True
