import csv, sys
import boto3


column_headers = ["tag_channel", "resource_id", "service"]
column_index = {"tag_channel": None, "resource_id": None, "service": None}
service_names = {"AmazonEC2": "ec2", "AmazonS3": "s3api", "AmazonVPC": "ec2"}

found_headers=False
client = boto3.client("ec2")
with open("sample_september.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
     # read csv file row by row
    for row in csv_reader:
        if not found_headers:
                # loop through list containing column headers
            for header in column_headers:
                try:
                           # find index for column header
                    column_index[header] = row.index(header)
                except Exception as e:
                    print("Caught an exception when looking up index:", e)
                           # unable to locate column header from file; exit program
                    sys.exit()
                # assign to True to skip header lookup on next row
            found_headers=True
        else:
                # print tag and its index
            #print(row)
            print("service:", service_names[row[column_index['service']]], "resource_id:",row[column_index['resource_id']], "tag_channel:",row[column_index['tag_channel']])
            if service_names[row[column_index['service']]] == 'ec2':
                print("It is EC2")

                response = client.create_tags(
                    DryRun = False,
                    Resources = [
                        row[column_index['resource_id']],
                    ],
                    Tags=[{
                       'Key': 'Channel',
                       'Value': row[column_index['tag_channel']]
                    }]
