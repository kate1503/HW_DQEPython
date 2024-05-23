import random


def sort_list(num_list):
    n = len(num_list)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if num_list[j] < num_list[min_index]:
                min_index = j
        num_list[i], num_list[min_index] = num_list[min_index], num_list[i]
    return num_list


def avg_odd_even_list(num_list):
    odd_list = []
    even_list = []
    for i in num_list:
        if i % 2:
            odd_list.append(i)
        else:
            even_list.append(i)
    avg_odd_list = sum(odd_list) / len(odd_list)
    avg_even_list = sum(even_list) / len(even_list)
    print(f'Average for Odd numbers: {avg_odd_list}')
    print(f'Average for Even numbers: {avg_even_list}')


if __name__ == '__main__':
    # Create list of 100 random numbers from 0 to 1000
    random_numbers_list = [random.randint(0, 1000) for _ in range(100)]
    print(f'Initial list with 100 random numbers:  {random_numbers_list}')
    sorted_list = sort_list(random_numbers_list)
    print(f'Sorted list:  {sorted_list}')
    avg_odd_even_list(sorted_list)

