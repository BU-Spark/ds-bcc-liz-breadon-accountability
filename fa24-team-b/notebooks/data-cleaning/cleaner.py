from rapidfuzz import process, fuzz
from tqdm import tqdm
import pandas as pd
import os

class Cleaning:
    """
    Cleans and standardizes street-related columns in a dataset.
    """
    def __init__(self, path):
        """
        Initializes the address cleaning pipeline.
        @param path: str, path to the input CSV file
        """
        assert os.path.exists(path), "File does not exist"

        self.data = pd.read_csv(path)
        self.words = {}
        self.grouped = {}
        self.mapping = {}

    def preprocess(self):
        """
        Cleans and standardizes the street-related columns.
        """
        self.data['street_number'] = self.data['street_number'].fillna('').replace('nan', '')
        self.data['street_name'] = self.data['street_name'].fillna('').replace('nan', '')
        self.data['street_suffix'] = self.data['street_suffix'].fillna('').replace('nan', '')
        self.data['unit_number'] = self.data['unit_number'].fillna('').replace('nan', '')

        self.data['street_number'] = self.data['street_number'].str.replace(r'[^0-9a-zA-Z]+', ' ', regex=True)
        self.data['street_name'] = self.data['street_name'].str.replace(r'[^0-9A-Za-z.,#-]+', ' ', regex=True)
        self.data['street_suffix'] = self.data['street_suffix'].str.replace(r'[^a-zA-Z]+', ' ', regex=True)
        self.data['unit_number'] = self.data['unit_number'].str.replace(r'[^0-9a-zA-Z-]+', ' ', regex=True)

        self.data['street_number'] = self.data['street_number'].str.replace(r'\s+', ' ', regex=True).str.strip()
        self.data['street_name'] = self.data['street_name'].str.replace(r'\s+', ' ', regex=True).str.strip()
        self.data['street_suffix'] = self.data['street_suffix'].str.replace(r'\s+', ' ', regex=True).str.strip()
        self.data['unit_number'] = self.data['unit_number'].str.replace(r'\s+', ' ', regex=True).str.strip()

        self.data['street'] = (
            self.data['street_number'] + ' ' +
            self.data['street_name'] + ' ' +
            self.data['street_suffix'] + ' ' +
            self.data['unit_number']
        )

        self.data['street'] = (
            self.data['street']
            .str.replace(r'[^0-9a-zA-Z]+', ' ', regex=True)
            .str.replace(r'\s+', ' ', regex=True)
            .str.strip()
            .str.lower()
        )

        print("Preprocessing complete.")

    def build_word_dictionary(self):
        """
        Extracts and counts unique words from the street column.
        """
        self.words = {}

        for _, row in tqdm(self.data.iterrows(), total=len(self.data), desc="Building word dictionary"):
            for word in row['street'].split():
                if len(word) < 3 or any(char.isdigit() for char in word):
                    continue
                self.words[word] = self.words.get(word, 0) + 1

    def group_words(self):
        """
        Groups similar words based on a fuzz ratio threshold.
        """
        temp_grouped = list(self.words.keys())
        new_grouped = {}

        for word in tqdm(temp_grouped, desc="Grouping similar words"):
            choices = list(new_grouped.keys())

            if not choices:
                new_grouped[word] = [word]
                continue

            best = process.extractOne(word, choices)
            if best and fuzz.ratio(word, best[0]) > 90:
                new_grouped[best[0]].append(word)
            else:
                new_grouped[word] = [word]

        updated_grouped = {}
        for key, values in new_grouped.items():
            representative = sorted(values, key=lambda x: self.words[x], reverse=True)[0]
            updated_grouped[representative] = values

        self.grouped = updated_grouped

    def create_mapping(self):
        """
        Creates a mapping of each word to its representative.
        """
        self.mapping = {value: key for key, values in self.grouped.items() for value in values}

    def apply_mapping(self):
        """
        Updates the street column by replacing words with their mapped representative.
        """
        self.data['street'] = self.data['street'].apply(
            lambda x: ' '.join([self.mapping.get(word, word) for word in x.split()])
        )
        self.data['street'] = self.data['street'].str.replace(r'\s+', ' ', regex=True).str.strip()

    def clean(self):
        """
        Orchestrates the cleaning process.
        """
        self.preprocess()
        while True:
            self.build_word_dictionary()
            previous_grouped = self.grouped.copy()
            self.group_words()
            if self.grouped == previous_grouped:
                break
            self.create_mapping()
            self.apply_mapping()

    def save(self, output_path):
        """
        Saves the cleaned dataset.
        @param output_path: str, path to save the cleaned CSV file
        """
        self.data.to_csv(output_path, index=False)
        
        print(f"Cleaned data saved to {output_path}.")

def main(input_path, output_path):
    """
    Main function to orchestrate the pipeline:
    1. Load the dataset from the input file.
    2. Clean and standardize the street-related columns.
    3. Save the cleaned dataset to the specified output file.
    @param input_path: str, path to the input CSV file
    @param output_path: str, path to save the cleaned CSV file
    """
    cleaner = Cleaning(input_path)
    cleaner.clean()
    cleaner.save(output_path)


if __name__ == '__main__':
    import argparse
    # Set up argument parsing for command-line execution
    parser = argparse.ArgumentParser(description="Clean street-related columns in a dataset.")
    parser.add_argument("input", type=str, help="Path to the input CSV file.", required=True)
    parser.add_argument("output", type=str, help="Path to save the cleaned CSV file.", default='./output.csv')
    args = parser.parse_args()
   
    # Execute the main function with parsed arguments
    main(args.input, args.output)
