# Paris DeepAir Project

Le Wagon - Bootcamp Data Science - Paris - Full time

Batch #1002 - 03/10-09/12/2022

------------------------------------------------

## Context

Paris DeepAir Project is an end-of studies project carried-out by 4 students from [Le wagon data science school](https://www.lewagon.com/data-science-course). The goal of this project is to predict the air quality in Paris on a horizon of 7 days, using time series with machine learning & deep learning, based on data from [Airparif](https://www.airparif.asso.fr/), the official air quality monitoring agency for Île-de-France region.


The Paris DeepAir Project is a fascinating capstone project that involves the use of time series, machine learning, and deep learning techniques to forecast air quality in Paris over the next seven days. The project was undertaken by four students from Le Wagon Data Science School, and its objective is to provide accurate and reliable air quality forecasts to the residents of Paris.

To accomplish this objective, the students first collected data from Airparif, the official air quality monitoring organization in the region. They then processed and cleaned the data, removing any missing or erroneous values and transforming it into a format that could be used for machine learning and deep learning models.

Next, the students explored various time series models, including ARIMA, Prophet, and LSTM, to determine which approach would be most effective for forecasting air quality. They then trained and tested these models using historical air quality data and compared their performance to identify the best-performing model.

After selecting the best-performing model, the students deployed it to a web application, allowing users to access air quality forecasts for the next seven days. The application provides a user-friendly interface that displays air quality data in an easy-to-understand format and allows users to customize the location and time range for the forecast.

Overall, the Paris DeepAir Project is an impressive example of how data science and machine learning techniques can be used to address real-world problems. The project's ability to provide accurate and reliable air quality forecasts can help improve public health outcomes and promote a cleaner environment in Paris.

------------------------------------------------

## Preliminary steps to carry-out

**Local repo setup:**
- Clone the project
- Create a virtual environment for this project named "PDPA-virt_env"
- Assign this virtual environment to the project
- Run the virtual environment into the local repo
- Into the CLI type:
```shell
make reinstall_package
```


**Data & files:**
- Download & paste the "data" folder into the local cloned version of the repo
- Create a ".env" file


**Jupyter notebook setup - to be done on CLI:**
```shell
# Install nbextensions
jupyter contrib nbextension install --user
jupyter nbextension enable toc2/main
jupyter nbextension enable collapsible_headings/main
jupyter nbextension enable spellchecker/main
jupyter nbextension enable code_prettify/code_prettify
```

------------------------------------------------

## Folder structure

**Folders description:**
- **data**: all data used for this project (5 years on an hourly basis)
- **documentation**: all the technical documentation consulted for this project
- **model_greykite**: ML models for each pollution cluster
- **notebooks**: individual notebooks for this project
- **workflow**: all the workflow for our model, divided in .py files

------------------------------------------------

## Dataset description

**Pollutants (French / English) in the ATMO  index:**
- **PM 2,5**: particules fines / fine particles
- **PM 10**: particules moyennes / medium particles
- **NO2**: dioxyde d'azote / nitrogen dioxide
- **O3**: ozone / ozone
- **SO2**: dioxyde de souffre / sulfur dioxide

Pollutants measured but not-included in the ATMO index - dropped :
- **CO**: monoxyde de carbone / carbon monoxide
- **NO**: monoxyde d'azote / nitrogen monoxide
- **NOX**: oxydes d'azote / nitrogen oxydes


Measure unit for all pollutants : mg/m3


In this project, 20 stations were selected (Paris intra-muros). All pollutants are not monitored in every station, each station is specialized in several pollutants. In total, there are :
- **NO2**: 20 stations
- **PM10**: 11 stations
- **PM2.5**: 6 stations
- **O3**: 5 stations
- **SO2**: 4 stations

Then, data from these 20 stations was grouped into 5 clusters : West, East, North, South, Center

------------------------------------------------

## ATMO Index

The ATMO index is a daily indicator of air quality, calculated from concentration into the air of regulated pollutant. This index classifies air quality into 6 classes (from good to extremely bad).

First, a sub-ATMO index is calculated for each regulated air pollutant, then a global ATMO index is calulated from these sub-ATMO indexes. The global ATMO index is equal to the worst classification of sub-ATMO indexes for the given day.

ATMO index classification :

![Grille-des-sous-indices](https://user-images.githubusercontent.com/108631539/204822631-d93a64e9-7ee2-496f-8e9a-623b6d60ef37.jpeg)

Source : Airparif
