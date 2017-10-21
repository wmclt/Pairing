#!/bin/env python3

#TODO
#
# don't use lib to parse cli arguments
# options:
#	-absent [...]
#	-alone [...]
#	-staying [...:...]
#   -lead [...] TODO two leads cannot go together
#	-help
#	-save [...:... || ...] TODO: ask if output good, if yes, save.
# 21 possible unique pairs for 7 people + 7 for being alone
# string representation pair sorted alphabetically: Wouter-Gilles -> Gilles-Wouter
# save chosen pairs: add +1 for each pair or alone

import sys
from random import choice
from collections import defaultdict
import ast

devs = ['Luc','Gilles','Bert','William','Johan','Wouter','Michel']
pairs = []
leads = []

def process_args(args):
    options_with_values = group_values_with_their_options(args)

    if "-help" in options_with_values:
        print_help()

    if "-absent" in options_with_values:
        for dev in options_with_values["-absent"]:        
            devs.remove(dev)        

    if "-alone" in options_with_values:
        for dev in options_with_values["-alone"]:        
            pairs.append(tuple([dev]))
            devs.remove(dev)

    if "-lead" in options_with_values:
        for dev in options_with_values["-lead"]:
            leads.append(dev)
            devs.remove(dev)
            
    if "-staying" in options_with_values:
        for pair_str in options_with_values["-staying"]:
            pair = parse_pair(pair_str)            
            pairs.extend(pair)        
            for dev in pair:
                devs.remove(dev)

    form_pairs()

def group_values_with_their_options(args):
    options_with_values = defaultdict(list)

    option = None
    for arg in args:
        if arg.startswith('-'):
            option = arg
        else:
            options_with_values[option].append(arg)

    return options_with_values

def form_pairs():
    # TODO take history (cumul) into account 
    # solution: just random() over partners with lowest cumul
    history = fetch_history()

    create_pairs_with_leads(history)
    
    create_pairs_without_leads(history)

def create_pairs_with_leads(history):
    while len(leads) > 0:
        lead = pop_random(leads)
        other = pop_random_least_paired_with(lead, history)
        pairs.append(create_pair(lead, other))

def create_pairs_without_leads(history):
    while len(devs) > 0:
	    one = pop_random(devs)
	    if len(devs) is 0: # last remaining dev
		    pairs.append((one))
	    else:
		    two = pop_random_least_paired_with(one, history)
		    pairs.append(create_pair(one,two))
    
def pop_random_least_paired_with(dev, history):
    pairs_with_dev = [pair for pair in history if dev in pair]

    # remove solos and pairs in which the partner is not in devs
    for pair in [p for p in pairs_with_dev]:
        #TODO HOW TAKE INTO ACCOUNT SOLO HISTORY?
        if len(pair) == 1:
            pairs_with_dev.remove(pair)
        else:
            other_d = get_other(pair, dev)
            if other_d not in devs:
                pairs_with_dev.remove(pair)

    minimum = 999999
    minimum_pairs = []
    for pair in pairs_with_dev:
        if history[pair] < minimum:
            minimum = history[pair]
            minimum_pairs = [pair]
        elif history[pair] == minimum:
            minimum_pairs.append(pair)
        else:
            pass

    chosen_pair = choice(minimum_pairs)
    other_dev = get_other(chosen_pair, dev)
    devs.remove(other_dev)
    return other_dev

def get_other(pair, dev):
    if dev == pair[0]:
        return pair[1]
    else:
        return pair[0]    

def fetch_history():
    try:
        return read_history()
    except FileNotFoundError:
        return create_zero_history()

global PAIR_CUMUL_SIGN
PAIR_CUMUL_SIGN = " - "

def read_history():
    pair_histories = {}
    reader = open("history.list","r")
    history = reader.read()
    for pair_history in history.split("\n"):
        if pair_history != "":
            pair_cumul = pair_history.split(PAIR_CUMUL_SIGN)
            pair_histories[ast.literal_eval(pair_cumul[0])] = int(pair_cumul[1])

    return pair_histories

def create_zero_history():
    pair_histories = {}
    for i, dev_i in enumerate(devs):
        for j in range(i+1,  len(devs)):
            pair = create_pair(devs[i], devs[j])
            pair_histories[pair] = 0
        pair_histories[tuple([dev_i])] = 0

    writer = open("history.list", "w")
    for pair in pair_histories:
        writer.write("{}{}{}\n".format(pair, PAIR_CUMUL_SIGN, pair_histories[pair]))
    writer.close()
    
    return pair_histories

def parse_pair(pair_str):
    return tuple(sorted(pair_str.split(":")))

def create_pair(dev_1, dev_2):
    return tuple(sorted([dev_1, dev_2]))

def pair_str_repr(pair):
    if type(pair) == str:
        return pair
    else:
        return "{}:{}".format(pair[0],pair[1])

def print_help():
    print("TODO: print help instructions")

def pop_random(people):
	return people.pop(people.index(choice(people)))

if __name__ == '__main__':
    process_args(sys.argv)
    
    #TODO ask if pairs alright, then save
    for pair in pairs:
        print(pair_str_repr(pair))
