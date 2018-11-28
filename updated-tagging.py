import csv, sys
import boto3



## Change the TagKeyName accordingly ##

TagKeyName = 'Channel'

TagValue = False

## Change the input parameters accordingly ##

column_headers = ["tag_channel", "resource_id", "service"]

column_index = {"tag_channel": None, "resource_id": None, "service": None}

service_names = {"AmazonEC2": "ec2", "AmazonS3": "s3", "AmazonVPC": "ec2", "AWSLambda":"lambda", "AmazonCloudWatch":"logs", "AmazonRDS":"rds", "AmazonES":"es", "ElasticMapReduce":"emr", "AmazonDynamoDB":"dynamodb", "AmazonKinesisFirehose":"firehose", "AmazonGlacier":"glacier", "awskms":"kms", "AmazonApiGateway":"apigateway", "AmazonKinesis":"kinesis", "AWSCloudTrail":"cloudtrail", "AWSQueueService":"sqs", "AWSSecretsManager": "secretsmanager", "AmazonCloudFront": "cloudfront", "AmazonEFS": "efs", "AmazonSageMaker": "sagemaker", "AmazonRedshift": "redshift", "AmazonElastiCache": "elasticache", "AmazonWorkSpaces": "workspaces", "AWSDirectoryService": "ds", "AmazonDAX": "dax", "AmazonRoute53": "route53", "AWSDirectConnect": "directconnect"}

#

found_headers=False

#

## creating clients for different services using boto3 ##

client_ec2 = boto3.client("ec2")

client_s3 = boto3.client("s3") 

client_lambda = boto3.client("lambda")

client_cloudwatch = boto3.client("logs")

client_rds = boto3.client("rds")

client_es = boto3.client("es")

client_emr = boto3.client("emr")

client_dynamodb = boto3.client("dynamodb")

client_firehose = boto3.client("firehose")

client_glacier = boto3.client("glacier")

client_kms = boto3.client("kms")

client_apigateway = boto3.client("apigateway")

client_kinesis = boto3.client("kinesis")

client_cloudtrail = boto3.client("cloudtrail")

client_sqs = boto3.client("sqs")

client_secretsmanager = boto3.client("secretsmanager")

client_cloudfront = boto3.client("cloudfront")

client_efs = boto3.client("efs")

client_sagemaker = boto3.client("sagemaker")

client_redshift = boto3.client("redshift")

client_elasticache = boto3.client("elasticache")

client_workspaces = boto3.client("workspaces")

client_ds = boto3.client("ds")

client_dax = boto3.client("dax")

client_route53 = boto3.client("route53")

client_directconnect = boto3.client("directconnect")



## Change the .csv input file name accordingly ##

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

                    print("Caught an exception when looking up index:",e)

                # unable to locate column header from file; exit program

                    sys.exit()

           # assign to True to skip header lookup on next row

            found_headers = True

        else:

           # print tag and its index

           # print(row)

            print("service:", service_names[row[column_index['service']]], "resource_id:",row[column_index['resource_id']], "tag_channel:",row[column_index['tag_channel']])

       #

        ## Boto3 method for tagging EC2 Instance ##    

            if row[column_index['tag_channel']].lower() == 'none' or row[column_index['tag_channel']].lower() == 'unknown':

                  print("Skipping update since resource id "+row[column_index['resource_id']]+" has value of none or unknown")

                  continue

            if service_names[row[column_index['service']]] == 'ec2':

                print("It is EC2", service_names[row[column_index['service']]])

                responsetag = client_ec2.describe_tags(

                           Filters=[

                             {

                              'Name': 'resource-id',

                              'Values': [

                               row[column_index['resource_id']],

                                ],

                             },

                            ],

                          )

          #      print(responsetag)

                keys = [tag['Key'].upper() for tag in responsetag['Tags']] 

                if  TagKeyName.upper() in keys:

                    if TagValue == False:

                       print("Tag "+TagKeyName+" already exists for resource id "+row[column_index['resource_id']])

                       continue 

                print('create')
                try:
                  response = client_ec2.create_tags(

                    DryRun = False,

                    Resources = [

                        row[column_index['resource_id']],

                    ],

                    Tags=[

                       {

                        'Key': TagKeyName,

                        'Value': row[column_index['tag_channel']]

                       }

                     ]

                   ),
                except Exception as e:
                  print(" EC2 Unable to create/update tag:",e)
				
                  continue
       

        ## Boto3 method for tagging S3 Bucket ##      

            #print("service:", service_names[row[column_index['service']]], "resource_id:",row[column_index['resource_id']], "tag_channel:",row[column_index['tag_channel']])

            if service_names[row[column_index['service']]] == 's3':

                print("It is S3")
	        try:
                    response = client_s3.get_bucket_tagging(
					
		         Bucket= row[column_index['resource_id']],
		         )

                except Exception as e:
                     print("Get Unable to create/update tag:",e)
                     continue

                keys = [tag['Key'].upper() for tag in responsetag['Tags']] 

                if  TagKeyName.upper() in keys:

                    if TagValue == False:

                       print("Tag "+TagKeyName+" already exists for resource id "+row[column_index['resource_id']])

                       continue 

                print('create')
	        try:
	          response = client_s3.put_bucket_tagging(

                    Bucket = row[column_index['resource_id']],

                    Tagging={

                        'TagSet':[

                             {

                                     'Key': TagKeyName,

                                     'Value': row[column_index['tag_channel']]

                              }

                          ]

                       }

                    ),
                except Exception as e:
                    print(" Put Unable to create/update tag:",e)
                    continue
       
