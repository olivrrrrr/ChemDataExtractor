import os
import sys 
import csv 

from chemdataextractor.doc import Document

with open('' ,'rb') as file:   
    doc = Document.from_file(file)

doc_records = doc.records.serialize()  

a_file = open('.csv','a') 

writer = csv.writer(a_file)
    
cleaned_doc_records = [record for record in doc_records if 'ratio' in record]
for record in cleaned_doc_records:
        writer.writerow([record]) 
