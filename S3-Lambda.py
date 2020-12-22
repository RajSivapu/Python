##
# This script triggers a lambda function which monitors S3 buckets and send emails when a new document gets uploaded to S3
import json
import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
        for i in event["Records"]:
            action = i["eventName"]
            ip = i["requestParameters"]["sourceIPAddress"]
            bucket_name = i["s3"]["bucket"]["name"]
            objects = i["s3"]["object"]["key"]   
        print (objects)
        data = s3.get_object(Bucket=bucket_name, Key=objects)
        json_data = data['Body']
        jsonobject = json.loads(json_data.read());

        if jsonobject['violations'][0]['owner'] == jsonobject['violations'][0]['ack_details']["acknowledged_by"]:
            print("name matched now")
            domain = "@gmail.com"
            reciever_email = jsonobject['violations'][0]['owner']
            client = boto3.client("ses")

            subject = "test lamda triggered email"
            body = """
                This is a test email
            """

            message = {"Subject": {"Data": subject}, "Body": {"Html": {"Data": body}}}
            response = client.send_email(Source = "XXXXXXXX" + domain, Destination = {"ToAddresses": [reciever_email + domain]}, Message = message)
        else:
            print("name not matched")    
            s3.delete_object(Bucket=bucket_name, Key=objects)