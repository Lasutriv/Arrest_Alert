# Tanner Fry
# tefnq2@mst.edu
#
from bs4 import BeautifulSoup
from itertools import cycle, islice
import datetime
import pandas as pd
import requests
import time

# Uses:
# 1. Auto check MO State Highway Patrol Arrest Reports page and pull data needed to update local database.
# 2. Single check on MO State Highway Patrol Arrest Reports
# 3.

# TODO: Get specific criminal activity from scraping and then create collection between arrest info and criminal activity
# CONT: Note: Create database table/key style logging


def main():
    # Test
    file_with_data = 'MO_Arrest_Data.txt'
    start_single_data_check(file_with_data)
    # start_auto_data_check(file_with_data, 3600)


# DATA MACHINE

def start_auto_data_check(file_with_data: str, update_time: int):
    """
    A function that automatically grabs data and compares against the report
    file to see if anything needs to be added.
    Note for update_time: 900 = 15mins, 1800 = 30mins, 3600 = 1hr

    :param file_with_data: the file to compare the gathered data against to see if entries are needed to be added
    :param update_time: the time between data grabs. Should be in seconds.
    :return: none
    """
    while True:
        data_rows = gather_data_from_mo_reports(file_with_data)
        if data_rows == '':
            exit()
        else:
            check_add_data_to_file(file_with_data, data_rows)

        time.sleep(update_time)  # Hr break between updates


def start_single_data_check(file_with_data: str):
    """
    A function to grab data and display the arrest results within the area of Missouri.

    :param file_with_data: the file to compare the gathered data against to see if entries are needed to be added
    :return: none
    """
    data_rows = gather_data_from_mo_reports(file_with_data)
    if data_rows == '':
        exit()
    else:
        check_add_data_to_file(file_with_data, data_rows)
        # filtered_data = filter_data_rows(data_rows)
        # display_data_rows(filtered_data)


def general_notification_push(update_time: int):
    """
    A function that pushes a notification if there is a new arrest report entry.

    Note for update_time: 900 = 15mins, 1800 = 30mins, 3600 = 1hr

    :param update_time: the time between data grabs. Should be in seconds.
    :return: none
    """
    # TODO: Make below.
    return


def specific_notification_push(update_time: int):
    """
    A function that checks any parameter passed against the report file
    to see whether or not a notification should be generated.

    Note for update_time: 900 = 15mins, 1800 = 30mins, 3600 = 1hr

    :param update_time: the time between data grabs. Should be in seconds.
    :return: none
    """
    # TODO: Make below.
    return

# DATA COLLECTION


def check_add_data_to_file(file_with_data: str, unfiltered_data: list):
    """
    A function to check and see if the gathered data should be added to the arrest data file.

    :param file_with_data: the file name where all MO arrest data sits
    :type file_with_data: str
    :param unfiltered_data: data from the MO arrest reports website
    :type unfiltered_data: list
    :return: none

    Example:
        data = get_data(file)

        if data empty:
            exit
        else:
            check_add_data_to_file(file, data)
    """
    read_lines = []
    write_lines = []
    # Gather data from file
    try:
        with open(file_with_data, 'r') as file:
            read_lines = file.readlines()
    except FileNotFoundError:
        file = open(file_with_data, 'w')
        file.close()

    # Compare file data with scraped data and add data that isn't in the file data
    if len(read_lines) is 0:
        for data in unfiltered_data:
            write_lines.append(data)
    else:
        for line in unfiltered_data:
            # Check to make sure the time is between 1-12, if larger than there's a storing issue from the website
            if int(line[3].split(':')[0]) / 12 > 1:
                break
            # Elements 2 and 3 in 'line' are 'date' and 'time'
            if line[2] in read_lines[0] and line[3] in read_lines[0]:
                break
            else:
                write_lines.append(line)

    # Add data from scraped that wasn't in file if there is data
    entry_count = 0
    if len(write_lines) is not 0:
        for line in write_lines:
            print('New line: ', line)
            entry_count += 1
        with open(file_with_data, 'w') as file:
            for line in write_lines:
                line = str(line) + '\n'
                file.write(line)
            for line in read_lines:
                file.write(line)

        print(f'File updated at {datetime.datetime.now()} with a total of {entry_count} entrie(s).')
    else:
        print(f'File not updated at {datetime.datetime.now()}.')


