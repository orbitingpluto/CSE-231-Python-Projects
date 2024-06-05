########################################################################################################################
#
# CSE 231 Project 05 - Yu-Gi-Oh! Card Data Analyser
#
# Reads csv file
# Option 1: Check all cards - displays all card info & least/most/median expensive cards
# Option 2: Search cards - prompts for query and category to search, displays all matching card info
#           & least/most/median expensive cards
# Option 3: View decklist - prompts for decklist filename (ydk file) & displays all card info
#           & least/most/median expensive cards
#
########################################################################################################################


import csv
import math
from operator import itemgetter

MENU = "\nYu-Gi-Oh! Card Data Analysis" \
           "\n1) Check All Cards" \
           "\n2) Search Cards" \
           "\n3) View Decklist" \
           "\n4) Exit" \
           "\nEnter option: "

CATEGORIES = ["id", "name", "type", "desc", "race", "archetype", "card price"]


def open_file(prompt_str):
    '''
    repeatedly prompts user for a file until it is opened
    prompt_str: user-inputted file name (str)
    returns: a file pointer
    '''
    while True:
        try:
            fp = open(prompt_str, "r", encoding="utf-8")
            break
        except FileNotFoundError:
            print("\nFile not Found. Please try again!")
            prompt_str = input("\nEnter cards file name: ")
            continue
    return fp


def read_card_data(fp):
    '''
    creates list of tuples of all cards in deck
        reads csv file
                adds first seven values of each row to a list
            converted to a tuple, and added to another list
        list of tuples is sorted by price, then name.
    fp: file pointer to csv file
    returns: all cards (rows) and their first seven values (list of tuples)
    '''
    card_data = []
    reader = csv.reader(fp)
    next(reader, None)
    for individual_card in reader:
        one_card_list = []
        for index, element in enumerate(individual_card):
            if index <= 6:
                if index == 1:
                    element = element[:45]
                if index == 6:
                    element = float(element)
                one_card_list.append(element)
        one_card_tuple = tuple(one_card_list)
        card_data.append(one_card_tuple)
    card_data.sort(key=itemgetter(6, 1))  # sort first by price, then name
    return card_data


def read_decklist(fp, card_data):
    '''
    creates a list of cards in a decklist from card_data, given id numbers in a ydk file
    fp: file pointer to a csv file
    card_data: all cards in file (list of tuples)
    returns: cards in decklist (list of tuples)
    '''
    decklist_data = []
    next(fp, None)
    for id_num in fp:
        try:
            id_num = int(id_num)
        except ValueError:  # skips lines that are not id numbers
            continue
        for card in card_data:
            if id_num == int(card[0]):  # if card is in decklist
                decklist_data.append(card)
    decklist_data.sort(key=itemgetter(6, 1))  # sort first by price, then name
    return decklist_data


def search_cards(card_data, query, category_index):
    '''
    searches through the given category index in each card
        adds the card to a list if the query is present in the given category.
    card_data: all cards in file (list of tuples)
    query: phrase user is searching for (str)
    category_index: index of the category to search (int)
    returns: cards with the given query (list)
    '''
    found_cards = []
    for card in card_data:
        for index, element in enumerate(card):
            if index == category_index:
                if query in element:
                    found_cards.append(card)
    return found_cards


def compute_stats(card_data):  # passed test
    '''
    computes the maximum, minimum, and median price by creating a new list of all prices.
    then, compares each card's price with each value, and adds them to a new list if their price is the min, max, or med
    card_data: all cards in file (list of tuples)
    returns: cards with min price (list), min price (int), cards with max price (list), max price (int), cards with
    median price (list), median price (int)
    '''
    price_list = []

    # max and min price
    for card in card_data:
        for index, element in enumerate(card):
            if index == 6:
                price_list.append(element)
    min_price = min(price_list)
    max_price = max(price_list)

    # median price
    price_list_length = len(price_list)
    median_price = price_list[math.floor(price_list_length / 2)]

    # cards
    min_cards = []
    max_cards = []
    median_cards = []
    for card in card_data:
        for index, element in enumerate(card):
            if index == 6:
                if element == min_price:
                    min_cards.append(card)
                if element == max_price:
                    max_cards.append(card)
                if element == median_price:
                    median_cards.append(card)

    return min_cards, min_price, max_cards, max_price, median_cards, median_price


