# Tanner Fry
# tefnq2@mst.edu
#
import ast
import datetime
import pandas as pd
import time


def main():
    # TODO: Create analytics of the arrests for Missouri, whether it's specific
    # CONT: crimes in certain areas, how often crimes happen in MO, or other.
    # Categories: Age, Places, Date, Time, County, Troop
    category = 'Age'  # Change this to a specific category to receive new information
    display_stat_category_info(category, get_count_of_identifiers_in_category(category))
    display_general_stat_info()


# Low level functions: Exploratory Analysis


def get_arrests(file='MO_Arrest_Data.txt'):
    """
    A function to count the length of the arrest data file, which in turn gives
    us the arrest amount since the first given day.

    :param file: the specific file name with the historical data
    :type file: str
    :return: the amount of arrests in the file
    :rtype: int
    """
    arrest_count = 0

    with open(file, 'r') as opened_file:
        for _ in opened_file:
            arrest_count += 1

    return arrest_count


def get_count_of_identifiers_in_category(category: str, file='MO_Arrest_Data.txt'):
    """
    A function that returns a dict where the keys are specific variables within the observation and the values are the
    number of times that observation was counted in the data set.

    Example observation:
    ['40', 'THAYER,MO', '10/14/2019', '1:27PM', 'HOWELL', 'G']

    :param category: the desired variable from the observation to parse
    :type category: str
    :param file: the specific file name with the historical data
    :type file: str
    :return: a dict with the ages and the count for each age
    :rtype: dict
    """
    # Example of return values: 'key_val_dict  = {26: 1, 28: 5}'
    categories = {'Age': 0, 'Places': 1, 'Date': 2, 'Time': 3, 'County': 4, 'Troop': 5}
    observation_index = categories[category]
    key_val_dict = {}
    with open(file, 'r') as opened_file:
        for line in opened_file:
            line_list = ast.literal_eval(line)

            # Cleanse any data that needs to be cleansed
            if observation_index == 0:  # Don't need to cleanse data for age
                pass
            if observation_index == 1 or observation_index == 4:  # Cleanse data for Places and County
                if '.' in line_list[observation_index]:
                    line_list[observation_index] = line_list[observation_index].replace('.', '')
                if "'" in line_list[observation_index]:
                    line_list[observation_index] = line_list[observation_index].replace("'", ' ')
                # TODO: Add changing of state name to the state's abbreviation. Like 'Missouri' to 'MO'

            # Add key to list of keys or add onto amount in specific key
            # if key is already in list
            if line_list[observation_index] not in key_val_dict:
                key_val_dict[line_list[observation_index]] = 1  # Start counting the specific key
            else:
                key_val_dict[line_list[observation_index]] += 1  # Add onto the count for a given key

    return key_val_dict


def get_min_max_arrests_in_category(category_dict: dict):
    """
    A function to return the min and max value count of a given category.

    :param category_dict: the historical keys/values of a particular category
    :type category_dict: dict
    :return: two dicts in a list, the min and max value of the given category
    :rtype: list
    """
    min = {'': 999}
    min_key = ''
    max = {'': 1}
    max_key = ''
    for key in category_dict:
        if category_dict[key] > max['']:
            max[''] = category_dict[key]
            max_key = key
        if category_dict[key] < min['']:
            min[''] = category_dict[key]
            min_key = key

    min[min_key], max[max_key] = min.pop(''), max.pop('')

    return [min, max]


def get_total_days_scraping(file='MO_Arrest_Data.txt'):
    """
    A function to calculate the amount of days between the first observed
    and the last observed arrest.

    :param file: the specific file name with the historical data
    :type file: str
    :return: the amount of days the program has been collecting data
    :rtype: int
    """
    arrest_count = 0
    day_newest = 0
    day_oldest = 0
    days_counting_arrests = 0

    with open(file, 'r') as opened_file:
        for line in opened_file:
            if arrest_count == 0:
                day_newest = ast.literal_eval(line)[2]
            else:
                day_oldest = ast.literal_eval(line)[2]
            arrest_count += 1

    day_newest = str(day_newest.replace('/', ' '))
    day_oldest = str(day_oldest.replace('/', ' '))

    datetime_day_newest = datetime.datetime.strptime(day_newest, '%m %d %Y')
    datetime_day_oldest = datetime.datetime.strptime(day_oldest, '%m %d %Y')

    days_counting_arrests = datetime_day_newest - datetime_day_oldest
    return days_counting_arrests.days


def display_basic_stat_arrests():
    """
    A function to calculate the average arrests per day.

    :return: none
    :rtype: none
    """
    print(f'Total arrests: {get_arrests()} arrests')
    print(f'Total days counting: {get_total_days_scraping()} days')
    print(f'Mean arrests per day in MO: {get_arrests() / get_total_days_scraping():.2f} people.')


def display_stat_category_info(category: str, category_dict: dict):
    """
    A function to display formatted category info based on the category
    passed as a parameter.

    Example usage:
    display_stat_category_info('County', get_count_of_identifiers_in_category('County'))

    :param category: the desired variable from the observation to parse
    :type category: str
    :param category_dict: the historical keys/values of a particular category
    :type category_dict: dict
    :return: none
    :rtype: none
    """
    if category == 'Age':
        print('Age\t\t| Amount')
        for key in sorted(category_dict):
            print(f'{key} yrs\t| {category_dict[key]} arrest(s)')
    elif category == 'Places':
        print('Place\t\t| Amount')
        for key in sorted(category_dict):
            print(f'{key}\t| {category_dict[key]} arrest(s)')
    elif category == 'Date':
        print('Date\t\t| Amount')
        for key in sorted(category_dict):
            print(f'{key}\t| {category_dict[key]} arrest(s)')
    elif category == 'Time':
        print('Time\t\t| Amount')
        for key in sorted(category_dict):
            print(f'{key}\t| {category_dict[key]} arrest(s)')
    elif category == 'County':
        print('County\t\t| Amount')
        for key in sorted(category_dict):
            print(f'{key}\t| {category_dict[key]} arrest(s)')
    elif category == 'Troop':
        print('Troop\t| Amount')
        for key in sorted(category_dict):
            print(f'{key}\t\t| {category_dict[key]} arrest(s)')

    min, max = get_min_max_arrests_in_category(get_count_of_identifiers_in_category(category))
    print(f'Min: {min}\nMax: {max}')

# High level functions: Function usage


def display_general_stat_info():
    """
    A function that can be called to give general statistics on the historical data.

    :return: none, but other functions within thee will display information.
    :rtype: none
    """
    display_basic_stat_arrests()


if __name__ == '__main__':
    main()
