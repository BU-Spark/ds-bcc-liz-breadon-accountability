import pandas as pd
import os
from rich.progress import Progress
from rich.progress import BarColumn
from rich.console import Console
from rich.progress import TextColumn

class DataFile:
    """
    Represents a single Excel file with student addresses. Handles reading the file,
    applying metadata (e.g., year range, university), and mapping columns to a standard format.
    """
    def __init__(self, path, year_range, university):
        assert os.path.exists(path), 'File does not exist.'
        
        self.path = path
        self.year_range = year_range
        self.university = university
        self.dataframe = None

        # Attempt to read the Excel file
        try: 
            self.dataframe = pd.read_excel(self.path, sheet_name='Student Addresses')
        except:
            print(f'Error reading {self.path}')

        # Add metadata columns if the file was read successfully
        if self.dataframe is not None:
            self.dataframe['year_start'] = self.year_range[0]
            self.dataframe['year_end'] = self.year_range[1]
            self.dataframe['university'] = self.university

    def map(self, mapping):
        """
        Maps the file's columns to a standardized format using the provided mapping.
        Adds missing columns as empty if they are not present in the original data.
        """
        if self.dataframe is None:
            return

        # Ensure all required columns exist, even if empty
        for column in mapping:
            if column not in self.dataframe.columns:
                self.dataframe[column] = pd.NA

        # Rename columns based on the mapping
        self.dataframe = self.dataframe.rename(columns=mapping)

        # Keep only the mapped columns in the final dataframe
        self.dataframe = self.dataframe[mapping.values()]

class DataPreparation:
    """
    Processes a directory of Excel files, extracts and standardizes student address data,
    and merges it into a single consolidated dataset.
    """
    def __init__(self, directory):
        self.directory = directory
        self.files = []  # List to store DataFile objects
        self.data = None  # Final merged dataset

    def load(self):
        """
        Reads all Excel files in the specified directory structure, extracting metadata from directories
        and filenames. Displays progress using Rich's progress bars.
        """
        console = Console()

        # Gather directories and files
        dir_list = []
        for root, dirs, files in os.walk(self.directory):
            if len(files) > 0:
                dir_list.append((root, files))

        # Sort directories alphabetically by name
        dir_list = sorted(dir_list, key=lambda x: x[0])

        # Set up progress bar for reading directories and files
        progress = Progress(
            TextColumn("{task.description}", justify="left"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}", justify="right"),
            console=console,
        )

        with progress:
            # Main task for tracking overall directory progress
            dir_task = progress.add_task("Reading directories", total=len(dir_list))

            for root, files in dir_list:
                # Sub-task for tracking progress within the current directory
                current_dir = root.split('/')[-1]
                file_task = progress.add_task(f"Processing files in {current_dir}", total=len(files))

                for file in files:
                    if file.endswith('.xlsx'):
                        # Construct file metadata from directory and filename
                        path = os.path.join(root, file)
                        year_range = tuple(current_dir.split('-'))
                        university = file.split('.')[0]
                        self.files.append(DataFile(path, year_range, university))

                    # Update progress for the current file
                    progress.update(file_task, advance=1)

                # Mark the directory as completed
                progress.remove_task(file_task)
                progress.update(dir_task, advance=1)

            progress.refresh()

    def merge(self):
        """
        Maps all files' columns to a standard schema and merges them into a single dataset.
        Displays progress during processing.
        """
        # Define the column mapping
        mapping = {
            '6a. \nStreet #': 'street_number',
            '6b. \nStreet Name': 'street_name',
            '6c. \nStreet Suffix  ': 'street_suffix',
            '6d.\n Unit #': 'unit_number',
            '6e. \nZip': 'zip_code',
            '7. \nUndergraduate (U) or Graduate (G)': 'level_of_study',
            '8. \nFull-time (FT) or \nPart-time (PT)': 'full_time',
            'year_start': 'year_start',
            'year_end': 'year_end',
            'university': 'university'
        }

        console = Console()
        total_files = len(self.files)

        # Progress bar for processing files
        progress = Progress(
            TextColumn("{task.description}", justify="left"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}", justify="right"),
            console=console
        )

        with progress:
            # Main task for processing files
            process_task = progress.add_task("Mapping and merging files", total=total_files)

            # Process each file: map columns and update progress
            for file in self.files:
                file.map(mapping)
                progress.update(process_task, advance=1)

            # Merge all processed files into a single DataFrame
            merged = pd.DataFrame(columns=list(mapping.values()))
            for file in self.files:
                merged = pd.concat([merged, file.dataframe], ignore_index=True)

            self.data = merged

            progress.refresh()

        console.print(f'Mapped and merged {total_files} files.')

    def save(self, path):
        """
        Saves the merged dataset to the specified file path.
        """
        assert self.data is not None, 'No data to save.'

        # Save the DataFrame to CSV
        self.data.to_csv(path, index=False)

        print(f'Data saved to {path}.')


def main(input_directory, output_file):
    """
    Main function to orchestrate the pipeline:
    1. Load Excel files from the input directory.
    2. Consolidate them into a single dataset.
    3. Save the dataset to the specified output file.
    """
    pipeline = DataPreparation(input_directory)
    pipeline.load()
    pipeline.merge()
    pipeline.save(output_file)

if __name__ == '__main__':
    import argparse
    # Set up argument parsing for command-line execution
    parser = argparse.ArgumentParser(description='Process and merge data files with student addresses.')
    parser.add_argument('input', type=str, help='The input directory containing the files to process.', required=True)
    parser.add_argument('output', type=str, help='The output file path to save the processed data.', default='./output.csv')
    args = parser.parse_args()

    # Execute the main function with parsed arguments
    main(args.input, args.output)