def display_data(card_data):
    '''
    displays the first 50 cheapest cards and their totals
    card_data: all cards in file (list of tuples)
    returns: nothing
    '''
    total = 0
    print("{:50s}{:30s}{:20s}{:40s}{:12s}".format('Name', 'Type', 'Race', 'Archetype', 'TCGPlayer'))
    for index, card in enumerate(card_data):
        if index <= 49:
            print("{:50s}{:30s}{:20s}{:40s}{:12.2f}".format(card[1], card[2], card[4], card[5], card[6]))
            total += card[6]
    print("\n{:50s}{:30s}{:20s}{:40s}{:12.2f}".format('Totals', '', '', '', total))


def display_stats(min_cards, min_price, max_cards, max_price, med_cards, med_price):
    '''
    displays the min, max, and med price and the cards that have those prices
    min_cards: cards with minimum price (list)
    min_price: minimum price of cards (int)
    max_cards: cards with maximum price (list)
    max_price: maximum price of cards (int)
    med_cards: cards with median price (list)
    med_price: median price of cards (int)
    returns: nothing
    '''
    print("\nThe price of the least expensive card(s) is {:,.2f}".format(min_price))
    for card in min_cards:
        print("\t{:s}".format(card[1]))
    print("\nThe price of the most expensive card(s) is {:,.2f}".format(max_price))
    for card in max_cards:
        print("\t{:s}".format(card[1]))
    print("\nThe price of the median card(s) is {:,.2f}".format(med_price))
    for card in med_cards:
        print("\t{:s}".format(card[1]))


def main():

    prompt_str = input("\nEnter cards file name: ")
    fp = open_file(prompt_str)
    card_data = read_card_data(fp)
    fp.close()

    option_input = 0
    while option_input != 4:

        # PROMPT FOR OPTIONS
        while True:
            option_input = input(MENU)
            try:
                option_input = int(option_input)
            except ValueError:  # if not number
                print("\nInvalid option. Please try again!")
                continue
            if option_input in range(1, 5):
                break
            else:  # if a number but not one of options
                print("\nInvalid option. Please try again!")
                continue

        # OPTION ONE
        if option_input == 1:

            number_of_cards = len(card_data)
            print("\nThere are {:d} cards in the dataset.".format(number_of_cards))
            display_data(card_data)
            min_card, min_price, max_card, max_price, med_card, med_price = compute_stats(card_data)
            display_stats(min_card, min_price, max_card, max_price, med_card, med_price)

        # OPTION TWO
        if option_input == 2:

            query = input("\nEnter query: ")

            # prompting for category until valid
            while True:
                category = input("\nEnter category to search: ")
                category = category.lower()
                if category in CATEGORIES:
                    for c in CATEGORIES:
                        if c == category:
                            category_index = CATEGORIES.index(c)
                    break
                else:
                    print("\nIncorrect category was selected!")
                    continue

            found_cards = search_cards(card_data, query, category_index)
            empty_list = []
            print("\nSearch results")
            if found_cards != empty_list:
                print("\nThere are {:d} cards with '{:s}' in the '{:s}' category."
                      .format(len(found_cards), query, category))
                display_data(found_cards)
                min_card, min_price, max_card, max_price, med_card, med_price = compute_stats(found_cards)
                display_stats(min_card, min_price, max_card, max_price, med_card, med_price)
            else:
                print("\nThere are no cards with '{:s}' in the '{:s}' category.".format(query, category))

        if option_input == 3:

            decklist_input = input("\nEnter decklist filename: ")
            decklist_fp = open_file(decklist_input)
            cards_in_decklist = read_decklist(decklist_fp, card_data)

            print("\nSearch results")
            display_data(cards_in_decklist)
            min_card, min_price, max_card, max_price, med_card, med_price = compute_stats(cards_in_decklist)
            display_stats(min_card, min_price, max_card, max_price, med_card, round(med_price, 2))

    print("\nThanks for your support in Yu-Gi-Oh! TCG")


if __name__ == "__main__":
    main()

