University Accountability - Student Address Data (2016-2024)
#### Project Overview
This project aims to enhance the transparency and accountability of off-campus student housing data reported by higher education institutions. By examining and standardizing data from the past decade, the project seeks to understand the impact on housing affordability and inform land use decisions. The initiative involves collaboration with the Inspectional Services Department to restore and clarify housing violation data, develop tools to identify problematic landlords, and integrate data across city departments. This ordinance will establish clear criteria for data collection and reporting, ultimately creating a publicly accessible database to ensure compliance and promote responsible property management.

#### Projects early insights:
Using the data, we can answer the following types of questions:
    > What is the trend of the number students in boston?
    > Where do students generally live in and around boston?
    > What are the trends regarding student housing across the city, by district, e.g. what % of the rental housing is taken up by students for each district and how has this changed over time?
    

This project focuses on processing and cleaning university accountability data for off-campus student addresses over the years 2016-2024. The dataset includes detailed records from multiple universities. Each record includes information about student addresses, degree level, full-time or part-time status, and whether students are at home or not-at-home. The cleaned datasets were combined into a final master file that consolidates the information for further analysis.

#### Repository Structure
Code: fa24-team-a\Code
    > Code used to pre-process the student addresses : fa24-team-a\Code\Code for StudentAddresses
    > Code used to analyze the student data by district :  fa24-team-a\Code\Districts code
Processed datasets: fa24-team-a\FinalData
    > The final combined dataset for student Addresses : fa24-team-a\FinalData\StudentAddresses-2016-2024.xlsx
    > Student addresses with geographical information : fa24-team-a\FinalData\geocoded_student_addresses.xlsx
    > Student addresses aggregation by districts : fa24-team-a\FinalData\student_housing_percentage_by_district.xlsx
    > Student addresses with their corresponding district information: fa24-team-a\FinalData\students_with_districts.xlsx
The raw datasets shared by the client : fa24-team-a\RawData
    > District information and shape files: fa24-team-a\RawData\Districts
    > Excel files of student addresses from 2016-2024: fa24-team-a\RawData\Student Addresses
Visualizations created for analysis : fa24-team-a\Visualization


#### Data Cleaning and Processing Steps

requirements:
you can run the command "pip install -r fa24-team-a\Code\Code for StudentAddresses\requirements.txt" to install all relevant packages to run the scripts.

Parsing and Splitting Addresses:

Data provided by the client after being parsed and joined can be found in fa24-team-a\FinalData. The raw data shared by the client can be found in fa24-team-a\RawData. 

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

The raw data was processed using the code found in fa24-team-a\Code\Code for StudentAddresses. Separate scripts can be found for each 2 year interval (i.e 2016-2018, 2018-2020, 2020-2022, 2022-2024). Data was conactenated to each other vertically, year-by-year. Certain universities which had issues with the data (as described above) were worked on individually to debug them and ensure that an accurate version of the data is added to the dataset.

Additionally, the data shared by Northeastern was vastly different from the standard format, hence a separate script was written to ensure that data shared by them is processed correctly and fits the standard format followed for this project.

Finally, the process to combine the dataset was also partially done manually using excel, particularly for universities with issues in their data. Most of the manual work include changing columns positions, copying and pasting data from one file to another, etc. for data cleaning.

The cleaned datasets for different years were concatenated into a final combined dataset. Extra whitespaces, newline characters (\n), and capitalizations were handled to ensure uniformity.
Two additional columns, University and Year, were added to track the source of each record.










