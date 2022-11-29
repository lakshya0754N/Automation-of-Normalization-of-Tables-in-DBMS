from table import Table
from autoNorm import AutoNormalization
import pandas as pd
import numpy as np
import pandas as pd
import mysql.connector

csvPath = input("Enter the path of the csv file: ")
tableName = input("Enter the name of the table: ")
directory = input("Enter the path of the directory to save the normalized tables: ")

normalized = AutoNormalization(csvPath, tableName)

conn=mysql.connector.connect(host='localhost',port=3306,user='lakshya0754n', password='lakshya',database='dbTest')

def insertinSQL(tableName, df):
    Attr=df.columns
    cursor = conn.cursor()
    dataType=list(df.dtypes)
    arr=[]
    for i in dataType:
        if i=='int64':
            arr.append('int')
        elif i=='float64':
            arr.append('float')
        elif i=='O':
            arr.append('varchar(255)')
        elif i=='bool':
            arr.append('bool')
    
    variables=""
    for i in range(len(Attr)):
        variables+=Attr[i]+" " + str(arr[i]) + ","
    variables = variables.rstrip(variables[-1])
    query="CREATE TABLE "+tableName+" (" + variables+");"
    df=df.values
    cursor.execute(query)
    for row in df:
        row=tuple(row)
        s=""
        for j in row:
            s+="%s,"
        s=s.rstrip(s[-1])
    
        q="Insert into "+tableName+" Values ("+s+")"
        cursor.execute(q, row)
        conn.commit()

print("Normalized Tables: \n")
for i in range(len(normalized.data)):
    normalized.data[i].exportTable(directory)
    print(f"Table {i+1}: \n {normalized.data[i]} \n\n  {normalized.data[i].table} \n")
    insertinSQL(normalized.data[i].tableName,normalized.data[i].table)

conn.close()