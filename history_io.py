from ast import literal_eval

PAIR_CUMUL_SIGN = " - "

def fetch_history():
    try:
        return _read_history()
    except FileNotFoundError:
        return _create_zero_history()

def increment_cumul_chosen_pairs(pairs):
    history = fetch_history()
    for pair in pairs:
        history[pair] = history[pair] + 1

    _store_pair_histories(history)

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
    for i, dev_i in enumerate(ALL_DEVS):
        for j in range(i+1,  len(ALL_DEVS)):
            pair = _create_pair(ALL_DEVS[i], ALL_DEVS[j])
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