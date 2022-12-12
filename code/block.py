import random


def prepare_block(block_info: list, randomize: bool) -> list:
    trials_list = []
    for elem in block_info:
        for i in range(elem["n_trials"]):
            trials_list.append({"n": elem["n_elements"], "size": elem["size"], "group_elements": elem["group_elements"]})
    if randomize:
        random.shuffle(trials_list)
    return trials_list

