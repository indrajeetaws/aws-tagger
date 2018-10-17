import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--tagkey")
parser.add_argument("-v", "--tagcolumnheader")
parser.add_argument("-f", "--csvfile")

args = parser.parse_args()
tagkey = args.tagkey
columnheader = args.tagcolumnheader
csvfile = args.csvfile

resourceID = 'resource_id'
service = 'service'
columnindex = int()
resourceIDindex = 0
serviceindex = int()

with open(csvfile, 'rU') as csv_file:
            reader = csv.reader(csv_file)
            header_row = True
            for row in reader:
                if header_row:
                    header_row = False
                    for k,v in enumerate(row):
                     if v == resourceID:
                      resourceIDindex = k
                      print("resourceIDindex %s" % k )  
                     if v == service:
                      serviceindex = k
                      print("serviceindex %s" % k )
                     if v == columnheader:
                      columnindex = k
                      print("columnindex %s" % k )

                else:
                      print((row[resourceIDindex],row[serviceindex],row[columnindex]) )
