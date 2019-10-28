# Tanner Fry
# tefnq2@mst.edu
# The main file to run scraping strategies and functions to gather the data.
import scrape_police_reports as spr

# Uses:
# 1. Auto check MO State Highway Patrol Arrest Reports page and pull data needed to update local database.
# 2. Single check on MO State Highway Patrol Arrest Reports
# 3.


def main():
    file_with_data = 'MO_Arrest_Data.txt'

    # start_single_data_check(file_with_data)
    spr.start_auto_data_check(file_with_data, 3600)


if __name__ == '__main__':
    main()
