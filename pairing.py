#!/usr/bin/env python3

# No libs used to parse cli arguments
# options:
#   -a|--absent [...]
#   -s|--solo [...]
#   -r|--remaining [...:...]
#   -l|--lead [...]
#   -h|--help
#   --history TODO? return history.list but sorted with highest cumul on top
#   --save [...:... || ...] TODO => just change history.list manually.
# Ask if output good, if yes, save.
# 21 possible unique pairs for 7 people + 7 for being solo
# string representation pair sorted alphabetically:
#       Wouter-Gilles -> Gilles-Wouter
# save chosen pairs: add +1 for each pair or solo
# If uneven, first deal with solo guy, then pairs

import sys

import bash_io
import history_io
import matchmaker
from config import ALL_DEVS

AFFIRMATIONS = ('y', 'yes')
NEGATIONS = ('n', 'no')
ACCEPTABLE_RESPONSES = AFFIRMATIONS + NEGATIONS


def main():
    good_pairing_found = False
    args = sys.argv[1:]

    while not good_pairing_found:
        history = history_io.fetch_history()
        devs, pairs, leads = bash_io.read_args([dev for dev in ALL_DEVS], args)

        pairs = matchmaker.form_pairs(history, devs, pairs, leads)

        bash_io.pretty_print(pairs)
        response = input("Is this pairing good? [Y/N]: ")
        while response.lower() not in ACCEPTABLE_RESPONSES:
            response = input(
                "Is this pairing good? Please answer 'y[es]' or 'n[o]': ")
        good_pairing_found = True if response in AFFIRMATIONS else False

    history_io.increment_cumul_chosen_pairs(pairs)


if __name__ == '__main__':
    main()
