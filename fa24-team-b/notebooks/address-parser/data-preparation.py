import pandas as pd
import os

class DataPreparation:
    """
    A pipeline to prepare address data for NLP tasks by processing, cleaning,
    and splitting the data into files with and without unit numbers.
    """
    def __init__(self, input_path, output_dir):
        """
        Initializes the data preparation pipeline.
        @param input_path: str, path to the input CSV file
        @param output_dir: str, path to the output directory
        """
        assert os.path.exists(input_path), "Input file does not exist."
        assert os.path.isdir(output_dir), "Output directory does not exist."

        self.data = pd.read_csv(input_path, low_memory=False)
        self.output_dir = output_dir

    def preprocess(self):
        """
        Cleans and standardizes the dataset by retaining relevant columns and dropping rows with missing essential columns.
        """
        # Select only relevant columns
        columns_to_keep = [
            'street_number',
            'street_name',
            'street_suffix',
            'unit_number',
        ]
        self.data = self.data[columns_to_keep]

        # Drop rows with missing essential address components
        self.data = self.data.dropna(subset=['street_number', 'street_name', 'street_suffix'])

    def save(self):
        """
        Saves the cleaned dataset to a CSV file.
        """
        print("Saving cleaned data to CSV file at {}.".format(os.path.join(self.output_dir, 'train.csv')))
        self.data.to_csv(os.path.join(self.output_dir, 'train.csv'), index=False)
        

def main(input, output):
    """
    Main function to execute the data preparation pipeline.
    @param input: str, path to the input CSV file
    @param output: str, path to the output directory
    """
    preparator = DataPreparation(input, output)
    preparator.preprocess()
    preparator.save()
    
    print("Data preparation complete.")

    
if __name__ == '__main__':
    import argparse
    # Set up argument parsing for command-line execution
    parser = argparse.ArgumentParser(description="Prepare address data for NLP tasks.")
    parser.add_argument("input", type=str, help="Path to the input CSV file.")
    parser.add_argument("output", type=str, help="Path to the output directory.")
    args = parser.parse_args()

    # Execute the main function with parsed arguments
    main(args.input, args.output)

