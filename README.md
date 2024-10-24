# Airline Customer Data Analysis

This project analyzes customer data from an airline company using Python and various data analysis libraries and is a part of the Data Engineering Bootcamp assignment at Dibimbing Batch 7.

## Description

This script performs an analysis on three datasets:

1. Customer loyalty history
2. Customer flight activity
3. Calendar data

The analysis includes visualizations of:

1. Total flights per month in 2018
2. Distribution of loyalty cards
3. Average salary by education level
4. Relationship between points accumulated and distance traveled

## Requirements

- Python 3.7+
- Jupyter Notebook
- pandas
- matplotlib
- PySpark

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`
4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Ensure your virtual environment is activated
2. Launch Jupyter Notebook:
   ```
   jupyter notebook
   ```
3. Open the `main.ipynb` file
4. Run the cells in order

## Dataset Analysis

1. Total Flights per Month (2018):

   - Shows the distribution of flights throughout the year 2018
   - Helps identify peak travel seasons and low periods

2. Distribution of Loyalty Cards:

   - Visualizes the proportion of different loyalty card types among customers
   - Useful for understanding customer segmentation and loyalty program effectiveness

3. Average Salary by Education Level:

   - Compares average salaries across different education levels
   - Provides insights into the relationship between education and income among customers

4. Points Accumulated vs Distance Traveled:
   - Scatter plot showing the relationship between distance traveled and points earned
   - Helps understand the correlation between customer travel distance and loyalty points accumulation

## Notes

- Ensure that the CSV files (customer_loyalty_history.csv, customer_flight_activity.csv, and calendar.csv) are in the `data` directory.
- The analysis uses PySpark for data processing, which may require additional setup depending on your system.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
