import itertools


def swap_key_value(old_dict):
    """
    Creates a new dictionary swapping keys and values of an existing dictionary
    :param old_dict: the dictionary that has to be swapped
    :return: the new dictionary, obtained swapping keys and values
    """
    new_dict = {}
    for old_key, old_value in old_dict.items():
        new_dict[old_value] = old_key

    # print if some keys were overwritten during the process
    if len(new_dict) == len(old_dict):
        print("No keys were lost during the process")
    else:
        print("Some values were lost during the process")
    return new_dict


def find_dict_index_in_dict_list(lst, key, value):
    """
    Searches for a specific dictionary in a dictionary list based on the pair (key, value)
    and returns the index of the first element that matches.
    :param lst: the list of dictionaries
    :param key: the key that has to match with the given value
    :param value: the value that has to match
    :return: the index of the dictionary, if present. Otherwise returns -1.
    """
    for index, dic in enumerate(lst):
        if dic[key] == value:
            return index
    return -1


def merge_keys_in_dict_list(lst, keys_to_merge):
    """
    Converts a list of dictionaries in the form {'k1': 1, 'k2': 2, 'k3': '3'}
    in a list of dictionaries in the form {('k1', 'k2'): (1, 2), 'k3': 3}. It basically merges the keys passed as
    parameter in a tuple of keys (and does the same for the corresponding values), and leaves the remaining keys-values
    as they are given
    :param lst: the list of dictionaries
    :param keys_to_merge: the list of keys of the dictionaries that have to be merged in a single key (tuple)
    :return: the list of converted dictionaries
    """
    # {'x': 1, 'y': 1, 'type': 'A'} -> {('x', 'y'): (1, 1), 'type': 'A'}
    dst_list = []
    unmerged_keys = []
    merged_keys = keys_to_merge

    # save the keys that are not going to be merged
    list_sample = lst[0]
    for k in list_sample.keys():
        if k not in merged_keys:
            unmerged_keys.append(k)

    for d in lst:
        merged_values = []
        for mk in merged_keys:
            merged_values.append(d[mk])

        # update dst dictionary with the tuple of keys
        merged_dict = {tuple(merged_keys): tuple(merged_values)}

        # append the unmerged keys corresponding values
        for uk in unmerged_keys:
            merged_dict[uk] = d[uk]

        dst_list.append(merged_dict)
    return dst_list


def merge_dict_lists_with_priority(l1, l2, duplicates, priority, comparison_keys):
    """
    Merge two lists
    :param l1: the first list
    :param l2: the second list
    :param duplicates: allow duplicates if True
    :param priority: in case duplicates is set to False,
            indicates which list has the priority in case of duplicate value
    :param comparison_keys: the keys that have to be compared when merging the two lists
    :return: the two lists merged into one
    """
    dst_list = []

    if duplicates:  # simply append l2 to l1
        return [x for x in itertools.chain(l1, l2)]
    else:  # compare and merge with priority
        if priority != 2 and priority != 1:
            # unexpected parameter value
            raise ValueError
        else:  # priority parameter is correct
            comparison_tuple = tuple(comparison_keys)
            merged_l1 = merge_keys_in_dict_list(l1, comparison_keys)
            merged_l2 = merge_keys_in_dict_list(l2, comparison_keys)

            for ml1 in merged_l1:
                # since we update merged_l2 every time we have a match,
                # checking if it has any element can save a lot of time
                if len(merged_l2):
                    index = -1
                else:
                    index = find_dict_index_in_dict_list(merged_l2, comparison_tuple, ml1[comparison_tuple])

                if index != -1:  # there's a value that matches
                    ml2 = merged_l2[index]

                    # reconstruct the dictionaries
                    d1 = dict(zip(comparison_tuple, ml1[comparison_tuple]))
                    del ml1[comparison_tuple]
                    d1 = {**d1, **ml1}

                    d2 = dict(zip(comparison_tuple, ml2[comparison_tuple]))
                    del ml2[comparison_tuple]
                    d2 = {**d2, **ml2}

                    # replacing values according to priority
                    if priority == 1:  # the first dict wins
                        d = {**d2, **d1}
                    else:  # the second dict wins
                        d = {**d1, **d2}

                    # remove dicts from merged list to improve next searches
                    del merged_l2[index]
                else:  # no match in the solution dictionary
                    # reconstruct dictionary
                    d1 = dict(zip(comparison_tuple, ml1[comparison_tuple]))
                    del ml1[comparison_tuple]
                    d = {**d1, **ml1}

                # update destination list
                dst_list.append(d)
    return dst_list
