# Tanner Fry
# tefnq2@mst.edu
#
from bs4 import BeautifulSoup
from itertools import cycle, islice
import pandas as pd
import requests
import time


def main():
    data_rows = gather_data_from_MO_reports()
    display_data_rows(data_rows)

# DATA COLLECTION


def gather_data_from_MO_reports():
    """
    Obtains all of the rows and their columns of data from MO's arrest report.

    :return: list of rows from all the data sets
    """
    site = 'https://www.mshp.dps.missouri.gov/HP71/SearchAction'
    page = requests.get(site)
    soup = BeautifulSoup(page.content, 'html.parser')
    arrests_data1 = soup.find_all('td', class_='infoCell')  # 7 cols in a row
    # TODO: Incorporate the below arrest info under each arrest
    # arrests_info1 = soup.find_all('td', class_='infoCellPrint')
    # arrests_info2 = soup.find_all('td', class_='infoCell2Print')
    # print(arrests_info1[0].find('a').get('href'))
    arrests_data2 = soup.find_all('td', class_='infoCell2')  # 7 cols in a row
    arrests_data1_rows = []  # Used to aggregate all the columns of the data set for infoCell
    arrests_data2_rows = []  # Used to aggregate all the columns of the data set for infoCell2
    data_sets = [arrests_data1, arrests_data2]

    arrests_data1_rows = return_data_set_rows(arrests_data1)
    arrests_data2_rows = return_data_set_rows(arrests_data2)
    arrests_data_rows = roundrobin(arrests_data1_rows, arrests_data2_rows)

    return arrests_data_rows

# DATA DISPLAY


def display_data_rows(data_rows: list, filter_city=None, filter_date=None, filter_time=None, filter_county=None, filter_troop_id=None):
    arrest_age, arrest_city_state, arrest_date, arrest_time, arrest_county, arrest_troop_id = '', '', '', '', '', ''
    column_names = ['Age', 'City/State', 'Date', 'Time', 'County', 'Troop ID']
    data_filtered = []
    for row in data_rows:
        # Apply filters
        arrest_age = row[0]
        if filter_city is None:
            arrest_city_state = row[1]
        else:
            if filter_city.upper() == row[1]:
                arrest_city_state = row[1]
        if filter_date is None:
            arrest_date = row[2]
        else:
            if filter_date == row[2]:
                arrest_date = row[2]
        if filter_time is None:
            arrest_time = row[3]
        else:
            if filter_time.upper() == row[3]:
                arrest_time = row[3]
        if filter_county is None:
            arrest_county = row[4]
        else:
            if filter_county.upper() == row[4]:
                arrest_county = row[4]
        if filter_troop_id is None:
            arrest_troop_id = row[5]
        else:
            if filter_troop_id.upper() == row[5]:
                arrest_troop_id = row[5]

        # Only display data that has been filtered and pulled correctly
        if arrest_age != '' and arrest_city_state != '' and arrest_date != '' and arrest_time != '' and arrest_county != '' and arrest_troop_id != '':
            data_filtered.append([arrest_age, arrest_city_state, arrest_date, arrest_time, arrest_county, arrest_troop_id])
            # print(f'Age: {arrest_age}, City/State: {arrest_city_state}, Date: {arrest_date}, Time: {arrest_time}, '
            #       f'County: {arrest_county}, Troop ID: {arrest_troop_id}')

    print(pd.DataFrame(data=data_filtered, index=None, columns=column_names))

# TOOLS


def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    num_active = len(iterables)
    nexts = cycle(iter(it).__next__ for it in iterables)
    while num_active:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            # Remove the iterator we just exhausted from the cycle.
            num_active -= 1
            nexts = cycle(islice(nexts, num_active))


def return_data_set_rows(data_set):
    # Row builder, note: there are 7 columns in a row and we don't want the first column because
    # it contains the name of the individuals
    col_counter = 0
    rows = []
    row_info = []

    for arrest_col in data_set:
        col_counter += 1
        if col_counter > 1:
            row_info.append(arrest_col.get_text())
        if col_counter == 7:
            rows.append(row_info)
            row_info = []
            col_counter = 0

    return rows


if __name__ == '__main__':
    main()
