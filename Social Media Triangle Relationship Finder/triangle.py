####################################################################################################################
# CSE 231 Project 06 - Triangle Relationship Finder
#
# Program that takes, reads, and organizes a name file, friend id file, and friend file into a data structure
# (nested dictionary). Takes multiple user options to find information about the relationships and patterns
# between friend lists.
#
####################################################################################################################

import sys
import csv
import math
from operator import itemgetter


def input(prompt=None):
    if prompt:
        print(prompt, end="")
    aaa_str = sys.stdin.readline()
    aaa_str = aaa_str.rstrip("\n")
    print(aaa_str)
    return aaa_str


choices = '''
  Menu : 
     1: Max number of friends intersection between X and Facebook among all
     2: Percentage of people with no shared friends between X and Facebook
     3: Individual information
     4: Percentage of people with  more friends in X compared to Facebook
     5: The number of  triangle friendships in X
     6: The number of  triangle friendships on Facebook
     7: The number of  triangle friendships in X and Facebook together 
       Enter any other key(s) to exit

  '''


def open_file(input_file):
    '''
    Opens a file, accounts for error
    :param input_file: file to be opened (str)
    :return: fp (file pointer)
    '''
    try:
        fp = open(input_file, "r")
        return fp
    except FileNotFoundError:
        print("Error. File does not exist")


def make_dict(twt_friends_list, fb_friends_list, names_list, fp_name, fp_x, fp_fb):
    '''
    Makes nested dictionary {"Person": {'X': ['Friend']}, {'FB': ['Friends]}}, then closes each file
    :param twt_friends_list: list of lists of twitter friends (lst of lsts)
    :param fb_friends_list: list of lists of fb friends (lst of lsts)
    :param names_list: list of names (lst)
    :param fp_name: file pointer for name csv file
    :param fp_x: file pointer for twt friend id txt file
    :param fp_fb: file pointer for fb friend file
    :return:
    '''
    parent_dict = {}
    for i, name in enumerate(names_list):
        sub_dict = {}
        for index, individual_list in enumerate(twt_friends_list):
            if i == index:
                sub_dict['X'] = individual_list
                parent_dict[name] = sub_dict
        for index2, indiv_list in enumerate(fb_friends_list):
            if i == index2:
                sub_dict['FB'] = indiv_list
                parent_dict[name] = sub_dict
    close_file(fp_name)
    close_file(fp_x)
    close_file(fp_fb)
    return parent_dict


def read_names(fp_names):
    '''
    Reads CSV file and creates a list of all names in file.
    :param fp_names: Names csv file to be read (str)
    :return: List of all names (lst)
    '''
    name_lst = []
    for line in fp_names:
        name_lst.append(line.strip())
    return name_lst


def read_x_or_fb(fp):
    '''
    Creates list of lists of friends (one list of friends per line, each list is one person's friend list)
    Removes empty strings at end of lists (from twt id number txt file)
    :param fp: file pointer of file to be read
    :return: list of lists of friends (X and FB) from file (lst of lsts)
    '''
    friend_lst = []
    for friend in fp:
        friend = friend.strip()
        if friend != "":
            friend_lst.append(friend.split(","))
        if friend == "":
            friend_lst.append('')
    for item in friend_lst:  # removes empty str at end of each sublist
        if len(item) > 0:
            for person in item:
                if person == "":
                    item.remove(person)
    return friend_lst


def id_num_to_name(friend_lst, name_lst):
    '''
    Turns id numbers into names (for twt id number txt file)
    :param friend_lst: list of lists of friends (lst of lsts)
    :param name_lst: list of names (lst)
    :return: list of lists of friends
    '''
    for id_num_list in friend_lst:
        for i, id_num in enumerate(id_num_list):
            if id_num != '' and id_num.isnumeric():
                for index, name in enumerate(name_lst):
                    if int(id_num) == index:
                        id_num_list[i] = name
    return friend_lst


def close_file(fp):
    '''
    Closes file
    :param fp: file pointer
    :return: nothing
    '''
    fp.close()


