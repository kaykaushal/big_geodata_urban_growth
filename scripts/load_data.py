import pandas as pd
import numpy as np 
import yaml
#import rasterio
from pathlib import Path

# function to get data links from download.yml file

def load_data(area, year):
    # check if file exists
    file_path = Path("download.yml")
    if file_path.exists():
        # open file using PyYAML library
        with open(file_path) as f:
            data = yaml.safe_load(f)
            url = data[area][year]
            print(url)
            return url
    else:
        print("File not found.")


