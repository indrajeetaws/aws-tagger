import csv, sys
import boto3


column_headers = ["tag_channel", "resource_id", "service"]
column_index = {"tag_channel": None, "resource_id": None, "service": None}
service_names = {"AmazonEC2": "ec2", "AmazonS3": "s3api", "AmazonVPC": "ec2", "AWSLambda": "lambda", "AmazonApiGateway": "apigateway"}

found_headers=False
client = boto3.client("ec2")
clientAPIGateway = boto3.client("apigateway")
clientLambda = boto3.client("lambda")

with open("sample_september.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
     # read csv file row by row
    for row in csv_reader:
        if not found_headers:
                # loop through list containing column headers
            print("column_index:", column_index)
            for header in column_headers:
                try:
                    print("Header:", header)
                          # find index for column header
                    column_index[header] = row.index(header)
                    print("column_index[header] ", column_index[header])
                except Exception as e:
                    print("Caught an exception when looking up index:", e)
                           # unable to locate column header from file; exit program
                    sys.exit()
                # assign to True to skip header lookup on next row
            found_headers=True
            print("column_index:", column_index)
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
                       }])
            if service_names[row[column_index['service']]] == 'apigateway':
                print("API Gateway")
                response = clientAPIGateway.tag_resource(
                    resourceArn = row[column_index['resource_id']],
                    tags={
                           'Channel' : row[column_index['tag_channel']]
                       })
            if service_names[row[column_index['service']]] == 'lambda':
                print("AWS Lambda")
                response = clientLambda.tag_resource(
                    Resource = row[column_index['resource_id']],
                    Tags={
                           'Channel' : row[column_index['tag_channel']]
                       })