def display_individual_info(name, friends_dict):
    '''
    Displays a inputted person's friends list from both X and FB
    :param name: inputted name to display info about (str)
    :param friends_dict: nested dictionary of each person and their friends on each platform (dict)
    :return: nothing
    '''
    twt_friends_lst = []
    fb_friends_lst = []
    print("-" * 14 + "\nFriends in X\n" + "*" * 14)
    for n in friends_dict.keys():
        if n == name:
            for friends in friends_dict[n]['X']:
                twt_friends_lst.append(friends)
                twt_friends_lst.sort()
            for friend in twt_friends_lst:
                print(friend, end="\n")
    print("-" * 20 + "\nFriends in Facebook\n" + "*" * 20)
    for n in friends_dict.keys():
        if n == name:
            for friends in friends_dict[n]['FB']:
                fb_friends_lst.append(friends)
                fb_friends_lst.sort()
            for friend in fb_friends_lst:
                print(friend, end="\n")


def max_intersect(friends_dict):
    '''
    Finds the maximum amount of intersections between friend lists through iteration, sets, and unions
    creates a list of intersections
    :param friends_dict: nested dictionary of each person and their friends on each platform (dict)
    :return: maximum number of intersections (int),
             list of intersections between friend lists (lst of sets)
    '''
    max_val = 0
    intersect_list = []
    for index, person in enumerate(friends_dict):
        if '' not in friends_dict[person]['X'] and '' not in friends_dict[person]['FB']:
            x = set(friends_dict[person]['X']) & set(friends_dict[person]['FB'])
            intersect_list.append(x)
            if len(x) > max_val:
                max_val = len(x)
    return max_val, intersect_list


def no_shared_friends(intersect_list):
    '''
    Counts all empty intersection sets, and this is the amount of people with no shared friends
    :param intersect_list: list of intersections (lst of sets)
    :return: amount of people with no shared friends (int)
    '''
    no_shared_total = 1
    empty_set = set()
    for intersection in intersect_list:
        if intersection == empty_set:
            no_shared_total += 1
    no_shared_percent = round((no_shared_total / len(intersect_list)) * 100)
    return no_shared_percent


def more_in_x_than_fb(friends_dict):
    '''
    Counts the length of each person's friends lists for each social media platform, compares them, and counts
    the amount of people who have more friends in X than FB
    :param friends_dict: nested dictionary of each person and their friends on each platform (dict)
    :return: percentage of people with more friends in X than FB (int)
    '''
    friends_in_x = 0
    friends_in_fb = 0
    more_in_x_val = 1
    for person in friends_dict:
        for x_friends_lst in friends_dict[person]['X']:
            friends_in_x = len(x_friends_lst)
        for fb_friends_lst in friends_dict[person]['FB']:
            friends_in_fb = len(fb_friends_lst)
        if friends_in_x > friends_in_fb:
            more_in_x_val += 1
    more_in_x_percent = math.ceil((more_in_x_val / len(friends_dict)) * 100)
    return more_in_x_percent


def triangle_friendships(friends_dict):
    '''
    Loops through each person, each of their friends, and each of that friend's friends and compares them to determine
    if they are a "triangle friendship" (if they are all friends with each other).
    :param friends_dict: nested dictionary of each person and their friends on each platform (dict)
    :return: the amount of triangle friendships in X (int), and FB (int)
    '''
    x_total = 0
    fb_total = 0
    for i in range(2):
        if i == 0:
            social_media = 'X'
        if i == 1:
            social_media = 'FB'
        for p1 in friends_dict:  # loop through all people in network
            for p2 in friends_dict[p1][social_media]:  # loop through all their friends
                for p3 in friends_dict[p2][social_media]:
                    if (p1 in friends_dict[p2][social_media] and p2 in friends_dict[p3][social_media] and
                            p1 in friends_dict[p3][social_media]):
                        if p1 != p3 and p2 != p3 and p1 != p2:
                            if i == 0:
                                x_total += 1
                            if i == 1:
                                fb_total += 1
                        else:
                            continue
    x_total = int(x_total / 6)  # I cant figure out how to fix the total being 6x more than it should be :(
    fb_total = int(fb_total / 6)
    return x_total, fb_total


