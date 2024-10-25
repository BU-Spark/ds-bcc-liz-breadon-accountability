import os
import shutil
import pandas as pd
import numpy as np
import re


def fmt(files_moved):
    longest = max(len(x) for x in list(files_moved.keys()) + list(files_moved.values()))
    border = ('#' + '-' * (longest + 2) + '#') + '    ' + ('#' + '-' * (longest + 2) + '#')
    t = '| {:^' + str(longest) + '} |' + '    ' + '| {:^' + str(longest) + '} |'

    print(border)
    print(t.format('Moved From', 'Moved To'))
    print(border)

    for k, v in files_moved.items():
        print(t.format(k, v))

    print(border)

def move_files(university_name, move_to_folder):
    if not university_name:
        raise ValueError('University name cannot be empty')
    
    if not move_to_folder:
        raise ValueError('Move to folder cannot be empty')

    dirname = '../data/raw/'
    folders = os.listdir(dirname)
    folders = sorted(folders)

    files_moved = {}

    if os.path.exists(move_to_folder):
        shutil.rmtree(move_to_folder)
    os.makedirs(move_to_folder)

    for folder in folders:
        if folder == '.DS_Store':
            continue
        if 'School Year Reports' in folder:
            path_to_folder = os.path.join(dirname, folder)
            files = os.listdir(path_to_folder)
            for file in files:
                if university_name in file:
                    year = folder.split(' ')[0]
                    new_name = f"{year}.xlsx"
                    path_to_file = os.path.join(path_to_folder, file)
                    path_to_new_file = os.path.join(move_to_folder, new_name)

                    shutil.move(path_to_file, path_to_new_file)
                    files_moved[path_to_file] = path_to_new_file

    if files_moved:
        fmt(files_moved)
    else:
        print(f"No files found with the name '{university_name}'")



def print_columns(dfs):
    for key in dfs.keys():
        print(key)
        print(list(dfs[key].columns))


def fix_missing_columns(df, columns):
    '''
        Adds columns to each dataframe in dfs if the column is not already present.
    '''
    for column in columns:
        if column not in list(df.columns):
            df[column] = np.nan
    return df


def reorder_columns(dfs, columns):
    '''
        Reorder columns so they match the order in the columns list
    '''
    for key in dfs:
        for column in columns:
            if column in list(dfs[key].columns):
                col = dfs[key][column]
                dfs[key].drop(columns=[column], inplace=True)
                dfs[key][column] = col
    return dfs


def prepare_dataframes(dirname):
    dirname = f'../data/sorted/universities/{dirname}/raw/'

    files = os.listdir(dirname)

    dataframes = {}

    for file in files:
        if file == '.DS_Store':
            continue
        path_to_file = dirname + file
        
        dataframe = None

        try:
            dataframe = pd.read_excel(path_to_file, sheet_name='Student Addresses')
        except Exception as e:
            print('Could not read file: ' + path_to_file)
            print(e)

        dataframes[file] = dataframe

    return dataframes

def find_common_column_groups(dataframes):
    groups = {}

    for university in dataframes:
        for year in dataframes[university]:
            df = dataframes[university][year]
            
            if df is None:
                continue

            as_key = str(list(df.columns))

            if as_key not in groups:
                groups[as_key] = []

            groups[as_key].append((university, year))

    return groups




