# Paris DeepAir Project

Le Wagon - Bootcamp Data Science - Full time
Batch #1002 - 03/10-09/12/2022

Projet de fin d'études présenté en groupe (4 personnes)

------------------------------------------------

## Preliminary steps to carry-out

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
- **data** : all data used for this project
- **notebooks** : individual notebooks for this project
- **workflow**: all the workflow for our model, divided in .py files

------------------------------------------------

## Dataset description

**Pollutants (French / English) in the ATMO  index:**
- **PM 2,5**: particules fines / fine particles
- **PM 10**: particules / particles
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

------------------------------------------------

## ATMO Index

The ATMO index is a daily indicator of air quality, calculated from concentration into the air of regulated pollutant. This index classifies air quality into 6 classes (from good to extremely bad).

First, a sub-ATMO index is calculated for each regulated air pollutant, then a global ATMO index is calulated from these sub-ATMO indexes. The global ATMO index is equal to the worst classification of sub-ATMO indexes for the given day.

ATMO index classification :

![Grille-des-sous-indices](https://user-images.githubusercontent.com/108631539/204822631-d93a64e9-7ee2-496f-8e9a-623b6d60ef37.jpeg)

Source : Airparif
