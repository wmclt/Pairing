from collections import defaultdict

PAIR_SPLIT_SIGN = ":"

def read_args(devs, args):
    pairs, leads = [], []
    options_with_values = _group_values_with_their_options(args)

    if "-h" in options_with_values:
        print_help()
        sys.exit(2)

    if "-a" in options_with_values:
        for dev in options_with_values["-a"]:
            devs.remove(dev)

    if "-s" in options_with_values:
        for dev in options_with_values["-s"]:
            pairs.append(tuple([dev]))
            devs.remove(dev)

    if "-l" in options_with_values:
        for dev in options_with_values["-l"]:
            leads.append(dev)
            devs.remove(dev)

    if "-r" in options_with_values:
        for pair_str in options_with_values["-r"]:
            pair = _parse_pair(pair_str)
            pairs.append(pair)
            for dev in pair:
                devs.remove(dev)

    return devs, pairs, leads

def _group_values_with_their_options(args):
    options_with_values = defaultdict(list)
    option = None
    for arg in args:
        if arg.startswith('--'):
            option = arg[1:3]
        if arg.startswith('-'):
            option = arg
        else:
            options_with_values[option].append(arg)

    return options_with_values


def _parse_pair(pair_str):
    return tuple(sorted(pair_str.split(PAIR_SPLIT_SIGN)))

def pretty_print(pairs):
    print("")
    for pair in pairs:
        print(_pair_str_repr(pair))


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
        -a|-absent [...]
        -s|--solo [...]
        -r|--remaining [...:...]
        -l|--lead [...]
        --help

    EXAMPLE:
        $ ./pairing.py --absent Wouter --lead Bert Michel --remaining Gilles:Luc
    """
    print(help_str)