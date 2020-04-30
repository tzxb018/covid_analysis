import csv
import os
import pandas as pd
from datetime import date, datetime, timedelta


def getDataFromUS():
    frames = []
    for filename in os.listdir(
        ".\\COVID-19\\csse_covid_19_data\\csse_covid_19_daily_reports"
    ):
        # making sure we are only reading the csv files
        if os.path.splitext(filename)[1] == ".csv":

            # reading in the data from the csv file
            name = (
                ".\\COVID-19\\csse_covid_19_data\\csse_covid_19_daily_reports\\"
                + filename
            )
            readin_data = pd.read_csv(name)

            # creating the dataframe for this date
            columns = ["Date", "State", "Confirmed", "Deaths", "Recovered"]
            day_data_formatted = pd.DataFrame(columns=columns)

            # obtaining the date
            date = os.path.splitext(filename)[0]

            # getting the state (need to consider the two different formats of the csv *rolls eyes*)
            if "Province/State" in readin_data:
                # data must be in the US
                day_data_from_readin_in_us = readin_data[
                    (readin_data["Country/Region"] == "US")
                ]

                # creating an array for each information and putting them into one collective data frame
                day_data_formatted["State"] = day_data_from_readin_in_us[
                    "Province/State"
                ]
                day_data_formatted["Confirmed"] = day_data_from_readin_in_us[
                    "Confirmed"
                ]
                day_data_formatted["Deaths"] = day_data_from_readin_in_us["Deaths"]
                day_data_formatted["Recovered"] = day_data_from_readin_in_us[
                    "Recovered"
                ]
                day_data_formatted["Date"] = date

            elif "Province_State" in readin_data:
                # data must be in the US
                day_data_from_readin_in_us = readin_data[
                    (readin_data["Country_Region"] == "US")
                ]

                # creating an array for each information and putting them into one collective data frame
                day_data_formatted["State"] = day_data_from_readin_in_us[
                    "Province_State"
                ]
                day_data_formatted["Confirmed"] = day_data_from_readin_in_us[
                    "Confirmed"
                ]
                day_data_formatted["Deaths"] = day_data_from_readin_in_us["Deaths"]
                day_data_formatted["Recovered"] = day_data_from_readin_in_us[
                    "Recovered"
                ]
                day_data_formatted["Date"] = date

            frames.append(day_data_formatted)

    covid_data = pd.concat(frames, ignore_index=True)

    return covid_data


# using the information from the function above, this will return a data frame that has the infomration regarding one state only
def filterDataForState(state_name, state_abb, data):
    state_data = data[
        (data["State"].str.contains(state_name)) | data["State"].str.contains(state_abb)
    ]
    # state_data.to_csv("test.csv", index=True)
    # print(state_data)
    return state_data


# combining all the data for the days after the given parameter
def filterDataByDate(df, start_date):
    # converting the start date into datetime object
    datetime_object = datetime.strptime(start_date, "%m/%d/%Y").date()
    df["Date"] = pd.to_datetime(df["Date"])
    grouped = df.groupby(["Date"]).sum()

    # going through each row and combining the data for each date that is after the start date
    date_data = []
    for name, group in df.groupby("Date"):
        if name >= datetime_object - timedelta(days=14):
            date_info = [
                name,
                group["Confirmed"].sum(),
                group["Deaths"].sum(),
                group["Recovered"].sum(),
            ]
            date_data.append(date_info)
    date_df = pd.DataFrame(
        data=date_data, columns=["Date", "Confirmed", "Deaths", "Recovered"],
    )

    # updating the recovered numbers by taking the confirmed cases from 14 days the current day and using 97.5% of that number to get the recovered data for that day
    for i in date_df.index:
        if i < len(date_df) - 14:
            confirmed_14_days_ago = date_df["Confirmed"][i]
            date_df["Recovered"][i + 14] = confirmed_14_days_ago * 0.975

    # removing the first 14 days, as those were used to calcualte the recovered cases of the data we need to be returned
    return_df = date_df.drop(list(range(0, 14)))
    return_df.reset_index(inplace=True, drop=True)

    return return_df


# from an excel file, this will get the total population of a state
def getPopulationForState(state_name):
    state_info = pd.read_csv(".\\state_population_data.csv")
    state_pop = state_info.loc[(state_info["State"] == state_name), "Pop"].iloc[0]
    return state_pop


# data for when each state has ordered their stay at home orders
def getDateOfStartOfOrder(state_name):
    stay_at_home = pd.read_csv(".\\state_stay_at_home_orders_dates.csv")
    if state_name in stay_at_home.State.values:
        state_date = stay_at_home.loc[
            (stay_at_home["State"] == state_name), "Effective Date"
        ].iloc[0]
        return state_date
    else:
        return None