def both_triangle_friendships(friends_dict):
    '''
    Loops through each person, the union of each of their friend lists, and the union of each of the friends in the
    first person's union, and compares them to determine if they are a "triangle friendship"
    (if they are all friends with each other).
    :param friends_dict: nested dictionary of each person and their friends on each platform (dict)
    :return: the amount of triangle friendships in both X and FB (int)
    '''
    total = 0
    for p1 in friends_dict:  # loop through all people in network
        for p2 in set(friends_dict[p1]['X']).union(friends_dict[p1]['FB']):  # loop through all their friends
            for p3 in set(friends_dict[p2]['X']).union(friends_dict[p2]['FB']):
                if (p1 in set(friends_dict[p2]['X']).union(friends_dict[p2]['FB']) and
                        p2 in set(friends_dict[p3]['X']).union(friends_dict[p3]['FB']) and
                        p1 in set(friends_dict[p3]['X']).union(friends_dict[p3]['FB'])):
                    if p1 != p3 and p2 != p3 and p1 != p2:
                        total += 1
    total /= 6
    return int(total)


def main():
    # prompting for name file
    while True:
        input_name_file = input("\nEnter a names file ~:")
        fp_name = open_file(input_name_file)
        if not fp_name:  # if open_file() does not return fp, reprompt
            continue
        else:
            names_lst = read_names(fp_name)
            break

    # prompting for X id file
    while True:
        input_x_file = input("\n\nEnter the twitter id file ~:")
        fp_x = open_file(input_x_file)
        if not fp_x:  # if open_file() does not return fp, reprompt
            continue
        else:
            twt_friends_list = read_x_or_fb(fp_x)
            twt_friends_list = id_num_to_name(twt_friends_list, names_lst)
            break

    # prompting for facebook id file
    while True:
        input_fb_file = input("\n\nEnter the facebook id file ~:")
        fp_fb = open_file(input_fb_file)
        if not fp_fb:  # if open_file() does not return fp, reprompt
            continue
        else:
            fb_friends_list = read_x_or_fb(fp_fb)
            break

    friends_dict = make_dict(twt_friends_list, fb_friends_list, names_lst, fp_name, fp_x, fp_fb)

    # prompting for options
    while True:
        print(choices)
        input_choice = input("Input a choice ~:")
        if not input_choice.isnumeric():
            print("Thank you")
            break
        else:
            if input_choice == '1':
                max_val, intersect_list = max_intersect(friends_dict)
                print("\nThe Max number intersection of friends between X and Facebook is: {}".format(max_val))
            if input_choice == '2':
                max_val, intersect_list = max_intersect(friends_dict)
                no_shared_percent = no_shared_friends(intersect_list)
                print("\n{}% of people have no friends in common on X and Facebook".format(no_shared_percent))
            if input_choice == '3':
                input_name = ''
                while input_name not in names_lst:
                    input_name = input("Enter a person's name ~:")
                    if input_name in names_lst:
                        display_individual_info(input_name, friends_dict)
                        break
                    else:
                        print("Invalid name or does not exist")
                        continue
            if input_choice == '4':
                percent_more_in_x = more_in_x_than_fb(friends_dict)
                print("{}% of people have more friends in X compared to Facebook".format(percent_more_in_x))
            if input_choice == '5':
                x_total, fb_total = triangle_friendships(friends_dict)
                print("The number of triangle friendships in X is: {}".format(x_total))
            if input_choice == '6':
                x_total, fb_total = triangle_friendships(friends_dict)
                print("The number of triangle friendships in Facebook is: {}".format(fb_total))
            if input_choice == '7':
                both_total = both_triangle_friendships(friends_dict)
                print("The number of triangle friendships in X merged with Facebook is:  {}".format(both_total))


if __name__ == '__main__':
    main()
