What Arrest Reports does:
    - run.py scrapes police reports from the Missouri State Highway Patrol using functions within
      scrape_police_reprts.py.
    - Analytics.py reads all data from MO_Arrest_Data.txt to show mean arrests per day, arrests by filter, minimum and
      maximum arrests for a given filter, total arrests, and total days since scraping data.

Coding highlights:
    - display_stat_category_info in analytics.py can show arrests for each category that is gathered such as age,
      city/state, date, time, county, and troop id.
    - get_count_of_identifiers_in_category breaks down data read from MO_Arrest_Data.txt in order to count specifics
      for whatever category was passed as a parameter.
    - get_min_max_arrests_in_category goes through an already made category dict and determines the minimum and maximum
      values in that dict. The counts for those keys are in the dict so for example, no need to recount the number of
      times a 56 year old has been arrested.

NOTES:
    - The mean arrests per day could become skewed if the arrest report isn't running every day to pick up new arrests.
      This is because the Missouri State highway Patrol site only keeps the last 50 arrest records. This issue could be
      mitigated by looking at the latest arrest data recorded and seeing if there's a big enough gap between current
      data and the historic data.
    - Min and max need to give the appropriate labels so as to not mix up, say, age with the amount of arrests.