import re
import pandas as pd

def parse_address(address):
    # List of possible street suffixes
    street_suffixes = [
        "street", "st", "road", "rd", "avenue", "ave", "boulevard", "blvd",
        "lane", "ln", "drive", "dr", "court", "ct", "place", "pl", "terrace", "ter",
        "way", "wy", "highway", "hwy", "circle", "cir", "parkway", "pkwy",
        "square", "sq", "loop", "lp", "trail", "trl", "crescent", "cres",
        "park", "pke", "expressway", "expy", "mount", "mt", "point", "pt",
        "station", "sta", "view", "vw", "fort", "ft", "east", "west", "north", "south", "row"
    ]

    # List of possible unit prefixes (unit designators)
    unit_designators = [
        "apt", "apartment", "unit", "ste", "suite", "floor", "fl",
        "rm", "room", "#", "no", "number", "apt.", "ap", "appt"
    ]

    # Initialize components
    street_number = None
    street_name = None
    street_suffix = None
    unit_number = None

    # Remove every non-alphanumeric character, except for spaces
    address = re.sub(r'[^a-zA-Z0-9\s]', '', address)
    # Remove multiple spaces
    address = re.sub(r'\s+', ' ', address)
    # Remove leading and trailing spaces
    address = address.strip()
    # Lowercase the address
    address = address.lower()

    # Before anything, check if there is a zip code in the address
    zip_code = None
    zip_code_long = re.search(r'\b\d{5}-\d{4}\b', address)
    zip_code_short = re.search(r'\b\d{5}\b', address)
    
    if zip_code_long:
        zip_code = zip_code_long.group()
        address = address.replace(zip_code, '').strip()
    elif zip_code_short:
        zip_code = zip_code_short.group()
        address = address.replace(zip_code, '').strip()

    # Split the address into tokens
    tokens = address.split()

    # Pattern to match street numbers (digits followed by optional letters)
    street_number_pattern = re.compile(r'^\d+[a-zA-Z]?$')

    # Extract street number and remove it from tokens
    street_number = None
    for i, token in enumerate(tokens):
        if street_number_pattern.match(token):
            street_number = token
            tokens.pop(i)
            break  # Assuming street number is the first matching token

    # Extract unit number (from the end) and remove it from tokens
    # Adjusted pattern to match unit numbers that are single letters
    unit_number_pattern = re.compile(r'^\d+[a-zA-Z]*$|^[a-zA-Z]$')
    for i in range(len(tokens)-1, -1, -1):
        token = tokens[i]
        if unit_number_pattern.match(token):
            unit_number = token
            tokens.pop(i)
            break  # Assuming unit number is the last matching token

    # Extract unit designator and remove it from tokens
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
        break  # Assuming only one unit designator per address

    # Extract street suffix and remove it from tokens
    for i, token in enumerate(tokens):
        for suffix in street_suffixes:
            if token == suffix:
                street_suffix = suffix
                tokens.pop(i)
                break
        else:
            continue
        break  # Assuming only one street suffix per address

    # The remaining tokens form the street name
    street_name = ' '.join(tokens).strip() if tokens else None

    # Compile results
    result = {
        'street_number': street_number,
        'street_name': street_name if street_name else None,
        'street_suffix': street_suffix,
        'unit_number': unit_number
    }
    return pd.Series(result)
