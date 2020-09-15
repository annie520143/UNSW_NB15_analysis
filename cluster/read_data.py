import csv
import pandas as pd

def read (file):
    with open(file,  newline='') as csvfile:
        packets = pd.read_csv(csvfile)
    
    return packets
