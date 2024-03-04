import boto3
import sys
import os
import time
from datetime import datetime, timedelta

def assume_role_and_get_bucket_acl(role_arn, session_name, bucket_name):
    sts_client = boto3.client('sts')
    assumed_role = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName=session_name,
        DurationSeconds=900
    )
    credentials = assumed_role['Credentials']

    s3_client = boto3.client(
        's3',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )

    try:
        print(f"Requesting {bucket_name} using session name: {session_name}")
        s3_client.get_bucket_acl(Bucket=bucket_name)
    except Exception:
        pass

def search_cloudtrail_logs(profile, bucket, start_time, session_names):
    print("Finding session names which passed the VPC endpoint in CloudTrail...")
    found_sessions = []

    cloudtrail_client = boto3.client('cloudtrail', region_name=os.getenv('AWS_REGION', 'us-west-1'))  # Default region as a fallback

    end_time = start_time + timedelta(minutes=15)
    while datetime.utcnow() < end_time and len(found_sessions) < 12:
        for session_name in session_names:
            try:
                events = cloudtrail_client.lookup_events(
                    LookupAttributes=[
                        {
                            'AttributeKey': 'EventName',
                            'AttributeValue': 'GetBucketAcl'
                        },
                    ],
                    StartTime=start_time,
                )
                for event in events['Events']:
                    if session_name in event['CloudTrailEvent'] and session_name not in found_sessions:
                        found_sessions.append(session_name)
                        print(f"Found {session_name} for {bucket} in CloudTrail")
                        if len(found_sessions) >= 12:
                            compile_account_id(found_sessions, bucket)
                            return
                        break
                if datetime.utcnow() >= end_time:
                    break
            except Exception as e:
                print(f"Error searching CloudTrail logs: {e}")
        time.sleep(10)

    if not found_sessions:
        print("No matching sessions found in CloudTrail logs within 15 minutes.")
    else:
        compile_account_id(found_sessions, bucket)

def compile_account_id(found_sessions, bucket):
    if found_sessions:
        account_id = ['0'] * 12
        for session in found_sessions:
            for i, char in enumerate(session):
                if char != '-':
                    account_id[i] = char
                    break
        account_id_str = ''.join(account_id)
        print(f"Bucket {bucket} Account ID: {account_id_str}")
    else:
        print("No matching sessions found in CloudTrail logs within 15 minutes.")

def main(profile, bucket):
    role_arn = os.getenv('ROLE_ARN', 'arn:aws:iam::123456789012:role/example-role') # Default ARN as a fallback
    start_time = datetime.utcnow()
    session_names = [f"{'-'*j}{i}{'-'*(11-j)}" for i in range(10) for j in range(12)]

    for session_name in session_names:
        assume_role_and_get_bucket_acl(role_arn, session_name, bucket)

    search_cloudtrail_logs(profile, bucket, start_time, session_names)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python aws_account_finder.py <profile> <bucket>")
        sys.exit(1)
    
    profile = sys.argv[1]
    bucket = sys.argv[2]
    main(profile, bucket)
