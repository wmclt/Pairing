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

    # TODO first takes leads into account
    
    # TODO remove
    for key in history:
        print("{}:{}".format(key, history[key]))
    
    while len(devs) > 0:
	    one = select_random(devs)
	    if len(devs) is 0:
		    pairs.append((one))
	    else:
		    two = select_random(devs)
		    pairs.append((one,two))
    

def fetch_history():
    #try:
    #    return read_history()
    #except FileNotFoundError:
    return create_zero_history()

def read_history():
    pair_histories = {}
    reader = open("history.list","r")
    history = reader.read()
    for pair_history in history.split("\n"):
        pair_cumul = pair_history.split(" ")
        pair_histories.append(pair_cumul[0], pair_cumul[1])

    return pair_histories

def create_zero_history():
    pair_histories = {}
    for i, dev_i in enumerate(devs):
        for j in range(i+1,  len(devs)):
            pair = create_pair(devs[i], devs[j])
            pair_histories[pair] = 0
        pair_histories[tuple([dev_i])] = 0
    
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

def select_random(remaining):
	return remaining.pop(remaining.index(choice(remaining)))

if __name__ == '__main__':
    process_args(sys.argv)
    
    for pair in pairs:
        print(pair_str_repr(pair))
