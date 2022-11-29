import streamlit as st
import pandas as pd
from table import Table
from autoNorm import AutoNormalization

st.set_page_config(page_title="auto-normalization-in-dbms", page_icon=":bar_chart:")

st.subheader("Hi! I am Tushar")
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

st.subheader("Normalized Tables: \n")
    
for i,tbl in enumerate(normalized.data):
    st.write(f"Table{i+1} : {tbl.tableName}")
    st.write(tbl.table)
    pKey = ""
    for attr in tbl.primaryKeys:
        pKey += attr + " "
    st.write(f"Primary Key: {pKey}")
    print(tbl.primaryKeys)
    