#######################################
# CSE 231 Project 7 - Crossword Puzzle
#
# Contains functions to manage user interaction with crossword game program
#
# Open_puzzle opens puzzle from file
# Display_clues displays clues to user, with given specified number or default all
# Get_commands processes and validates user option commands
# Main handles flow of control of game based on logical process and user input
#
#######################################

from crossword import Crossword, Clue
import sys

HELP_MENU = "\nCrossword Puzzler -- Press H at any time to bring up this menu" \
            "\nC n - Display n of the current puzzle's down and across clues" \
            "\nG i j A/D - Make a guess for the clue starting at row i, column j" \
            "\nR i j A/D - Reveal the answer for the clue starting at row i, column j" \
            "\nT i j A/D - Gives a hint (first wrong letter) for the clue starting at row i, column j" \
            "\nH - Display the menu" \
            "\nS - Restart the game" \
            "\nQ - Quit the program"

OPTION_PROMPT = "\nEnter option: "
PUZZLE_PROMPT = "Enter the filename of the puzzle you want to play: "
PUZZLE_FILE_ERROR = "No puzzle found with that filename. Try Again.\n"

# def input( prompt=None ):
#     """
#         DO NOT MODIFY: Uncomment this function when submitting to Codio
#         or when using the run_file.py to test your code.
#         This function is needed for testing in Codio to echo the input to the output
#         Function to get user input from the standard input (stdin) with an optional prompt.
#         Args:
#             prompt (str, optional): A prompt to display before waiting for input. Defaults to None.
#         Returns:
#             str: The user input received from stdin.
#     """
#
#     if prompt:
#         print( prompt, end="" )
#     aaa_str = sys.stdin.readline()
#     aaa_str = aaa_str.rstrip( "\n" )
#     print( aaa_str )
#     return aaa_str

def open_puzzle():
    '''
    Opens and loads csv file and creates a new object. Accounts for invalid file
    :return: nothing
    '''
    while True:
        file = input(PUZZLE_PROMPT)
        try:
            puzzle_object = Crossword(file)
            return puzzle_object
        except FileNotFoundError:
            print(PUZZLE_FILE_ERROR)
            continue


def display_clues(puzzle_object, num_clues=0):
    '''
    Displays clues to user, depending on how many they want. Defaults to showing
    all clues, including at the beginning of the game
    :param puzzle_object: Crossword object representing current state of puzzle (obj)
    :param num_clues: Number of clues the user desires (int)
    :return: nothing
    '''
    # default to all clues
    if num_clues == 0:

        print("\nAcross")
        for k in puzzle_object.clues.keys():
            if puzzle_object.clues[k].down_across == "A":
                print(puzzle_object.clues[k])

        print("\nDown")
        for k in puzzle_object.clues.keys():
            if puzzle_object.clues[k].down_across == "D":
                print(puzzle_object.clues[k])

    # if user specifies number of clues
    else:

        # create list of down/across clues to iterate through,
        # for simple printing purposes
        across_clue_list = []
        down_clue_list = []
        for k in puzzle_object.clues.keys():
            if puzzle_object.clues[k].down_across == "A":
                across_clue_list.append(puzzle_object.clues[k])
            if puzzle_object.clues[k].down_across == "D":
                down_clue_list.append(puzzle_object.clues[k])

        print("\nAcross")
        for index, k in enumerate(across_clue_list):
            for i in range(num_clues):
                if index == i:
                    print(k)
                else:
                    continue

        print("\nDown")
        for index, k in enumerate(down_clue_list):
            for i in range(num_clues):
                if index == i:
                    print(k)
                else:
                    continue


