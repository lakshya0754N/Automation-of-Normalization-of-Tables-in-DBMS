from table import Table
from autoNorm import AutoNormalization
import pandas as pd
import numpy as np

csvPath = input("Enter the path of the csv file: ")
tableName = input("Enter the name of the table: ")

normalized = AutoNormalization(csvPath, tableName)

print("Normalized Tables: \n")
for i in range(len(normalized.data)):
    print(f"Table {i+1}: \n {normalized.data[i]} \n\n  {normalized.data[i].table} \n")
