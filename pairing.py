#!/bin/env python3

# No libs used to parse cli arguments
# options:
#	-absent [...]
#	-alone [...]
#	-staying [...:...]
#   -lead [...]
#	-help
#	-save [...:... || ...] TODO
# Ask if output good, if yes, save.
# 21 possible unique pairs for 7 people + 7 for being alone
# string representation pair sorted alphabetically: 
#       Wouter-Gilles -> Gilles-Wouter
# save chosen pairs: add +1 for each pair or alone
# TODO Not same pairs as yesterday
# TODO pass devs, pairs, leads as arguments
# TODO if uneven, first deal with solo guy, then pairs
# TODO maybe notify if some pair/solo has been doing much more than the rest

import sys
from random import choice
from collections import defaultdict
from ast import literal_eval

PAIR_CUMUL_SIGN = " - "
PAIR_SPLIT_SIGN = ":"
AFFIRMATIONS = ('y','yes')
NEGATIONS = ('n','no')
ACCEPTABLE_RESPONSES = AFFIRMATIONS + NEGATIONS

def main():
    good_pairing_found = False
    args = sys.argv[1:]
    while not good_pairing_found:
        pairs = _create_pairing(args)

        print("")
        for pair in pairs:
            print(_pair_str_repr(pair))

        response = input("Is this pairing good? [Y/N]: ")
        while response.lower() not in ACCEPTABLE_RESPONSES:
            response = input("Is this pairing good? Please answer 'y[es]' or 'n[o]': ")
        good_pairing_found = True if response in AFFIRMATIONS else False

    _increment_cumul_chosen_pairs_in_history(pairs)

def _create_pairing(args):
    devs = ['Luc','Gilles','Bert','William','Johan','Wouter','Michel']
    leads, pairs = [], []
    options_with_values = _group_values_with_their_options(args)

    if "-help" in options_with_values:
        print_help()
        sys.exit(2)

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
            pair = _parse_pair(pair_str)
            pairs.append(pair)
            for dev in pair:
                devs.remove(dev)

    _form_pairs(devs, pairs, leads)
    
    return pairs

def _group_values_with_their_options(args):
    options_with_values = {}
    option = None
    for arg in args:
        if arg.startswith('-'):
            option = arg
            options_with_values[option] = []
        else:
            options_with_values[option].append(arg)

    return options_with_values

def _form_pairs(devs, pairs, leads):
    history = _fetch_history()

    _create_pairs_with_leads(devs, pairs, leads, history)

    _create_pairs_without_leads(devs, pairs, history)

def _create_pairs_with_leads(devs, pairs, leads, history):
    while len(leads) > 0:
        lead = _pop_random(leads)
        other = _pop_random_least_paired_with(lead, devs, history)
        pairs.append(_create_pair(lead, other))

def _create_pairs_without_leads(devs, pairs, history):
    if len(devs)%2 == 1:
        dev = _pop_random_least_alone(devs, history)        
        pairs.append((dev,))

    while len(devs) > 0:
	    one = _pop_random(devs)
	    two = _pop_random_least_paired_with(one, devs, history)
	    pairs.append(_create_pair(one,two))

def _pop_random_least_alone(devs, history):
    solo_cumuls = []
    for dev in devs:
        solo_cumuls.append(_get_solo_history(dev, history))
    
    minimum = 99999
    min_soloists = []
    for cumul in solo_cumuls:
        if cumul[1] < minimum:
            min_soloists = [cumul[0]]
            minimum = cumul[1]
        elif cumul[1] == minimum:
            min_soloists.append(cumul[0])
        else:
            pass

    chosen_dev = choice(min_soloists)
    devs.remove(chosen_dev)
    return chosen_dev

def _pop_random(people):
	return people.pop(people.index(choice(people)))

def _get_solo_history(dev, history):
    for pair in history:
        if dev in pair and len(pair) == 1:
            return (dev, history[pair])

def _pop_random_least_paired_with(dev, devs, history):
    pairs_with_dev = _get_pairs_with_dev_and_unchosen_partner(dev, devs, history)

    minimum_pairs = _find_minimum_pairs(history, pairs_with_dev)

    chosen_pair = choice(minimum_pairs)
    other_dev = _get_other(chosen_pair, dev)
    devs.remove(other_dev)
    return other_dev

def _get_pairs_with_dev_and_unchosen_partner(dev, devs, history):
    pairs_with_dev = []
    for pair in history:
        if len(pair) > 1 and dev in pair:
            other_dev = _get_other(pair, dev)
            if other_dev in devs:
                pairs_with_dev.append(pair)

    return pairs_with_dev

def _find_minimum_pairs(history, pairs_with_dev):
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
    return minimum_pairs

def _get_other(pair, dev):
    if dev == pair[0]:
        return pair[1]
    else:
        return pair[0]

def _fetch_history():
    try:
        return _read_history()
    except FileNotFoundError:
        return _create_zero_history

def _read_history():
    pair_histories = {}
    reader = open("history.list","r")
    history = reader.read()
    for pair_history in history.split("\n"):
        if pair_history:
            pair_cumul = pair_history.split(PAIR_CUMUL_SIGN)
            pair_histories[literal_eval(pair_cumul[0])] = int(pair_cumul[1])

    return pair_histories

def _create_zero_history():
    pair_histories = {}
    for i, dev_i in enumerate(devs):
        for j in range(i+1,  len(devs)):
            pair = _create_pair(devs[i], devs[j])
            pair_histories[pair] = 0
        pair_histories[tuple([dev_i])] = 0

    _store_pair_histories(pair_histories)
    return pair_histories

def _store_pair_histories(pair_histories):
    writer = open("history.list", "w")
    for pair in pair_histories:
        writer.write("{}{}{}\n".format(pair, PAIR_CUMUL_SIGN, pair_histories[pair]))
    writer.close()

def _parse_pair(pair_str):
    return tuple(sorted(pair_str.split(PAIR_SPLIT_SIGN)))

def _create_pair(dev_1, dev_2):
    return tuple(sorted([dev_1, dev_2]))

def _pair_str_repr(pair):
    if len(pair) == 1:
        return pair[0]
    else:
        return "{}{}{}".format(pair[0], PAIR_SPLIT_SIGN, pair[1])

def print_help():
    help_str = """
    COMMAND:
        ./pairing.py

    OPTIONS:
        -absent [...]
        -alone [...]
        -staying [...:...]
        -lead [...]
        -help

    EXAMPLE:
        $ ./pairing.py -absent Wouter -lead Bert Michel -staying Gilles:Luc
    """
    print(help_str)

def _increment_cumul_chosen_pairs_in_history(pairs):
    history = _fetch_history()
    for pair in pairs:
        history[pair] = history[pair] + 1

    _store_pair_histories(history)

if __name__ == '__main__':
    main()
