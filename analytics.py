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
    # general_stat_info()
    category_dict = count_identifier_in_category('Age')
    stat_category_info('Age', category_dict)

# Low level functions: Exploratory Analysis


def count_arrests(file='MO_Arrest_Data.txt'):
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


def count_identifier_in_category(category: str, file='MO_Arrest_Data.txt'):
    """


    :param category:
    :param file:
    :return:
    """
    # Example 'categories_age = {26: 1, 28: 5}'
    categories_age = {}
    categories_places = {}
    categories_date = {}
    categories_time = {}
    categories_county = {}
    categories_troop = {}
    with open(file, 'r') as opened_file:
        for line in opened_file:
            line_list = ast.literal_eval(line)
            if category == 'Age':
                # Add age to list of ages or add onto amount in specific age
                # if age is already in list
                if line_list[0] not in categories_age:
                    categories_age[line_list[0]] = 1
                else:
                    categories_age[line_list[0]] += 1
            elif category == 'Places':
                pass
            elif category == 'Date':
                pass
            elif category == 'Time':
                pass
            elif category == 'County':
                pass
            elif category == 'Troop':
                pass

    # Display data desired
    if category == 'Age':
        return categories_age
    elif category == 'Places':
        pass
    elif category == 'Date':
        pass
    elif category == 'Time':
        pass
    elif category == 'County':
        pass
    elif category == 'Troop':
        pass


def count_total_days_scraping(file='MO_Arrest_Data.txt'):
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


def stat_arrests_per_day():
    """
    A function to calculate the average arrests per day.

    :return: none
    :rtype: none
    """
    print(f'Mean arrests per day in MO: {count_arrests() / count_total_days_scraping():.2f} people.')


def stat_category_info(category: str, category_dict):
    if category == 'Age':
        print('Age\t\t| Amount')
        for key in sorted(category_dict):
            print(f'{key} yrs\t| {category_dict[key]} ppl')

# High level functions: Function usage


def general_stat_info():
    """
    A function that can be called to give general statistics on the historical data.

    :return: none, but other functions within thee will display information.
    :rtype: none
    """
    stat_arrests_per_day()


if __name__ == '__main__':
    main()
