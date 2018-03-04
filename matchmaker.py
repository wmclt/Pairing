from random import choice


def form_pairs(history: dict, devs: list, pairs: list, leads: list) -> list:
    """Form pairs based on the history, the present devs, the pairs already 
    chosen and leads on stories."""
    _create_pairs_with_leads(devs, pairs, leads, history)
    _create_pairs_without_leads(devs, pairs, history)
    return pairs


def _create_pair(dev_1, dev_2):
    return tuple(sorted([dev_1, dev_2]))


def _create_pairs_with_leads(devs, pairs, leads, history):
    while len(leads) > 0:
        lead = _pop_random(leads)
        other = _pop_random_least_paired_with(lead, devs, history)
        pairs.append(_create_pair(lead, other))


def _create_pairs_without_leads(devs, pairs, history):
    if len(devs) % 2 == 1:
        dev = _pop_random_least_solo(devs, history)
        pairs.append((dev,))

    while len(devs) > 0:
        one = _pop_random(devs)
        two = _pop_random_least_paired_with(one, devs, history)
        pairs.append(_create_pair(one, two))


def _pop_random_least_solo(devs, history):
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
    pairs_with_dev = _get_pairs_with_dev_and_unchosen_partner(
        dev, devs, history)

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
