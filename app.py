import streamlit as st
import pandas as pd
from table import Table
from autoNorm import AutoNormalization
import mysql.connector

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


st.set_page_config(page_title="auto-normalization-in-dbms", page_icon=":bar_chart:")

st.subheader("AutoNorm")
st.title("Auto Normalization of the table: ")

tableName = st.text_input("Enter the name of the table: ")
uploadedFile = st.file_uploader("Choose a file")

if uploadedFile is not None:
    df = pd.read_csv(uploadedFile)
else:
    raise Exception("Please upload a csv file")
  
directory = "data"

normalized = AutoNormalization("", tableName, df)

st.subheader("The Original Table")
st.write(f"Table {tableName}")
st.write(normalized.orgTable.table)
pKey = ""
for attr in normalized.orgTable.primaryKeys:
    pKey += attr + " "
st.write(f"Primary Key: {pKey}")

# st.write("Functional Dependencies...")
# for fd in normalized.orgTable.functionalDependencies:
#     st.write(f"{fd[0]} -> {fd[1]}")

# st.write("Candidate Keys...")
# for key in normalized.orgTable.candidateKeys:
#     st.write(key)

st.subheader("Normalized Tables(BCNF): \n")
    
for i,tbl in enumerate(normalized.data):
    st.write(f"Table{i+1} : {tbl.tableName}")
    insertinSQL(normalized.data[i].tableName,normalized.data[i].table)
    st.write(tbl.table)
    pKey = ""
    for attr in tbl.primaryKeys:
        pKey += attr + " "
    st.write(f"Primary Key: {pKey}")
    print(tbl.primaryKeys)
    
conn.close()