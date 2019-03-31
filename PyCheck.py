from random import *
import threading
import _csv, csv
import sys


char_colors = ['y', 'g', 'b', 'r']
char_values = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'C', 'B', 'A']
alpha_values = ['C', 'B', 'A']
alpha_combos = []
bag = []
player_one = []
player_two = []
temp_p_one = []
temp_p_two = []
temp_rule_three = []
p_one = []
p_two = []
num_lines = sum(1 for line in open('Raw Data'))     # lines of data
sequence = []
content = []

def read_test_data():
    with open('Raw Data') as f:
        content = f.readlines()
    content = [x.strip().split(':') for x in content]  # pass entire data set into a string based list

    for line in content:
       player_one.append(line[0])
       player_two.append(line[1])

def create_alpha_counters():
    for v in alpha_values:  # creating the alpha counters
        for c in char_colors:
            alpha_combos.append(c + v)

def create_bag_of_counters():
    for v in char_values:  # creating the bag counters
        for c in char_colors:
            bag.append(c + v)

def view_player_counters(p_list):
    for line in p_list:
        print line

def view_all_counters(p_list):
    for player_draw in p_list:
        for counter in player_draw:
            print counter,

def view_player_counters_list(p_list):
    for i in range(len(p_list)):
        print p_list[i]

def rebuild_player_counters(p_list):
    temp_player = []
    for x in range(len(p_list)): # row numbers
        temp_player = [x.strip().split(',') for x in p_list]
    return temp_player

def create_empty_sequence():
    for x in range(num_lines): # row numbers
        sequence.append(0)

def view_sequence(seq):
    return "\nSequence =\t"+str(seq,)

def player_one_win(i):
    sequence[i] = 0

def player_two_win(i):
    sequence[i] = 1

def decide_temp_list(player, value):
    if player == 1:
        temp_p_one.append(value)
    elif player == 2:
        temp_p_two.append(value)

def split_list_for_rule_one(p_list):  # pass in list to split up for use by RULE 1
    if p_list[0][0] == "bA":    # determine the player (given data is known)
        player = 1
    elif p_list[0][0] == "r4":
        player = 2

    for b in range(len(p_list)):
        counted_alphas = 0
        temp_list = []
        for i in range(len(p_list[b])):
            if str(p_list[b][i][1]).isalpha():
             counted_alphas += 1
             temp_list.append(p_list[b][i])
        if counted_alphas == 0:  # switch replacement
            decide_temp_list(player, "LN")
        elif counted_alphas == 1:
            decide_temp_list(player, temp_list[0])
        else:
            decide_temp_list(player, "LM")

def lowest_single_letter(list1, list2):
    for x in range(num_lines):  # combinations for winning to be applied below
        if (list1[x] and list2[x]) in alpha_combos:  # 1 Letter vs 1 Letter
            if list1[x] > list2[x]:
                player_one_win(x)
            elif list1[x] < list2[x]:   # no need to compare for color alpha list compares based on index position
                player_two_win(x)
        else: # both not in the list - only need to compare for a 1 letter vs No letter
            if (list1[x] in alpha_combos) and (list2[x] is 'LN'): # player one wins
                player_one_win(x)
            elif (list2[x] in alpha_combos) and (list1[x] is 'LN'): # player two wins
                player_two_win(x)
        # skip anything involving 'LM' as multpies are to be ignored

def split_list_for_rule_two(p_list):  # pass in list to split up for use by RULE 2
    if p_list[0][0] == "bA":    # determine the player (given data is known)
        player = 1
    elif p_list[0][0] == "r4":
        player = 2

    for b in range(len(p_list)):
        total = 0      # begin changes here
        for i in range(len(p_list[b])):
            if p_list[b][i][1].isdigit(): # if the second char in the values is a number
                total += (int)(str(p_list[b][i])[1]) # add on the value that is the second character
        decide_temp_list(player, total)

def counter_sum_comparison(list1, list2):
    # pass in both lists
    for b in range(num_lines):  # NOT WORKING CORRECTLY - NEARLY
        val_one = 0
        val_two = 0
        if (list1[b] - 8) < 0:
            val_one = abs(list1[b] - 8) + 8 # Prob here
        elif(list1[b] - 8) >= 0:
            val_one = list1[b] - 8

        if (list2[b] - 8) < 0:
            val_two = abs(list2[b] - 8) + 8
        elif (list2[b] - 8) >= 0:
            val_two = list2[b] - 8

    for b in range(num_lines):
        if list1[b] != 0:
            list1[b] = abs(list1[b]-8)
        else:
            list1[b] = 8
        if list2[b] != 0:
            list2[b] = abs(list2[b] - 8)
        else:
            list2[b] = 8

    for b in range(num_lines):
        if list1[b] < list2[b]:
            player_one_win(b)
        elif list2[b] < list1[b]:
            player_two_win(b)
        # no need for an else as it will continue to comparison 3

