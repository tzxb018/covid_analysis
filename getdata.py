import csv
import os
import pandas as pd

frames = []
for filename in os.listdir('COVID Analysis\\COVID-19\\csse_covid_19_data\\csse_covid_19_daily_reports'):
    # making sure we are only reading the csv files
    if os.path.splitext(filename)[1] == '.csv':
        # print(os.path.splitext(filename)[0])

        # reading in the data from the csv file
        name = 'COVID Analysis\\COVID-19\\csse_covid_19_data\\csse_covid_19_daily_reports\\' + filename
        readin_data = pd.read_csv(name)

        # creating the dataframe for this date
        columns = ['Date', 'State', 'Confirmed', 'Deaths', 'Recovered']
        day_data_formatted = pd.DataFrame(columns=columns)

        # obtaining the date
        date = os.path.splitext(filename)[0]
        
        # getting the state (need to consider the two different formats of the csv *rolls eyes*)
        if 'Province/State' in readin_data:
            # data must be in the US
            day_data_from_readin_in_us = readin_data[(readin_data['Country/Region']=='US')] 

            # creating an array for each information and putting them into one collective data frame
            day_data_formatted['State'] =  day_data_from_readin_in_us['Province/State']
            day_data_formatted['Confirmed'] =  day_data_from_readin_in_us['Confirmed']
            day_data_formatted['Deaths'] = day_data_from_readin_in_us['Deaths']
            day_data_formatted['Recovered'] = day_data_from_readin_in_us['Recovered']
            day_data_formatted['Date'] = date

        elif 'Province_State' in readin_data:
            # data must be in the US
            day_data_from_readin_in_us = readin_data[(readin_data['Country_Region']=='US')] 

            # creating an array for each information and putting them into one collective data frame
            day_data_formatted['State'] =  day_data_from_readin_in_us['Province_State']
            day_data_formatted['Confirmed'] =  day_data_from_readin_in_us['Confirmed']
            day_data_formatted['Deaths'] = day_data_from_readin_in_us['Deaths']
            day_data_formatted['Recovered'] = day_data_from_readin_in_us['Recovered']
            day_data_formatted['Date'] = date
        
        frames.append(day_data_formatted)

covid_data = pd.concat(frames, ignore_index=True)
print(covid_data)

covid_data.to_csv('test.csv', index=True)

 
