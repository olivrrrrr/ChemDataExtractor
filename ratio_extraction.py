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
