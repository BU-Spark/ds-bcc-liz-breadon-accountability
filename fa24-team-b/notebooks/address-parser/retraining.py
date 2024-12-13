import re
import pandas as pd
import random
import os
from deepparse.dataset_container import ListDatasetContainer
from deepparse.parser import AddressParser
import poutyne

class Retraining:
    """
    A pipeline to retrain an existing address model model with new training data.
    """
    def __init__(self, path_to_train, path_to_model = None,):
        """
        Initializes the model retraining pipeline.
        @param path_to_model: str, path to the existing model file
        @param path_to_train: str, path to the training data file
        """
        assert os.path.exists(path_to_train), "Training data file does not exist."
        
        self.model = AddressParser(device='cpu', model_type='bpemb')
        if path_to_model:
            self.model = AddressParser(device='cpu', model_type='bpemb', path_to_model=path_to_model)

        self.train = pd.read_csv(path_to_train)

    def prepare(self):

        def process_str(s):
            if pd.isna(s):
                return pd.NA
            s = re.sub(r'\s+', ' ', s)
            s = s.strip()

            if s == '':
                return pd.NA

            return s.lower()
        self.train['street_number'] = self.train['street_number'].apply(process_str)
        self.train['street_name'] = self.train['street_name'].apply(process_str)
        self.train['street_suffix'] = self.train['street_suffix'].apply(process_str)
        self.train['unit_number'] = self.train['unit_number'].apply(process_str)
        
        def split_into_tokens(s):
            if pd.isna(s):
                return []
            return s.split(' ')
        
        self.train['street_number'] = self.train['street_number'].apply(split_into_tokens)
        self.train['street_name'] = self.train['street_name'].apply(split_into_tokens)
        self.train['street_suffix'] = self.train['street_suffix'].apply(split_into_tokens)
        self.train['unit_number'] = self.train['unit_number'].apply(split_into_tokens)
        
        train_X = []
        train_Y = []

        for i in range(len(self.train)):
            address = []
            tags = []

            for sn in self.train['street_number'][i]:
                address.append(sn)
                tags.append('StreetNumber')

            for sn in self.train['street_name'][i]:
                address.append(sn)
                tags.append('StreetName')

            for ss in self.train['street_suffix'][i]:
                address.append(ss)
                tags.append('StreetName')

            for un in self.train['unit_number'][i]:
                address.append(un)
                tags.append('Unit')

            train_X.append((' '.join(address).strip()))
            train_Y.append(tags)

        return list(zip(train_X, train_Y))
        
    def retrain_model(self, epochs=3):
        """
        Retrains the existing model using prepared data.
        @param epochs: Number of epochs for training.
        @param batch_size: Batch size for training.
        """
        train_XY = self.prepare()

        random.shuffle(train_XY)

        data = ListDatasetContainer(train_XY)
        lr_scheduler = poutyne.StepLR(step_size=1, gamma=0.1)
        batch_size = 256

        return self.model.retrain(
            data,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[lr_scheduler]
        )


def main(train_path, epochs=3):
    """
    Main function to run the pipeline.
    1. Preprocesses the training data.
    2. Retrains the model.
    3. Tests the model with sample addresses.
    @param train_path: Path to the training data file.
    """
    random.seed(42)
    retrainer = Retraining(path_to_train=train_path)
    return retrainer.retrain_model(retrainer.model, epochs=epochs)

if __name__ == '__main__':
    import argparse
    # Set up argument parsing for command-line execution
    parser = argparse.Argumentmodel(description='Address model Pipeline')
    parser.add_argument('train_path', type=str, help='Path to training data file')
    parser.add_argument('--epochs', type=int, default=3, help='Number of epochs for retraining')
    args = parser.parse_args()

    # Execute the main function with parsed arguments
    main(args.input, args.output)
