import chess, os, csv, datetime
import random

class Kkr_DataSets():

    types = ['train', 'valid', 'test']
    percentages = [0.1, 0.01, 0.001]

    def __init__(self, out_dir = r"..\data", out_file = "KRk_new.csv"):
        self.out_dir = out_dir
        self.out_file = out_file
        self.threshold = [self.percentages[0], self.percentages[0] + self.percentages[1],  self.percentages[0] + self.percentages[1] + self.percentages[2]]

    def create_output_files(self):
        self.out_file_handle = [None, None, None]
        for index, type in enumerate(self.types):
            csv_file = open(os.path.join(self.out_dir, type, self.out_file), mode='w', newline='')
            self.out_file_handle[index] = csv.writer(csv_file, delimiter=',')
            
    def read_all_files(self):
        self.create_output_files()
        for filename in os.listdir(self.out_dir):
            # Check if the file has a CSV extension
            if filename.endswith(".csv"):
                # Construct the full path to the CSV file
                csv_file_path = os.path.join(self.out_dir, filename)

                # Process the CSV file
                with open(csv_file_path, 'r', newline='') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    
                    # Iterate through rows in the CSV file
                    for row in csv_reader:
                        random_nr = random.random()
                        if random_nr <= self.threshold[2]:
                            if random_nr <= self.threshold[0]:
                                writer = self.out_file_handle[0]
                            elif random_nr <= self.threshold[1]:
                                writer = self.out_file_handle[1]
                            else:
                                writer = self.out_file_handle[2]

                            # Process each row as needed
                            writer.writerow(row)

if __name__ == "__main__":
    kkr_dataset = Kkr_DataSets()
    kkr_dataset.read_all_files()