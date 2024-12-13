# University Accountability Ordinance - Team B  
## Project Structure  

### Project Overview  
This project examines the influence of off-campus student housing on Boston’s housing market. The initiative, supported by Boston City Councilor Liz Breadon’s Office (District 9), aims to improve transparency and accountability in housing data reporting. By analyzing and standardizing a decade’s worth of data, the project provides insights into housing affordability, landlord accountability, and urban development.  

The primary goals of this project are to address the following questions:  
1. **Housing Trends**: What percentage of rental housing is occupied by students in each district, and how has this changed over time?  
2. **Housing Conditions**: What are the living conditions of students residing in off-campus housing?  
3. **Landlord Compliance**: What is the spectrum and severity of violations committed by landlords, and who are the most non-compliant landlords?  

---

### Team Contributions  

#### **Raul: Data Cleaning, Automation, and Notebook Polishing**  
- Created a pipeline for automatically reading the data, fixing and bringing it to a universal format, and merging it into a single file.  
- Created another pipeline for partially automated data cleaning.  
- Retrained a model for address parsing (splitting the address into sections such as `StreetName`, `StreetNumber`, `Unit`).  
- Manually cleaned the dataset by mapping unstandardized or inconsistent values.  
- Formatted notebooks for improved readability and organized the team GitHub repository.  

#### **Raul & Gabby: Exploratory Data Analysis and Visualization**  
- Conducted detailed exploratory data analysis (EDA) of the student housing dataset to understand trends in off-campus housing occupancy.  
- Analyzed data for Boston neighborhoods and institutions, visualizing where students live off-campus.  
- Created a line graph depicting trends in undergraduate and graduate students living off-campus from 2016 to 2024, emphasizing changes during the COVID-19 pandemic.  
- Developed an exploratory dashboard and bubble map to highlight high-density student housing areas, such as Allston, Fenway-Kenmore, and Back Bay.  
- Conducted school-specific analyses, creating area charts, bar charts, and tables for various Boston institutions to demonstrate the proportion of students living off-campus and total enrollment over time.  
- Summarized findings by identifying common relationships between enrollment and off-campus housing trends and distinctions between undergraduate and graduate student housing patterns.  

#### **Zainab: Property Assessment Analysis (Key Question 2)**  
- Processed and standardized property assessment data for the years 2016–2024 to ensure consistency across datasets.  
- Analyzed annual distributions of property conditions across ZIP codes, creating heatmaps to visualize geographic trends.  
- Identified areas with persistent challenges (e.g., consistently "Unsound" conditions in ZIP codes like 02108) and areas with notable improvements (e.g., transitioning to "Good" or "Very Good" conditions in ZIP codes like 02124).  
- Examined building classifications through heatmaps to track redevelopment patterns, highlighting ZIP codes transitioning from "Old" to "New" classifications and those experiencing redevelopment stagnation.  
- Investigated owner-occupancy trends, analyzing the proportion of owner-occupied versus rental properties annually and identifying transitions between owner-heavy and rental-heavy markets.  
- Created pie charts to analyze annual distributions of heating system types, emphasizing the dominance of individual-controlled systems (~61%) and the minimal presence of properties lacking heating systems (~1%).  
- Calculated average bedroom counts by ZIP code to assess housing configurations, identifying neighborhoods with larger units suitable for shared student rentals and smaller units catering to individuals.  
- Conducted comprehensive data cleaning and standardization to address inconsistencies in property attributes, ensuring datasets were consistent and reliable across all years.  
- Synthesized findings into actionable insights, providing detailed analyses of housing conditions to inform targeted interventions and policy recommendations for improving off-campus student housing.  

#### **Christine: Building Violations Analysis (Key Question 3)**  
- Analyzed building and property violations data from 2016 to 2024 to evaluate patterns in landlord non-compliance.  
- Examined violation frequency and severity across neighborhoods, identifying Dorchester as the area with the highest violations annually and Mission Hill as consistently low.  
- Created a bubble map linked to a Looker Studio dashboard to visualize violations geographically, with filters for years and violation types.  
- Highlighted addresses with the highest violation counts and their corresponding neighborhoods, such as 13 Hendry St (Dorchester) and 1127-1131 Harrison Ave (Roxbury).  
- Categorized violations into recurring types, such as "Failure to Obtain Permit" and "Unsafe and Dangerous Conditions," consistently ranking as the top violations from 2016–2024.  
- Identified the most non-compliant landlords based on SAM IDs and analyzed violations by frequency and severity.  
- Developed an interactive dashboard in Looker Studio to allow stakeholders to filter violations by landlord and type for actionable insights.  

---

### Repository Structure  
To be completed.  

---

### Datasets Used  

#### **Student Housing Data**  
- **Source**: University Accountability Report for Student Housing.  
- **Details**: Includes data on housing types, addresses, occupancy status, and student demographics.  
- **Coverage**: Undergraduate and graduate students living on-campus and off-campus.  

#### **Property Assessment Data**  
- **Source**: Boston’s Open Data Portal.  
- **Details**: Annual datasets (2016–2024) detailing property conditions, classifications, owner details, and physical attributes.  
- **Key Attributes**:  
  - **Property Condition**: Rated from "Unsound" to "Very Good".  
  - **Building Classification**: Categorized as "Old," "Average," or "New".  
  - **Owner-Occupancy**: Differentiates between rental and owner-occupied properties.  
  - **Heating Systems**: Details on system types, including individual, self-contained, or shared systems.  
  - **Average Bedroom Count**: Reflects housing size and suitability.  

#### **Building and Property Violations Data**  
- **Source**: Boston’s Open Data Portal.  
- **Details**: Records of property violations by landlords, detailing violation types, severity, and addresses.  
- **Coverage**: Data spans from 2016 to 2024, highlighting non-compliance issues among landlords.  

---

### Reproducibility Guidelines  
To be completed.  
