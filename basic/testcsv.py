import csv
from datetime import datetime

def writecsv(record_list):
    with open('data.csv','a',newline='') as file:
        fw = csv.writer(file)
        fw.writerow(record_list)

dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
record = [dt,'A','B','C']
writecsv(record)        