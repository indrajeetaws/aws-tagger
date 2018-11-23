import csv, sys
import boto3

## Change the TagKeyName accordingly ##
TagKeyName = 'Channel'
TagValue = True
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
                  print("Not have any value")
                  continue
            if service_names[row[column_index['service']]] == 'ec2':
                print("It is EC2")
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
                       print('tttttttttttttttttt')
                       continue 
                print('create')
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
       
        ## Boto3 method for tagging S3 Bucket ##      
            #print("service:", service_names[row[column_index['service']]], "resource_id:",row[column_index['resource_id']], "tag_channel:",row[column_index['tag_channel']])
            if service_names[row[column_index['service']]] == 's3':
                print("It is S3")
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
       
        ## Boto3 method for tagging Lambda ##      
            if service_names[row[column_index['service']]] == 'lambda':
                print("It is Lambda")
                response = client_lambda.tag_resource(
                    Resource = row[column_index['resource_id']],
                    Tags={
                           TagKeyName : row[column_index['tag_channel']]
                       }
                   ),
       
        ## Boto3 method for tagging CloudWatch log Groups ##      
	        if service_names[row[column_index['service']]] == 'logs':
                        print("It is CloudWatch")
		        response = client_cloudwatch.tag_log_group(
		        logGroupName= row[column_index['resource_id']],
		        tags={
			           TagKeyName: row[column_index['tag_channel']]
		           }
		       ),
       
        ## Boto3 method for tagging RDS ##      
            if service_names[row[column_index['service']]] == 'rds': 
                print("It is RDS")             
                response = client_rds.add_tags_to_resource(
                    ResourceName= row[column_index['resource_id']],
                    Tags=[
                        {
                            'Key': TagKeyName,
                            'Value': row[column_index['tag_channel']]
                        }
                    ]
                ),
       
        ## Boto3 method for tagging ElasticSearch ##      
            if service_names[row[column_index['service']]] == 'es':
                print("It is ES")
                response = client_es.add_tags(
                    ARN= row[column_index['resource_id']],
                    TagList=[
                        {
                            'Key': TagKeyName,
                            'Value': row[column_index['tag_channel']]
                        }
                    ]
                ),
       
        ## Boto3 method for tagging EMR ##      
            if service_names[row[column_index['service']]] == 'emr':
                print("It is EMR")
                response = client_emr.add_tags(
                    ResourceId= row[column_index['resource_id']],
                    Tags=[
                        {
                            'Key': TagKeyName,
                            'Value': row[column_index['tag_channel']]
                        }
                    ]
                ),
       
        ## Boto3 method for tagging DynamoDB ##      
            if service_names[row[column_index['service']]] == 'dynamodb':
                print("It is DynamoDB")
                response = client_dynamodb.tag_resource(
                    ResourceArn= row[column_index['resource_id']],
                    Tags=[
                        {
                            'Key': TagKeyName,
                            'Value': row[column_index['tag_channel']]
                        }
                    ]
                ),
       
        ## Boto3 method for tagging Firehose ##      
            if service_names[row[column_index['service']]] == 'firehose':
                print("It is Firehose")
                response = client_firehose.tag_delivery_stream(
                    DeliveryStreamName= row[column_index['resource_id']],
                    Tags=[
                        {
                            'Key': TagKeyName,
                            'Value': row[column_index['tag_channel']]
                        }
                    ]
                ),
       
        ## Boto3 method for tagging Glacier ##      
            if service_names[row[column_index['service']]] == 'glacier':
                print("It is Glacier") 
                response = client_glacier.add_tags_to_vault(
                    vaultName= row[column_index['resource_id']],
                    Tags={
                        TagKeyName: row[column_index['tag_channel']] 
                    }
                ),
       
        ## Boto3 method for tagging KMS ##      
            if service_names[row[column_index['service']]] == 'kms':
                print("It is KMS")
                response = client_kms.tag_resource(
                    KeyId= row[column_index['resource_id']],
                    Tags=[
                        {
                            'TagKey': TagKeyName,
                            'TagValue': row[column_index['tag_channel']]
                        }
                    ]
                ),
       
        ## Boto3 method for tagging ApiGateway ##      
            if service_names[row[column_index['service']]] == 'apigateway':
                print("It is ApiGateway")
                response = client_apigateway.tag_resource(
                    resourceArn= row[column_index['resource_id']],
                    tags={
                        TagKeyName: row[column_index['tag_channel']] 
                    }
                ),
       
        ## Boto3 method for tagging Kinesis ##      
            if service_names[row[column_index['service']]] == 'kinesis':
                print("It is Kinesis")
                response = client_kinesis.add_tags_to_stream(
                    StreamName= row[column_index['resource_id']],
                    Tags={
                        TagKeyName: row[column_index['tag_channel']] 
                    }
                ),
       
        ## Boto3 method for tagging CloudTrail ##      
            if service_names[row[column_index['service']]] == 'cloudtrail':
                print("It is CloudTrail")
                response = client_cloudtrail.add_tags(
                    ResourceId= row[column_index['resource_id']],
                    TagsList=[
                        {
                            'Key': TagKeyName,
                            'Value': row[column_index['tag_channel']]
                        }
                    ]
                ),
       
        ## Boto3 method for tagging SQS ##      
            if service_names[row[column_index['service']]] == 'sqs':
                print("It is sqs")
                response = client_sqs.tag_queue(
                    QueueUrl= row[column_index['resource_id']],
                    Tags={
                        TagKeyName: row[column_index['tag_channel']]
                    }
                ),

        ## Boto3 method for tagging SecretsManager ##      
          #To run this command, you must have the following permissions:
                      # secretsmanager:TagResource
            if service_names[row[column_index['service']]] == 'secretsmanager':
                print("It is SecretsManager")
                response = client_secretsmanager.tag_resource(
                    SecretId = row[column_index['resource_id']],
                    Tags=[
                       {
                        'Key': TagKeyName,
                        'Value': row[column_index['tag_channel']]
                       }
                     ]
                   ),
 
        ## Boto3 method for tagging CloudFront ##      
            if service_names[row[column_index['service']]] == 'cloudfront':
                print("It is CloudFront")
                response = client_cloudfront.tag_resource(
                   Resource = row[column_index['resource_id']],
                   Tags={
                        'Items': [
                       {
                        'Key': TagKeyName,
                        'Value': row[column_index['tag_channel']]
                       }
                     ]
                   }
                 ),

        ## Boto3 method for tagging EFS ##      
            if service_names[row[column_index['service']]] == 'efs':
                print("It is EFS")
                response = client_efs.create_tags(
                    FileSystemId = row[column_index['resource_id']],
                    Tags=[
                       {
                        'Key': TagKeyName,
                        'Value': row[column_index['tag_channel']]
                       }
                    ]
                 ),

        ## Boto3 method for tagging Sagemaker ##      
            if service_names[row[column_index['service']]] == 'sagemaker':
                print("It is SageMaker")
                response = client_sagemaker.add_tags(
                    FileSystemId = row[column_index['resource_id']],
                    Tags=[
                       {
                        'Key': TagKeyName,
                        'Value': row[column_index['tag_channel']]
                       }
                    ]
                 ),

        ## Boto3 method for tagging Redshift ##      
            if service_names[row[column_index['service']]] == 'redshift':
                print("It is Redshift")
                response = client_redshift.create_tags(
                    ResourceName = row[column_index['resource_id']],
                    Tags=[
                       {
                        'Key': TagKeyName,
                        'Value': row[column_index['tag_channel']]
                       }
                    ]
                 ),

        ## Boto3 method for tagging ElastiCache ##      
            if service_names[row[column_index['service']]] == 'elasticache':
                print("It is ElastiCache")
                response = client_elasticache.add_tags_to_resource(
                    ResourceName = row[column_index['resource_id']],
                    Tags=[
                       {
                        'Key': TagKeyName,
                        'Value': row[column_index['tag_channel']]
                       }
                    ]
                 ),

        ## Boto3 method for tagging Workspaces ##      
            if service_names[row[column_index['service']]] == 'workspaces':
                print("It is WorkSpaces")
                response = client_workspaces.create_tags(
                    ResourceId = row[column_index['resource_id']],
                    Tags=[
                       {
                        'Key': TagKeyName,
                        'Value': row[column_index['tag_channel']]
                       }
                    ]
                 ),

        ## Boto3 method for tagging DirectoryService ##      
            if service_names[row[column_index['service']]] == 'ds':
                print("It is DirectoryService")
                response = client_ds.add_tags_to_resource(
                    ResourceId = row[column_index['resource_id']],
                    Tags=[
                       {
                        'Key': TagKeyName,
                        'Value': row[column_index['tag_channel']]
                       }
                    ]
                 ),

        ## Boto3 method for tagging DAX ##      
            if service_names[row[column_index['service']]] == 'dax':
                print("It is DAX")
                response = client_dax.tag_resource(
                    ResourceName = row[column_index['resource_id']],
                    Tags=[
                       {
                        'Key': TagKeyName,
                        'Value': row[column_index['tag_channel']]
                       }
                    ]
                 ),

        ## Boto3 method for tagging Route53 ##      
            if service_names[row[column_index['service']]] == 'route53':
                print("It is Route53")
                response = client_route53.change_tags_for_resource(
                    ResourceType = 'healthcheck'|'hostedzone',
                    ResourceId = row[column_index['resource_id']],
                    AddTags=[
                       {
                        'Key': TagKeyName,
                        'Value': row[column_index['tag_channel']]
                       }
                    ]
                 ),

        ## Boto3 method for tagging DirectConnect ##      
            if service_names[row[column_index['service']]] == 'directconnect':
                print("It is Direct Connect")
                response = client_directconnect.tag_resource(
                    resourceArn = row[column_index['resource_id']],
                    tags=[
                       {
                        'Key': TagKeyName,
                        'Value': row[column_index['tag_channel']]
                       }
                    ]
                 ) 