def find_counters_index(value):
    index = 0
    for item in range(len(bag)):
        if value == bag[index]:
            return index
        index += 1

def split_list_for_rule_three(p_list):      # CHANGE ME !!!!!!!!!!!!
    if p_list[0][0] == "bA":    # determine the player (given data is known)
        player = 1
    elif p_list[0][0] == "r4":
        player = 2

    for b in range(len(p_list)):        # add counters from that specific draw to a temp list
        temp_list = []
        del temp_list[:]
        for i in range(len(p_list[b])):
            temp_list.append(p_list[b][i])  # created temp bag of drew counters

        # at this point that bag contains, 1 or 2 or 3 counters
        a = 0
        b = 0
        c = 0
        if len(temp_list) == 1:     # 1 counter to chose from
            decide_temp_list(player, temp_list[0])
        elif len(temp_list) == 2:   # compare A to B
            a = find_counters_index(temp_list[0])
            b = find_counters_index(temp_list[1])
            if a > b:
                decide_temp_list(player, temp_list[0])
            elif b > a:
                decide_temp_list(player, temp_list[1])
            # CANT BE DRAW EVER via this technique as bag gives an ordered index sized value
        elif len(temp_list) == 3:  # only option left is 3
            a = find_counters_index(temp_list[0])
            b = find_counters_index(temp_list[1])
            c = find_counters_index(temp_list[2])
            if (a > b) and (a > c):
                decide_temp_list(player, temp_list[0])
            elif (b > a) and (b > c):
                decide_temp_list(player, temp_list[1])
            elif (c > a) and (c > b):
                decide_temp_list(player, temp_list[2])
    # grab element with biggest index from list of counters, pass through to decide temp list

def single_highest_counter(list1, list2):
    temp_stored_p_1_indexes = []
    temp_stored_p_2_indexes = []
    for i in range(len(list1)): # convert each counter into a # vs # scenario where biggest wins
        temp_stored_p_1_indexes.append(find_counters_index(list1[i]))
        temp_stored_p_2_indexes.append(find_counters_index(list2[i]))

    for i in range(len(temp_stored_p_1_indexes)):
        if temp_stored_p_1_indexes[i] > temp_stored_p_2_indexes[i]:
            player_one_win(i)
        elif temp_stored_p_2_indexes[i] > temp_stored_p_1_indexes[i]:
            player_two_win(i)

def clear_temp_values():
    del temp_p_one[:]  # clearing the temp list 1
    del temp_p_two[:]  # clearing the temp list 2

def convert_the_sequence(seq):
    str_text = ""
    for i in range((len(seq))):
        str_text += str(seq[i])
    return str_text

def display_hidden_message(str_decrpt_me):
    secret_msg = ""

    return secret_msg

def __init__():
    read_test_data()
    create_empty_sequence()
    create_alpha_counters()
    create_bag_of_counters()

    p_one = rebuild_player_counters(player_one)
    p_two = rebuild_player_counters(player_two)

    print "\nPlayer 1 =", len(p_one), "=", p_one
    print "\nPlayer 2 =", len(p_two), "=", p_two
    print view_sequence(sequence)

    split_list_for_rule_one(p_one)                         # RULE 1
    split_list_for_rule_one(p_two)                         # RULE 1
    print "\n\nTemp P1 Rule 1 (P1) = ", temp_p_one,        # RULE 1
    print "\n\nTemp P2 Rule 1 (P2) = ", temp_p_two         # RULE 1
    lowest_single_letter(temp_p_one, temp_p_two)           # RULE 1
    print view_sequence(sequence)                          # RULE 1
    clear_temp_values()                                    # RULE 1

    split_list_for_rule_two(p_one)                         # RULE 2
    split_list_for_rule_two(p_two)                         # RULE 2
    print "\n\nTemp P1 Rule 2 (P1) = ", temp_p_one,        # RULE 2
    print "\n\nTemp P2 Rule 2 (P2) = ", temp_p_two         # RULE 2
    counter_sum_comparison(temp_p_one, temp_p_two)         # RULE 2
    print view_sequence(sequence)                          # RULE 2
    clear_temp_values()                                    # RULE 2

    print "\np_one : \t", p_one,
    print "\np_two : \t", p_two, "\n"

    split_list_for_rule_three(p_one)                       # RULE 3
    split_list_for_rule_three(p_two)                       # RULE 3
    print "\n\nTemp P1 Rule 3 (P1) = ", temp_p_one,        # RULE 3
    print "\n\nTemp P2 Rule 3 (P2) = ", temp_p_two         # RULE 3
    single_highest_counter(temp_p_one, temp_p_two)         # RULE 3
    print view_sequence(sequence)                          # RULE 3

    print bag,"\n"
    print convert_the_sequence(sequence)                   # converting binary to ASCII characters


t1 = threading.Thread(target=__init__())
t1.start()
t1.join()
