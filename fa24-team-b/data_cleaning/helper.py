import os
import shutil
import pandas as pd
import numpy as np
import re

def fmt(files_moved):
    """
    Formats and prints a table showing files moved from their original locations to new destinations.

    Parameters:
    files_moved (dict): A dictionary where keys are original file paths and values are new file paths.
    """
    # Determine the length of the longest file path for formatting purposes
    longest = max(len(x) for x in list(files_moved.keys()) + list(files_moved.values()))
    # Create the table border based on the longest file path
    border = ('#' + '-' * (longest + 2) + '#') + '    ' + ('#' + '-' * (longest + 2) + '#')
    # Define the format string for table rows, centering the text within each column
    t = '| {:^' + str(longest) + '} |' + '    ' + '| {:^' + str(longest) + '} |'

    # Print the table header
    print(border)
    print(t.format('Moved From', 'Moved To'))
    print(border)

    # Iterate over the moved files and print each one in the table
    for k, v in files_moved.items():
        print(t.format(k, v))

    # Print the table footer
    print(border)

def move_files(university_name, move_to_folder):
    """
    Moves files containing a specific university name from multiple folders to a designated folder.

    Parameters:
    university_name (str): The name of the university to search for in file names.
    move_to_folder (str): The destination folder where the files will be moved.
    """
    # Validate input parameters
    if not university_name:
        raise ValueError('University name cannot be empty')
    if not move_to_folder:
        raise ValueError('Move to folder cannot be empty')

    # Define the directory containing the raw data
    dirname = '../data/raw/'
    # Get a sorted list of all folders in the directory
    folders = os.listdir(dirname)
    folders = sorted(folders)

    # Dictionary to keep track of moved files
    files_moved = {}

    # Remove the destination folder if it exists and recreate it
    if os.path.exists(move_to_folder):
        shutil.rmtree(move_to_folder)
    os.makedirs(move_to_folder)

    # Iterate through each folder in the raw data directory
    for folder in folders:
        if folder == '.DS_Store':
            continue  # Skip system files
        if 'School Year Reports' in folder:
            # Construct the path to the folder
            path_to_folder = os.path.join(dirname, folder)
            # List all files in the folder
            files = os.listdir(path_to_folder)
            # Iterate through each file in the folder
            for file in files:
                # Check if the file name contains the university name
                if university_name in file:
                    # Extract the year from the folder name
                    year = folder.split(' ')[0]
                    # Create a new file name using the year
                    new_name = f"{year}.xlsx"
                    # Construct full paths for the source and destination files
                    path_to_file = os.path.join(path_to_folder, file)
                    path_to_new_file = os.path.join(move_to_folder, new_name)

                    # Move the file to the new location
                    shutil.move(path_to_file, path_to_new_file)
                    # Record the moved file paths
                    files_moved[path_to_file] = path_to_new_file

    # Print the result if any files were moved
    if files_moved:
        fmt(files_moved)
    else:
        print(f"No files found with the name '{university_name}'")

def print_columns(dfs):
    """
    Prints the column names of each DataFrame in a dictionary.

    Parameters:
    dfs (dict): A dictionary where keys are identifiers and values are pandas DataFrames.
    """
    # Iterate over each DataFrame in the dictionary
    for key in dfs.keys():
        print(key)
        # Print the list of column names for the current DataFrame
        print(list(dfs[key].columns))

def fix_missing_columns(df, columns):
    '''
    Adds columns to the DataFrame if they are not already present.

    Parameters:
    df (pd.DataFrame): The DataFrame to be modified.
    columns (list): A list of column names that should be present in the DataFrame.

    Returns:
    pd.DataFrame: The modified DataFrame with all specified columns present.
    '''
    # Iterate over each required column
    for column in columns:
        # If the column is missing, add it with NaN values
        if column not in list(df.columns):
            df[column] = np.nan
    return df

def reorder_columns(dfs, columns):
    '''
    Reorders columns in each DataFrame to match the order in the columns list.

    Parameters:
    dfs (dict): A dictionary of DataFrames to be reordered.
    columns (list): The desired order of columns.

    Returns:
    dict: The dictionary of DataFrames with columns reordered.
    '''
    # Iterate over each DataFrame in the dictionary
    for key in dfs:
        # Iterate over each column in the desired order
        for column in columns:
            if column in list(dfs[key].columns):
                # Extract the column data
                col = dfs[key][column]
                # Drop the column from its current position
                dfs[key].drop(columns=[column], inplace=True)
                # Re-add the column to place it at the end
                dfs[key][column] = col
    return dfs

