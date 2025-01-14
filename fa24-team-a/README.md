University Accountability - Student Address Data (2016-2024)

## Project Overview
This project aims to enhance the transparency and accountability of off-campus student housing data reported by higher education institutions. By examining and standardizing data from the past decade, the project seeks to understand the impact on housing affordability and inform land use decisions. The initiative involves collaboration with the Inspectional Services Department to restore and clarify housing violation data, develop tools to identify problematic landlords, and integrate data across city departments. This ordinance will establish clear criteria for data collection and reporting, ultimately creating a publicly accessible database to ensure compliance and promote responsible property management.

### Projects early insights:
Using the data, we can answer the following types of questions:
- What is the trend of the number students in boston?
- Where do students generally live in and around boston?
- What are the trends regarding student housing across the city, by district, e.g. what % of the rental housing is taken up by students for each district and how has this changed over time?
    

This project focuses on processing and cleaning university accountability data for off-campus student addresses over the years 2016-2024. The dataset includes detailed records from multiple universities. Each record includes information about student addresses, degree level, full-time or part-time status, and whether students are at home or not-at-home. The cleaned datasets were combined into a final master file that consolidates the information for further analysis.

# Repository Structure

## Analysis
- **Path**: `fa24-team-a/Analysis`
- Contains scripts and outputs for various analyses:
  - **311 Service Requests**:
    - Scripts and visualizations analyzing 311 service request data.
    - Includes density heatmaps, trends in service requests, and most frequent service request analyses.
  - **Combining Student Addresses**:
    - Scripts and outputs for merging and cleaning student housing data across multiple years and universities.
    - Addresses the heterogeneity in formats and ensures consistency in the combined datasets.
  - **Combining StudentAddresses and SAM
    - Script to geolocate and combine both student addresses and SAM ID
  - **Neighborhoods**:
    - Analyses grouped by neighborhoods or zip codes.
    - Includes population trends and zip code-specific summaries.
  - **NoOfStudentsPerUnit**:
    - Script required to get data on no of students living per unit
  - **Violations**:
    - Scripts and datasets focusing on housing violations.
    - Outputs include trends in violations, identification of problematic landlords, and violation severities.

## Final Data
- **Path**: `fa24-team-a/FinalData`
- Consolidated and cleaned datasets ready for visualization and further analysis:
  - **Student Addresses Dataset**:
    - Cleaned and geocoded addresses for 2016–2024.
  - **District Aggregations**:
    - Aggregated datasets by district and zip code.
  - **Violations Data**:
    - Processed datasets highlighting housing violation trends.
  - **Link to 311 data**
  - **Link to final Dataset**

## Visualization
- **Path**: `fa24-team-a/Visualization`
- Finalized visualizations, charts, and maps


### Data Cleaning and Processing Steps

requirements:
you can run the command "pip install -r fa24-team-a\Code\Code for StudentAddresses\requirements.txt" to install all relevant packages to run the scripts.

Parsing and Splitting Addresses:

Data provided by the client after being parsed and joined can be found in fa24-team-a\FinalData. The raw data shared by the client can be found in fa24-team-a\RawData. 

The raw datasets contained addresses stored in single columns or incomplete address fields. A custom Python script was written to parse and split the addresses into individual components such as:
- 6a. Street #
- 6b. Street Name
- 6c. Street Suffix
- 6d. Unit #
- 6e. Zip

Address suffixes such as 'St', 'Ave', 'Blvd', etc., were accounted for in different cases (e.g., lowercase, uppercase).
Address Parsing for Different Universities:

Specific scripts were developed to process the addresses differently for universities like Northeastern, Boston College, Wentworth, and MCPHS. This involved parsing addresses in unique formats across datasets from different years.
Removing Duplicates and Filtering:

University-specific data, such as those for Northeastern and Boston College, were filtered and cleaned. Data for overlapping years were handled carefully, and duplicates were removed.
For example, Northeastern's 2017-2018 data were specifically filtered to account for unique address formats and column structures.

Combining Data:

The raw data was processed using the code found in fa24-team-a/Analysis/Combining_Student_Addresses for StudentAddresses. Separate scripts can be found for each 2 year interval (i.e 2016-2018, 2018-2020, 2020-2022, 2022-2024). Data was conactenated to each other vertically, year-by-year. Certain universities which had issues with the data (as described above) were worked on individually to debug them and ensure that an accurate version of the data is added to the dataset.

Additionally, the data shared by Northeastern was vastly different from the standard format, hence a separate script was written to ensure that data shared by them is processed correctly and fits the standard format followed for this project.

Finally, the process to combine the dataset was also partially done manually using excel, particularly for universities with issues in their data. Most of the manual work include changing columns positions, copying and pasting data from one file to another, etc. for data cleaning.

The cleaned datasets for different years were concatenated into a final combined dataset. Extra whitespaces, newline characters (\n), and capitalizations were handled to ensure uniformity.
Two additional columns, University and Year, were added to track the source of each record.

After combining StudentAddresses we answered Key question number 1 - What are the trends regarding student housing across the city, by district, e.g. what % of the rental housing is taken up by students for each district and how has this changed over time? to answer this we used the codes found in "fa24-team-a/Analysis/Neighborhoods". To run these codes we used boston neighborhood shapefiles which are also available in the folder.

After this we answered question 2a) What are the housing conditions for students living off-campus? how many students per unit? , for this analysis we used the code found in "fa24-team-a/Analysis/NoOfStudentsPerunit"

After this we could not answer any more key questions without SAM id values so we geolocated Student Addresses and SAM ID the code for which can be found in "fa24-team-a/Analysis/Combining StudentAddresses and SAM"
After getting the combined data for student addresses and sam id, we combined it with all the other datasets as well using the sam ID as primary key the code for which can be found here: "fa24-team-a/Analysis/Violations"

After getting the final combined data, we used this to answer question 2b, 3 and 4.
the codes for
- 2b:
- 3:
- 4:

Finally we solved our own question, question 5. What are the spatial and temporal trends of Boston's most frequent 311 service requests, and how do they correlate with neighborhood characteristics?
to solve this we first combined and cleaned 8 years of service request data and then processed the data and came up with visuals to answer our question the codes for which can be found at: "fa24-team-a/Analysis/311"

The final datasets we got throughout all the steps can be found at: "fa24-team-a/FinalData"
the final visuals we got thorughout all the steps can be found at: "fa24-team-a/Visualization"











