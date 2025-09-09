
# The  Data Ingestion Artifacts inclues all the outputs that we want 
# from Data Ingestion Component
# The output of DataIngestion Component should be the 
# trained_file_path and test_file_path

from dataclasses import dataclass
# dataclass creates variable for an empty class

@dataclass
class DataIngestionArtifact:
    trained_file_path:str
    test_file_path:str
