## DataAnalysisonCSV

## Overview
This project is to parse the csv file, calculate the necessary information and export the result with a json format.
The pandas framework is used for this project.

## Structure

- src

    The main source code for parsing an excel file, calculating and creating json file.

- utils

    The tools for management of folders and files of this project.

- app

    The main execution file
    
- requirements

    All the dependencies for this project
    
- settings

    Several settings including the excel file path as an input

## Installation

- Environment

    Ubuntu 18.04, Windows 10, Python 3.6+
    
- Dependency Installation

    Please go ahead to this project directory and run the following command in the terminal.
    ```
        pip3 install -r requirements.txt
    ```

## Execution

- Please set the EXCEL_PATH variable in settings file with the absolute path of an excel file to process.

- Please navigate the directory of this project and run the following command.

    ```
        python3 app.py
    ```
  
- The processing result will be in output directory.
