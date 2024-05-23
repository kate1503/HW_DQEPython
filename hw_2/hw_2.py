import random
import string
from collections import defaultdict


def generate_random_dict():
    # Random number of keys
    num_keys = random.randint(2, 3)
    # Random letters as keys
    keys = random.choices(string.ascii_lowercase, k=num_keys)
    values = [random.randint(0, 100) for _ in range(num_keys)]
    # Combine keys and values into a dictionary
    return dict(zip(keys, values))


def generate_list_of_random_dicts():
    num_dicts = random.randint(2, 10)
    # Random number of dictionaries in the list
    return [generate_random_dict() for _ in range(num_dicts)]


def common_dict(list_of_dicts):
    merged_dict = defaultdict(list)

    # Collect all unique keys and their values in merged_dict
    for num_dict, dictionary in enumerate(list_of_dicts):
        for key, value in dictionary.items():
            # Adding a tuple (dictionary_number, value) to the list corresponding
            # to the current key in the merged_dict
            merged_dict[key].append((num_dict, value))
    result_dict = {}
    for key, values in merged_dict.items():
        # Check if the current key is unique (it is unique if there is only one tuple in list)
        if len(values) == 1:
            result_dict[key] = values[0][1]
        else:
            # Find the tuple with max value for the current key
            max_value = max(values, key=lambda x: x[1])
            # Rename key and set max value
            result_dict[f'{key}_{max_value[0]}'] = max_value[1]
    return result_dict


if __name__ == '__main__':
    random_dicts_list = generate_list_of_random_dicts()
    print(f'Initial List of random dicts: \n {random_dicts_list}')
    common_processed_dict = common_dict(random_dicts_list)
    print(f'Common processed dict: \n {common_processed_dict}')
