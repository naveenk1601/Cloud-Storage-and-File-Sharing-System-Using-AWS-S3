import boto3
import json

# AWS Configuration
aws_access_key_id = 'YOUR_AWS_ACCESS_KEY'
aws_secret_access_key = 'YOUR_AWS_SECRET_KEY'
region_name = 'YOUR_REGION'

# Initialize S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

# Create S3 bucket
bucket_name = 'your-unique-bucket-name'
s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
    'LocationConstraint': region_name})

# Set bucket policy
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{bucket_name}/*"
        }
    ]
}

s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(bucket_policy))

# Enable versioning
s3.put_bucket_versioning(
    Bucket=bucket_name,
    VersioningConfiguration={
        'Status': 'Enabled'
    }
)

# Set lifecycle policy (example: delete old versions after 30 days)
lifecycle_policy = {
    'Rules': [
        {
            'ID': 'DeleteOldVersions',
            'Status': 'Enabled',
            'NoncurrentVersionExpiration': {
                'NoncurrentDays': 30
            }
        }
    ]
}

s3.put_bucket_lifecycle_configuration(Bucket=bucket_name, LifecycleConfiguration=lifecycle_policy)

# Enable CloudWatch logging
cloudwatch_logs = boto3.client('logs', aws_access_key_id=aws_access_key_id, 
                                aws_secret_access_key=aws_secret_access_key, region_name=region_name)

log_group_name = 'S3Logs'
cloudwatch_logs.create_log_group(logGroupName=log_group_name)

print(f'S3 bucket "{bucket_name}" created and configured successfully!')