def get_commands(puzzle_object, option_input):
    '''
    Validates user input and returns their input command. If invalid, returns None
    :param puzzle_object: Crossword object representing current state of puzzle (obj)
    :param option_input: User input command (str)
    :return:
    '''

    option_input = option_input.strip().upper()

    # C checks there is only one argument which is a positive integer
    if "C" in option_input:
        if len(option_input) == 3 and option_input[1] == " ":
            try:
                x = int(option_input[2])
                return option_input
            except ValueError:
                return None
        else:
            return None
    # H, S, Q checks there is no additional arguments
    elif "H" in option_input or "S" in option_input or "Q" in option_input:
        if len(option_input) > 1:
            return None
        else:
            return option_input
    elif "G" in option_input or "R" in option_input or "T" in option_input:
        if len(option_input) == 7:
            for i in range(7):
                if i % 2 != 0:  # odd index numbers (where spaces should be)
                    if option_input[i] != " ":
                        return None
            # checking first two arguments are numeric and positive
            if not option_input[2].isnumeric() and not option_input[4].isnumeric():
                return None
            if option_input[6] != "A" and option_input[6] != "D":  # checking for A/D
                return None
            # check if key exists
            x = int(option_input[2])
            y = int(option_input[4])
            indices_input = tuple([x, y])
            for k in puzzle_object.clues.keys():
                if indices_input != puzzle_object.clues[k].indices:
                    continue
                else:
                    for key in puzzle_object.clues.keys():
                        if indices_input == puzzle_object.clues[key].indices and option_input[6] == puzzle_object.clues[key].down_across:
                            return puzzle_object.clues[key]
        else:
            return None


def main():

    validated_option_input = None
    while validated_option_input != "Q":

        # beginning display
        puzzle_object = open_puzzle()
        num_clues = 0
        display_clues(puzzle_object, num_clues)
        print(puzzle_object)
        print(HELP_MENU)

        # while the input is invalid, to loop back through option prompt
        while validated_option_input is None:

            option_input = input(OPTION_PROMPT)
            validated_option_input = get_commands(puzzle_object, option_input)

            # if the input is valid
            if validated_option_input is not None:

                if "C" in option_input:
                    display_clues(puzzle_object, int(validated_option_input[2]))
                    # initialize back to None, so option prompt displays again
                    validated_option_input = None

                if "G" in option_input:
                    # prompt options again if invalid
                    if validated_option_input is None:
                        continue
                    else:
                        valid_guess = False
                        # validate guess
                        while not valid_guess:
                            try:
                                guess_input = input("Enter your guess (use _ for blanks): ")
                                Crossword.change_guess(puzzle_object, validated_option_input, guess_input)
                            except RuntimeError as message:
                                print(message)
                                continue
                            print(puzzle_object)
                            # initialize to True to break out of loop, to go back to valid options loop
                            valid_guess = True
                            validated_option_input = None

                if "R" in option_input:
                    if validated_option_input is None:
                        continue
                    else:
                        Crossword.reveal_answer(puzzle_object, validated_option_input)
                        print(puzzle_object)
                        validated_option_input = None

                if "T" in option_input:
                    if validated_option_input is None:
                        continue
                    else:
                        x = Crossword.find_wrong_letter(puzzle_object, validated_option_input)
                        if x >= 0:
                            print("Letter {} is wrong, it should be {}".format(x + 1, validated_option_input.answer[x]))
                        else:  # find_wrong_letter returns -1 if correct
                            print("This clue is already correct!")
                        validated_option_input = None

                if "H" in option_input:
                    print(HELP_MENU)
                    validated_option_input = None

                if option_input == "S":
                    # re-display beginning
                    puzzle_object = open_puzzle()
                    num_clues = 0
                    display_clues(puzzle_object, num_clues)
                    print(puzzle_object)
                    print(HELP_MENU)
                    validated_option_input = None

                # check if solved after every option
                x = Crossword.is_solved(puzzle_object)
                if x is True:
                    print("Puzzle solved! Congratulations!")
                    validated_option_input = "Q"
                else:
                    continue

            # if invalid, print message and prompt for option again
            else:
                print("Invalid option/arguments. Type 'H' for help.")
                continue


if __name__ == "__main__":
    main()