def prepare_dataframes(dirname):
    """
    Reads Excel files from a specified directory and returns a dictionary of DataFrames.

    Parameters:
    dirname (str): The name of the directory containing the Excel files.

    Returns:
    dict: A dictionary where keys are file names and values are DataFrames.
    """
    # Construct the full path to the directory
    dirname = f'../data/sorted/universities/{dirname}/raw/'

    # List all files in the directory
    files = os.listdir(dirname)

    # Dictionary to store the DataFrames
    dataframes = {}

    # Iterate over each file in the directory
    for file in files:
        if file == '.DS_Store':
            continue  # Skip system files
        # Construct the full file path
        path_to_file = dirname + file
        
        dataframe = None

        try:
            # Read the 'Student Addresses' sheet from the Excel file
            dataframe = pd.read_excel(path_to_file, sheet_name='Student Addresses')
        except Exception as e:
            # Print an error message if reading fails
            print('Could not read file: ' + path_to_file)
            print(e)

        # Add the DataFrame to the dictionary
        dataframes[file] = dataframe

    return dataframes

def find_common_column_groups(dataframes):
    """
    Identifies groups of DataFrames that share the same column structure.

    Parameters:
    dataframes (dict): A nested dictionary of DataFrames, organized by university and year.

    Returns:
    dict: A dictionary where keys are string representations of column lists and values are lists of (university, year) tuples.
    """
    # Dictionary to store groups of DataFrames with common columns
    groups = {}

    # Iterate over each university in the dataframes
    for university in dataframes:
        # Iterate over each year for the current university
        for year in dataframes[university]:
            df = dataframes[university][year]
                
            if df is None:
                continue  # Skip if DataFrame is None

            # Convert the list of columns to a string to use as a dictionary key
            as_key = str(list(df.columns))

            # Add the university and year to the corresponding group
            if as_key not in groups:
                groups[as_key] = []

            groups[as_key].append((university, year))

    return groups

def seperate_address(address):
    """
    Separates a full address string into its components: street number, street name, street suffix, and unit number.

    Parameters:
    address (str): The full address string.

    Returns:
    pd.Series: A Series containing the separated address components.
    """
    # List of common street suffixes
    street_suffixes = [
        "street", "st", "road", "rd", "avenue", "ave", "boulevard", "blvd",
        "lane", "ln", "drive", "dr", "court", "ct", "place", "pl", "terrace", "ter",
        "way", "wy", "highway", "hwy", "circle", "cir", "parkway", "pkwy",
        "square", "sq", "loop", "lp", "trail", "trl", "crescent", "cres",
        "park", "pke", "expressway", "expy", "mount", "mt", "point", "pt",
        "station", "sta", "view", "vw", "fort", "ft", "east", "west", "north", "south", "row"
    ]

    # List of common unit designators
    unit_designators = [
        "apt", "apartment", "unit", "ste", "suite", "floor", "fl",
        "rm", "room", "#", "no", "number", "apt.", "ap", "appt"
    ]

    # Initialize components
    street_number = None
    street_name = None
    street_suffix = None
    unit_number = None

    # Clean the address string
    address = re.sub(r'[^a-zA-Z0-9\s]', '', address)  # Remove non-alphanumeric characters
    address = re.sub(r'\s+', ' ', address)             # Replace multiple spaces with a single space
    address = address.strip()                          # Remove leading and trailing spaces
    address = address.lower()                          # Convert to lowercase

    # Initialize zip code variables
    zip_code = None
    # Search for long and short zip codes in the address
    zip_code_long = re.search(r'\b\d{5}-\d{4}\b', address)
    zip_code_short = re.search(r'\b\d{5}\b', address)
    
    # Extract and remove the zip code from the address
    if zip_code_long:
        zip_code = zip_code_long.group()
        address = address.replace(zip_code, '').strip()
    elif zip_code_short:
        zip_code = zip_code_short.group()
        address = address.replace(zip_code, '').strip()

    # Split the address into tokens
    tokens = address.split()

    # Patterns to identify street numbers and unit numbers
    street_number_pattern = re.compile(r'^\d+[a-zA-Z]?$')
    unit_number_pattern = re.compile(r'^\d+[a-zA-Z]*$|^[a-zA-Z]$')

    # Extract street number
    for i, token in enumerate(tokens):
        if street_number_pattern.match(token):
            street_number = token
            tokens.pop(i)
            break  # Found the street number, exit the loop

    # Extract unit number
    for i in range(len(tokens)-1, -1, -1):
        token = tokens[i]
        if unit_number_pattern.match(token):
            unit_number = token
            tokens.pop(i)
            break  # Found the unit number, exit the loop

    # Check for unit designators
    for i, token in enumerate(tokens):
        for unit_designator in unit_designators:
            if token == unit_designator:
                if unit_number:
                    unit_number = f'{unit_designator} {unit_number}'
                else:
                    unit_number = unit_designator
                tokens.pop(i)
                break  # Found the unit designator, exit the inner loop
        else:
            continue
        break  # Exit the outer loop if unit designator is found

    # Extract street suffix
    for i, token in enumerate(tokens):
        for suffix in street_suffixes:
            if token == suffix:
                street_suffix = suffix
                tokens.pop(i)
                break  # Found the street suffix, exit the inner loop
        else:
            continue
        break  # Exit the outer loop if street suffix is found

    # The remaining tokens form the street name
    street_name = ' '.join(tokens).strip() if tokens else None

    # Create a result dictionary
    result = {
        'street_number': street_number,
        'street_name': street_name if street_name else None,
        'street_suffix': street_suffix,
        'unit_number': unit_number
    }
    # Return the result as a pandas Series
    return pd.Series(result)

