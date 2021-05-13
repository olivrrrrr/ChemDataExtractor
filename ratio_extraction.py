from chemdataextractor.doc import Document, Heading, Paragraph
from chemdataextractor.scrape import Selector
from chemdataextractor.scrape.pub.rsc import RscHtmlDocument
from chemdataextractor.reader import AcsHtmlReader, RscHtmlReader, PdfReader
import os
import sys 
import csv 
 
with open('file_name' ,'rb') as file:   
    doc = Document.from_file(file)

# initialise with an empty dictionary
compoundInfo = {}
# Produce the list of dictionaries
doc_records = doc.records.serialize()   
# filter to only ratio information 
ratio_doc_records = [record for record in doc_records if 'ratio' in record]

# using a loop extract the ratio information within ratio_doc_records 
i = 0 
for i in range(len(ratio_doc_records)):
    for key, value in ratio_doc_records[i].items():  
        compoundInfo[key] = value
# Only allow Name and Ratio information, don't show any other attributes
        if (key == 'nmr_spectra' or key == 'ir_spectra' or key == 'melting_points' or key == 'labels' or key == 'roles'):
            del compoundInfo[key]
        
# Open a new CSV file and append this information     
    with open('csv_filename', 'a', newline='') as f:
        fieldnames = ['names', 'ratio']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        f.seek(0,2)
        
# If there is nothing written in the csv write a header        
        if f.tell() == 0:
            writer.writeheader()
       
        writer.writerow(compoundInfo)
     
     # This gets desired CSV information format

import pandas as pd
from urllib.request import urlopen
import csv
from csv import writer
import pandas as pd
import numpy as np 
import re

df = pd.read_csv('Extracted_Information.csv')

# This removes all brackets 
df['names'] = df['names'].map(lambda x: x.lstrip('[\'').rstrip('\']'))

df.to_csv(("CSV1.csv"), index=False)

# This splits all title names and then creates compound columns
split = lambda x: pd.Series([i for i in reversed(x.replace(', ','$').replace(' and ', '$' ).split('$'))])
rev =  df['names'].apply(split)
rev.rename(columns={0:'Compound 1', 1:'Compound 2', 2:'Compound 3', 3:'Compound 4', 4:'Compound 5'},inplace=True)
rev = rev[['Compound 1','Compound 2','Compound 3','Compound 4', 'Compound 5']]

rev.to_csv(('CSV2.csv'), index=False)
rev.head()

df2 = pd.read_csv('CSV2.csv')

# This removes all quotation marks
df2['Compound 1'] = df2['Compound 1'].astype(str).str.strip('\'"') 
df2['Compound 2'] = df2['Compound 2'].astype(str).str.strip('\'"')
df2['Compound 3'] = df2['Compound 3'].astype(str).str.strip('\'"')
df2['Compound 4'] = df2['Compound 4'].astype(str).str.strip('\'"')
df2['Compound 5'] = df2['Compound 5'].astype(str).str.strip('\'"')

# This removes all labels marks (e.g. 'C14-C3')
for column in df2.columns: 
    df2[column] = df2[column].str.replace(r'((\d\d-\w\d))',"")
    df2[column] = df2[column].str.replace(r'((\d-\w\d))',"")
    df2[column] = df2[column].str.replace(r'(\d\d-\w\d)',"")
    df2[column] = df2[column].str.replace(r'(\d\d-\s\w\d)',"")
    df2[column] = df2[column].str.replace(r'\(',"")
    df2[column] = df2[column].str.replace(r'\)',"")
    
df2.to_csv(('CSV3.csv'), index=False)
df2.head()

# This add ratio information
ratioArr = []

for element in df['ratio']:
    ratioArr += [element]

df2['ratio'] = ratioArr

df2.to_csv(("CSV3.csv"), index=False)
df2.head()

dataframe = pd.read_csv('CSV3.csv') 
dataframe.replace(np.nan,0)

# This adds SMILES information for each compound in each row
def CIRconvert(ids):
    try:
        url = 'http://cactus.nci.nih.gov/chemical/structure/' + ids + '/smiles'
        ans = urlopen(url).read().decode('utf8')
        return ans
    except:
        return 'Did not work'

identifiers  = []
identifiers2  = []
identifiers3  = []
identifiers4  = []
identifiers5  = []

for element in dataframe['Compound 1']: 
    identifiers += [CIRconvert(element)]
dataframe['SMILES_Compound_1'] = identifiers

for element in dataframe['Compound 2']: 
    identifiers2 += [CIRconvert(element)]
dataframe['SMILES_Compound_2'] = identifiers2

for element in dataframe['Compound 3']: 
    identifiers3 += [CIRconvert(element)]
dataframe['SMILES_Compound_3'] = identifiers3

for element in dataframe['Compound 4']: 
    identifiers4 += [CIRconvert(element)]
dataframe['SMILES_Compound_4'] = identifiers4

for element in dataframe['Compound 5']: 
    identifiers5 += [CIRconvert(element)]
dataframe['SMILES_Compound_5'] = identifiers5

# This removes all information that only includes one ratio or more than one ratio
containsComma = dataframe[~dataframe['ratio'].str.contains(',')].index
containsLetterA = dataframe[dataframe['ratio'].str.contains('A|a')].index
dataframe.drop(containsComma, inplace=True)
dataframe.drop(containsLetterA, inplace=True)

dataframe.to_csv(("CSV4.csv"), index=False)
dataframe.head()
