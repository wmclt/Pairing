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
# string representation pair sorted alphabetically: Wouter-Gilles -> Gilles-Wouter
# save chosen pairs: add +1 for each pair or alone
# TODO Not same pairs as yesterday
# TODO pass devs, pairs, leads as arguments

import sys
from random import choice
from collections import defaultdict
import ast

devs = ['Luc','Gilles','Bert','William','Johan','Wouter','Michel']
pairs = []
leads = []

PAIR_CUMUL_SIGN = " - "
AFFIRMATIONS = ('y','yes')
NEGATIONS = ('n','no')
ACCEPTABLE_RESPONSES = AFFIRMATIONS + NEGATIONS

def _process_args(args):
    options_with_values = _group_values_with_their_options(args)

    if "-help" in options_with_values:
        _print_help()
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

    _form_pairs()

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

def _form_pairs():
    history = _fetch_history()

    _create_pairs_with_leads(history)

    _create_pairs_without_leads(history)

def _create_pairs_with_leads(history):
    while len(leads) > 0:
        lead = _pop_random(leads)
        other = _pop_random_least_paired_with(lead, history)
        pairs.append(_create_pair(lead, other))

def _create_pairs_without_leads(history):
    while len(devs) > 0:
	    one = _pop_random(devs)
	    if len(devs) is 0: # last remaining dev
		    pairs.append((one))
	    else:
		    two = _pop_random_least_paired_with(one, history)
		    pairs.append(_create_pair(one,two))

def _pop_random_least_paired_with(dev, history):
    pairs_with_dev = _get_pairs_with_dev_and_unchosen_partner(dev, history)

    minimum_pairs = _find_minimum_pairs(history, pairs_with_dev)

    chosen_pair = choice(minimum_pairs)
    other_dev = _get_other(chosen_pair, dev)
    devs.remove(other_dev)
    return other_dev

def _get_pairs_with_dev_and_unchosen_partner(dev, history):
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
        if pair_history != "":
            pair_cumul = pair_history.split(PAIR_CUMUL_SIGN)
            pair_histories[ast.literal_eval(pair_cumul[0])] = int(pair_cumul[1])

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
    return tuple(sorted(pair_str.split(":")))

def _create_pair(dev_1, dev_2):
    return tuple(sorted([dev_1, dev_2]))

def _pair_str_repr(pair):
    if type(pair) == str:
        return pair
    else:
        return "{}:{}".format(pair[0],pair[1])

def _print_help():
    help_str = """
    options:
        -absent [...]
        -alone [...]
        -staying [...:...]
        -lead [...]
        -help

    Example:
        $ ./pairing.py -absent Wouter -lead Bert Michel -staying Gilles:Luc
    """
    print(help_str)

def _pop_random(people):
	return people.pop(people.index(choice(people)))

def _increment_cumul_chosen_pairs_in_history(pairs):
    history = _fetch_history()
    for pair in pairs:
        history[pair] = history[pair] + 1

    _store_pair_histories(history)

if __name__ == '__main__':
    good_pairing_found = False
    args = sys.argv[1:]
    while not good_pairing_found:
        devs = ['Luc','Gilles','Bert','William','Johan','Wouter','Michel']
        pairs = []
        leads = []
        _process_args(args)

        print("")
        for pair in pairs:
            print(_pair_str_repr(pair))

        response = input("Is this pairing good? [Y/N]: ")
        while response.lower() not in ACCEPTABLE_RESPONSES:
            response = input("Is this pairing good? Please answer 'y[es]' or 'n[o]': ")
        good_pairing_found = True if response in AFFIRMATIONS else False

    _increment_cumul_chosen_pairs_in_history(pairs)
