import random
import string


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
    merged_dict = {}
    for i, dictionary in enumerate(list_of_dicts, start=1):
        for key, value in dictionary.items():
            if key in merged_dict:
                merged_dict[key] = max(merged_dict[key], value)
                if merged_dict[key] == value:
                    merged_dict[f'{key}_{i}'] = merged_dict.pop(key)
            else:
                merged_dict[key] = value
    return merged_dict


if __name__ == '__main__':
    random_dicts_list = generate_list_of_random_dicts()
    print(f'Initial List of random dicts: \n {random_dicts_list}')
    common_processed_dict = common_dict(random_dicts_list)
    print(f'Common processed dict: \n {common_processed_dict}')
