# RLT_test_task
Telegram bot for test task of RLT company

## Overview

This is aiogram telegram bot for aggregate documents from MongoDB database.

## Features

The main functions of the Telegram bot application:

- **Data Input**: The bot accepts input parameters in JSON format, such as:
  ```json
  {
    "dt_from": "2022-09-01T00:00:00",
    "dt_upto": "2022-12-31T23:59:00",
    "group_type": "month"
  }
  ```
- **Data Aggregation**: Based on the provided parameters, the bot aggregates data from a MongoDB database. Supported group types include "hour", "day", "month", etc.
- **Data Output**: The bot returns aggregated data in the following JSON format:
  ```json
  {
    "dataset": [5906586, 5515874, 5889803, 6091874], 
    "labels": ["2022-09-01T00:00:00", "2022-10-01T00:00:00", 
                "2022-11-01T00:00:00", "2022-12-01T00:00:00"]
  }
  ```
## Tech Stack

- **Backend**: Python, Aiogram 3.7.x, MongoDB, asyncio

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/nsstnc/RLT_test_task.git
    cd RLT_test_task
    ```

2. Restore the MongoDB database. Before that, you need to install MongoDB and MongoDB tools from the official website.
    ```bash
    mongorestore dump_for_test_task\dump
    ```
3. Run the setup script to configure the virtual environment and start the project:

    ```bash
    sh setup.sh  # Use `setup.bat` on Windows
    ```
   
4. Enter the token of your bot that you received from Botfather into terminal window.

5. Start using your bot.

## File Structure
```
RLT_test_task/  
├── dump_for_test_task # Database's dumps directory  
├── bot.py # The main aiogram bot program
├── database.py # Database class for init DB and aggregating data
├── README.md # Project documentation  
├── requirements.txt # List of dependencies  
├── setup.bat # Script to set up the virtual environment and start the project for Windows systems  
├── setup.sh # Script to set up the virtual environment and start the project for UNIX systems  
```