University Accountability - Student Address Data (2016-2024)

Project Overview
This project focuses on processing and cleaning university accountability data for off-campus student addresses over the years 2016-2024. The dataset includes detailed records from multiple universities. Each record includes information about student addresses, degree level, full-time or part-time status, and whether students are at home or not-at-home. The cleaned datasets were combined into a final master file that consolidates the information for further analysis.

Repository Structure
Code: Contains the code files and scripts used to process and clean the datasets.
FinalData: Contains the final combined dataset, StudentAddresses-2016-2024.xlsx, which includes the cleaned data for all years.
RawData: Contains the raw datasets from the respective years:
StudentAddresses-2016-2018
StudentAddresses-2018-2020
StudentAddresses-2020-2022
StudentAddresses-2022-2024
Data Cleaning and Processing Steps
Parsing and Splitting Addresses:

The raw datasets contained addresses stored in single columns or incomplete address fields. A custom Python script was written to parse and split the addresses into individual components such as:
6a. Street #
6b. Street Name
6c. Street Suffix
6d. Unit #
6e. Zip
Address suffixes such as 'St', 'Ave', 'Blvd', etc., were accounted for in different cases (e.g., lowercase, uppercase).
Address Parsing for Different Universities:

Specific scripts were developed to process the addresses differently for universities like Northeastern, Boston College, Wentworth, and MCPHS. This involved parsing addresses in unique formats across datasets from different years.
Removing Duplicates and Filtering:

University-specific data, such as those for Northeastern and Boston College, were filtered and cleaned. Data for overlapping years were handled carefully, and duplicates were removed.
For example, Northeastern's 2017-2018 data were specifically filtered to account for unique address formats and column structures.
Combining Data:

The cleaned datasets for different years were concatenated into a final combined dataset. Extra whitespaces, newline characters (\n), and capitalizations were handled to ensure uniformity.
Two additional columns, University and Year, were added to track the source of each record.
Visualizations:


StudentAddresses-2016-2024.xlsx: The final cleaned and combined dataset containing all student addresses from the years 2016 to 2024.

Instructions for Use