def gather_data_from_mo_reports(file_with_data: str):
    """
    A function that obtains all of the rows and their columns of data from MO's arrest report.

    :param file_with_data: the file to compare the gathered data against to see if entries are needed to be added
    :type file_with_data: str
    :return: list of rows from all the data sets
    """
    site = 'https://www.mshp.dps.missouri.gov/HP71/SearchAction'
    arrests_data_rows = []

    try:
        page = requests.get(site)
        soup = BeautifulSoup(page.content, 'html.parser')
        arrests_data1 = soup.find_all('td', class_='infoCell')  # 7 cols in a row
        # TODO: Incorporate the below arrest info under each arrest
        # arrests_info1 = soup.find_all('td', class_='infoCellPrint')
        # arrests_info2 = soup.find_all('td', class_='infoCell2Print')
        # print(arrests_info1[0].find('a').get('href'))
        # return
        arrests_data2 = soup.find_all('td', class_='infoCell2')  # 7 cols in a row
        arrests_data1_rows = []  # Used to aggregate all the columns of the data set for infoCell
        arrests_data2_rows = []  # Used to aggregate all the columns of the data set for infoCell2
        data_sets = [arrests_data1, arrests_data2]

        arrests_data1_rows = return_data_set_rows(arrests_data1)
        arrests_data2_rows = return_data_set_rows(arrests_data2)
        arrests_data_rows = roundrobin(arrests_data1_rows, arrests_data2_rows)

        return arrests_data_rows
    except requests.ConnectionError as excep:
        print('Connection error: ' + str(excep) + '\n\n' + 'Exiting.')
        exit()


# DATA DISPLAY

def display_data_rows(filtered_data: list):
    """
    Function used to display aggregated data from the Missouri Police Reports.

    :param filtered_data: collection of data rows, each row representing an arrest
    :return: none
    """
    column_names = ['Age', 'City/State', 'Date', 'Time', 'County', 'Troop ID']
    print(pd.DataFrame(data=filtered_data, index=None, columns=column_names))

# DATA FILTER


def filter_data_rows(data_rows: list, filter_age=None, filter_city=None, filter_date=None, filter_time=None, filter_county=None, filter_troop_id=None):
    """
    Function used to filter  aggregated data from the Missouri Police Reports
    website in a pandas dataframe view. The data can be filtered with many
    different variations.

    Inserted data looks like:

    Note: filter_age uses this syntax: filter_age='begin_int-end_int'

    :param data_rows: a list of rows that contain all of the spliced data from Missouri's police report website
    :param filter_age: a filter parameter to see either a range of ages or a specific age
    :param filter_city: a filter parameter to see arrests from specific cities
    :param filter_date: a filter parameter to see arrests from a specific date
    :param filter_time: a filter parameter to see arrests from a specific time
    :param filter_county: a filter parameter to see arrests from a specific county
    :param filter_troop_id: a filter parameter to see arrests from a specific highway patrol troop
    :return: list of data rows, each row representing an arrest
    """
    arrest_age, arrest_city_state, arrest_date, arrest_time, arrest_county, arrest_troop_id = '', '', '', '', '', ''
    data_filtered = []
    for row in data_rows:
        # Apply filters
        if filter_age is None:
            arrest_age = row[0]
        else:
            if '-' in filter_age:
                diced_ages = filter_age.split('-')
                diced_begin, diced_end = diced_ages[0], diced_ages[1]
                if int(diced_begin) <= int(row[0]) <= int(diced_end):
                    arrest_age = row[0]
            else:
                if filter_age == row[0]:
                    arrest_age = row[0]
        if filter_city is None:
            arrest_city_state = row[1]
        else:
            special_filter_city = filter_city + ', MO'
            if special_filter_city.upper() == row[1]:
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

        # Reset variables
        arrest_age, arrest_city_state, arrest_date, arrest_time, arrest_county, arrest_troop_id = '', '', '', '', '', ''

    return data_filtered

# TOOLS


def roundrobin(*iterables):
    """
    A tool used to intertwine lists in my scenario. Recipe credited to George Sakkis.

    :param iterables: lists, tuples, and strings are all iterables
    :return: combined iterable
    """
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
    # Row builder, noting there are 7 columns in a row and we don't want the first column because
    # it contains the name of the individuals
    col_counter = 0
    rows = []
    row_info = []

    # Note: We skip the very first row as it contains names. This is to abide
    # Note: by guidelines set from Missouri State Highway Patrol in an email
    # Note: chain exchange.
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
