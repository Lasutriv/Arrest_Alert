# Tanner Fry
# tefnq2@mst.edu
#
import ast
import datetime
import pandas as pd
import time


def main():
    # TODO: Create analytics of the arrests for Missouri, whether it's specific crimes in certain areas,
    # CONT: how often crimes happen in MO, or other.
    stat_arrests_per_day()


def count_arrests(file='MO_Arrest_Data.txt'):
    arrest_count = 0

    with open(file, 'r') as opened_file:
        for _ in opened_file:
            arrest_count += 1

    return arrest_count


def count_total_days_scraping(file='MO_Arrest_Data.txt'):
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


def auto_stat_info():
    pass


def stat_arrests_per_day():
    print(f'Mean arrests per day: {count_arrests() / count_total_days_scraping()}')


if __name__ == '__main__':
    main()