def fix_zip_code(zip_code):
    """
    Corrects and standardizes zip code formats.

    Parameters:
    zip_code (str): The zip code to be corrected.

    Returns:
    str: The corrected zip code in standard format.
    """
    # Compile regular expressions for different zip code formats
    f1 = re.compile(r'^0\d{4}$')           # Format: 0XXXX
    f2 = re.compile(r'^0\d{4}-\d{4}$')     # Format: 0XXXX-XXXX
    f3 = re.compile(r'^\d{4}\.0$')         # Format: XXXX.0

    # Convert the zip code to a string and remove spaces
    zip_code_str = str(zip_code).strip()
    zip_code_str = zip_code_str.replace(' ', '')
    
    # Return '00000' if the zip code is null
    if pd.isnull(zip_code_str):
        return '00000'

    # Check if the zip code matches the expected formats
    if f1.fullmatch(zip_code_str):
        return zip_code_str
    
    if f2.fullmatch(zip_code_str):
        return zip_code_str
    
    if f3.fullmatch(zip_code_str):
        digits = zip_code_str[:4]
        fixed_zip = '0' + digits
        return fixed_zip
    
    # Handle zip codes with 4 or fewer digits
    if len(zip_code_str) <= 4 and zip_code_str.isdigit():
        fixed_zip = '0' + zip_code_str.zfill(4)
        if f1.fullmatch(fixed_zip):
            return fixed_zip
        else:
            return '00000'
        
    # Handle zip codes with length between 6 and 9 characters
    elif 6 <= len(zip_code_str) <= 9:
        fixed_zip = zip_code_str[:5]
        if f1.fullmatch(fixed_zip):
            return fixed_zip
        else:
            return '00000'
        
    # Handle zip codes with length greater than or equal to 11 characters
    elif len(zip_code_str) >= 11:
        fixed_zip = zip_code_str[:5] + '-' + zip_code_str[6:]
        if f2.fullmatch(fixed_zip):
            return fixed_zip
        else:
            return '00000'
        
    else:
        return '00000'

def is_in_massachusetts(zip_code):
    """
    Checks whether a zip code is within the state of Massachusetts.

    Parameters:
    zip_code (str): The zip code to check.

    Returns:
    bool: True if the zip code is in Massachusetts, False otherwise.
    """
    try:
        # Attempt to convert the zip code to an integer
        zip_code = int(zip_code)
    except:
        # If conversion fails, extract the first part of the zip code
        zip_part = zip_code.split('-')[0]

        try:
            zip_part = int(zip_part)
        except:
            return False  # Not a valid zip code
            
        # Check if the zip code falls within the Massachusetts range
        if zip_part >= 1001 and zip_part <= 2791:
            return True
            
        return False
    
    # Check if the zip code falls within the Massachusetts range
    if zip_code >= 1001 and zip_code <= 2791:
        return True
    
    return False
