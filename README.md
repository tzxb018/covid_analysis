# Covid Analysis 
![GitHub top language](https://img.shields.io/github/languages/top/tzxb018/covid_analysis?style=plastic)
![Size](https://img.shields.io/github/repo-size/tzxb018/covid_analysis?style=plastic)
![Issues](https://img.shields.io/github/issues/tzxb018/covid_analysis?style=plastic)
![Commit](https://img.shields.io/github/commit-activity/m/tzxb018/covid_analysis?style=plastic)

## Overview
This project for my CSCE 440 class analyzes the effectivness of the stay at home orders (SAHO) in each individual state in the United States. Taking information of the number of cases from the [John Hopkins Covid-19 repo](https://github.com/CSSEGISandData/COVID-19), I seperated the data into two sections, the data before the SAHO was issued, and the other after. I then used a cubic least square polynomial and a SIR model to fit a mathematical model to the data and used these models to analyze the effectivness of SAHOs to slow down the spread of COVID-19 in each state. The report for this project is called [Determining the Effectivness of the Stay At Home Orders with Different Models](https://github.com/tzxb018/covid_analysis/blob/master/Determining_the_Effectiveness_of_the_Stay_At_Home_Orders_with_Different_Models%20(1).pdf).

## Necessary Packages
To successfully run and use this repo, you will need to install the following packages.
- [Pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html) 
- [Datetime](https://pypi.org/project/DateTime/)
- [Numpy](https://numpy.org/doc/stable/)
- [Scipy.integrate](https://numpy.org/doc/stable/)
- [Matplotlib.pyplot](https://matplotlib.org/users/installing.html)
- [Csv](https://pypi.org/project/python-csv/)

## Under The Hood
Here is a lsit of the scripts that run in this project and what they do
- [driver.py](https://github.com/tzxb018/covid_analysis/blob/master/driver.py): This is the main class of the project. This takes informations from the helper classes and processes the information here and outputs the results.
- [getdata.py](https://github.com/tzxb018/covid_analysis/blob/master/getdata.py): This script takes information from the John Hopkins repo and returns the filtered out data for each state. This script also finds the day each state started their SAHOs and their total population.
- [least_square_approx.py](https://github.com/tzxb018/covid_analysis/blob/master/least_square_approx.py): This script is responsible for taking data and returning the best fit least square polynomial.
- [plot.py](https://github.com/tzxb018/covid_analysis/blob/master/plot.py): This script takes data and plots it accordingly. There are two types of plots this script will plot, one that compares the SIR models data to the actual reported data. The other compares the polynomial found in least_square_approx.py and compares it to the actual reported data. 
- [sir.py](https://github.com/tzxb018/covid_analysis/blob/master/sir.py): This script takes the actual reported data and finds the best fit SIR model for it. 

## Compiling
To run this project, one should first make sure that the John Hopkins Repo is updated. To do this, run the following script
```
cd ./COVID-19
git pull
cd ..
```
Once the information from the repo has been updated, compile and run the driver.py script. The script will output the graphs and tables into their respective csv files and graph images. 

## Outputting Results
When running the driver class, two csv files will be generated. The first one is called out.csv. This csv file will output the reproducitve rates of the virus before and after the SAHO for each state. The second is called results-from-cubic-fit.csv. This will output the average derivative and average second derivative from the cubic functions for each state before and after the SAHO.
4 graphs for each state will be generated into the graphs folder. 

- statename Before SAHO_polyfit.png: graph that plots the cubic least square polynomial and its derivative with the actual data before the SAHO. ![](https://github.com/tzxb018/covid_analysis/blob/master/graphs/New%20York%20Before%20SAHO_polyfit.png)

- statename After SAHO_polyfit.png: graph that plots the cubic least square polynomial and its derivative with the actual data after the SAHO.
![](https://github.com/tzxb018/covid_analysis/blob/master/graphs/New%20York%20After%20SAHO_polyfit.png)


- statename_pre.png: graph that plots the SIR model with the actual data before the SAHO. 
![](https://github.com/tzxb018/covid_analysis/blob/master/graphs/New%20York_pre.png)
- statename_post.png: graph that plots the SIR model with the actual data after the SAHO.
![](https://github.com/tzxb018/covid_analysis/blob/master/graphs/New%20York_post.png)