def seperate_address(address):
    street_suffixes = [
        "street", "st", "road", "rd", "avenue", "ave", "boulevard", "blvd",
        "lane", "ln", "drive", "dr", "court", "ct", "place", "pl", "terrace", "ter",
        "way", "wy", "highway", "hwy", "circle", "cir", "parkway", "pkwy",
        "square", "sq", "loop", "lp", "trail", "trl", "crescent", "cres",
        "park", "pke", "expressway", "expy", "mount", "mt", "point", "pt",
        "station", "sta", "view", "vw", "fort", "ft", "east", "west", "north", "south", "row"
    ]

    unit_designators = [
        "apt", "apartment", "unit", "ste", "suite", "floor", "fl",
        "rm", "room", "#", "no", "number", "apt.", "ap", "appt"
    ]

    # Initialize components
    street_number = None
    street_name = None
    street_suffix = None
    unit_number = None

    address = re.sub(r'[^a-zA-Z0-9\s]', '', address)
    address = re.sub(r'\s+', ' ', address)
    address = address.strip()
    address = address.lower()

    zip_code = None
    zip_code_long = re.search(r'\b\d{5}-\d{4}\b', address)
    zip_code_short = re.search(r'\b\d{5}\b', address)
    
    if zip_code_long:
        zip_code = zip_code_long.group()
        address = address.replace(zip_code, '').strip()
    elif zip_code_short:
        zip_code = zip_code_short.group()
        address = address.replace(zip_code, '').strip()

    tokens = address.split()

    street_number_pattern = re.compile(r'^\d+[a-zA-Z]?$')

    street_number = None
    for i, token in enumerate(tokens):
        if street_number_pattern.match(token):
            street_number = token
            tokens.pop(i)
            break

    unit_number_pattern = re.compile(r'^\d+[a-zA-Z]*$|^[a-zA-Z]$')
    for i in range(len(tokens)-1, -1, -1):
        token = tokens[i]
        if unit_number_pattern.match(token):
            unit_number = token
            tokens.pop(i)
            break

    for i, token in enumerate(tokens):
        for unit_designator in unit_designators:
            if token == unit_designator:
                if unit_number:
                    unit_number = f'{unit_designator} {unit_number}'
                else:
                    unit_number = unit_designator
                tokens.pop(i)
                break
        else:
            continue
        break

    for i, token in enumerate(tokens):
        for suffix in street_suffixes:
            if token == suffix:
                street_suffix = suffix
                tokens.pop(i)
                break
        else:
            continue
        break

    street_name = ' '.join(tokens).strip() if tokens else None

    result = {
        'street_number': street_number,
        'street_name': street_name if street_name else None,
        'street_suffix': street_suffix,
        'unit_number': unit_number
    }
    return pd.Series(result)

def fix_zip_code(zip_code):
    f1 = re.compile(r'^0\d{4}$')
    f2 = re.compile(r'^0\d{4}-\d{4}$')
    f3 = re.compile(r'^\d{4}\.0$')

    zip_code_str = str(zip_code).strip()
    zip_code_str = zip_code_str.replace(' ', '')
    
    if pd.isnull(zip_code_str):
        return '00000'

    if f1.fullmatch(zip_code_str):
        return zip_code_str
    
    if f2.fullmatch(zip_code_str):
        return zip_code_str
    
    if f3.fullmatch(zip_code_str):
        digits = zip_code_str[:4]
        fixed_zip = '0' + digits
        return fixed_zip
    
    if len(zip_code_str) <= 4 and zip_code_str.isdigit():
        fixed_zip = '0' + zip_code_str.zfill(4)

        if f1.fullmatch(fixed_zip):
            return fixed_zip
        else:
            return '00000'
        
    elif 6 <= len(zip_code_str) <= 9:
        fixed_zip = zip_code_str[:5]
        if f1.fullmatch(fixed_zip):
            return fixed_zip
        else:
            return '00000'
        
    elif len(zip_code_str) >= 11:
        fixed_zip = zip_code_str[:5] + '-' + zip_code_str[6:]
        if f2.fullmatch(fixed_zip):
            return fixed_zip
        else:
            return '00000'
        
    else:
        return '00000'

def is_in_massachusetts(zip_code):
    try:
        zip_code = int(zip_code)
    except:
        zip = zip_code.split('-')[0]

        try:
            zip = int(zip)
        except:
            return False
        
        if zip >= 1001 and zip <= 2791:
            return True
        
        return False
    
    if zip_code >= 1001 and zip_code <= 2791:
        return True
    
    return False
