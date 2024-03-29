# AWS Account Finder
Find an AWS Account ID from any S3 Bucket

## Introduction

AWS account IDs alone cannot be used to gain access or control over resources. However, they can be used by security professionals to identify potential targets, particularly when searching for exposed AWS resources without adequate security controls. Account IDs can also contribute to the effectiveness of social engineering attacks or targeted phishing campaigns. In AWS environments where other vulnerabilities or misconfigurations exist, an account ID could be used to escalate privileges or bypass resource-based policies that include account IDs as a condition.

**Disclaimer:
This tool is provided for educational and security research purposes only. Use only with explicit permission from the owners of the AWS resources.**

## Features

- Find an AWS Account ID from any S3 Bucket
- Assist in security assessments and research
- Supports AWS CLI profiles

## Prerequisites

- An AWS account

## Setup Instructions

### 1. Find the region for the S3 bucket
   1. `curl -I bucket-name.s3.amazonaws.com`
   2. Look for the **x-amz-bucket-region** header in the response
### 2. Login to your AWS Console
   1. Set the region to the same region as the S3 bucket in the dropdown at the top of the page
   2. Under **VPC > Your VPCs** click **Create a VPC**
      1. Select VPC only
      2. Click **Create VPC**
   3. Under Under **VPC > Subnets** click **Create subnet**
      1. For the **VPC ID** select the VPC you just created
      2. Click **Create subnet**
   4. Under **EC2 > Instances** click **Launch instances**
      1. Select Amazon Linux (Default settings including t2.micro are OK)
      2. Under **Key pair** select an existing key pair name or create a new key pair
      3. Under **Network settings** ensure the **Network** and **Subnet** are set to the VPC and subnet you created earlier
      4. Under **Firewall** select **Create security group**
      5. Check **Allow SSH traffic from** **Anywhere** and **Allow HTTPS traffic from the internet**
      6. Click **Launch instance**
      7. After the instance has been created select the instance and under **Instance state** select **Start instance**
   5. Under **VPC > Endpoints** click **Create endpoint**
      1. Select AWS services
      2. Under **Services** find and select the **com.amazonaws.<YOUR_REGION>.s3 amazon Interface** service
      3. Under **VPC** select your VPC
      4. Under **Additional settings**
         1. Check **Enable DNS name**
         2. Uncheck **Enable private DNS only for inbound endpoint**
      5. In **Subnets** check the box for the **Availability Zone** with your subnet in the dropdown
      6. In **Security groups** select the security group you created with your EC2 instance
      7. In the **Policy** select Custom and copy the **policy.py** from [here](https://raw.githubusercontent.com/marksowell/aws-account-finder/main/policy.json)
      8. Click **Create endpoint**
   6. Under **VPC > Elastic IPs** click **Allocate Elastic IP address**
      1. Click **Allocate**
      2. After the IP address is allocated select it and under **Actions** select **Associate Elastic IP address**
      3. Select Instance
      4. Under **Instance** choose your EC2 instance
      5. Under **Private IP address** choose the IP address in the dropdown
      6. Click **Associate**
   7. Under **IAM > Roles** click **Create role**
      1. Select AWS Service
      2. Under **Use Case** in **Service or use case** select EC2
      3. Click **Next**
      4. Under **Permissions policies** find and select **AdministratorAccess** and **AWSCloudTrail_FullAccess**
      5. Click **Next**
      6. Give your role the name **ec2-role**
      7. Click **Create role**
   8. Under **EC2 > Instances** select your instance
      1. Under **Actions > Security** select **Modify IAM role**
      2. In the **IAM role** dropdown select the role you just created **ec2-role**
      3. Click **Update IAM role**
   9. Under **IAM > Roles** click **Create role**
       1. Select AWS account
       2. Under **An AWS account** select **This account (YOUR_ACCOUNT_ID)**
       3. Click **Next**
       4. Under **Permissions policies** find and select **AdministratorAccess**
       5. Click **Next**
       6. Input a Role name and Description
       7. Click **Create role**
   10. Under **CloudTrail > Trails** click **Create trail**
       1. Input a Trail name
       2. Select **Create new s3 bucket**
       3. Under **Log file SSE-KMS encryption** uncheck **Enabled**
       4. Click **Next**
       5. Under **Events** check **Management events** and **Data events**
       6. Under **Data events > Data event > Data event type** in the **Select a source** dropdown select **S3**
       7. Click **Next**
       8. Click **Create trail**
### 3. Connect to your EC2 instance using SSH
   1. Install pip  
   `sudo yum install python3-pip -y`
   2. Install boto3  
   `pip3 install boto3`
   3. Install git  
   `sudo yum install git -y`
   4. Clone this Githib repository  
   `git clone https://github.com/marksowell/aws-account-finder.git`
   5. Navigate to the aws-account-finder project directory  
   `cd aws-account-finder`
   6. Configure AWS CLI ([Configuration and credential file settings](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html))  
   `vi ~/.aws/credentials`  
   Ensure the **aws_access_key_id**, **aws_secret_access_key**, and **aws_session_token** (if you are using temporary credentials) are set under [default] or a profile you will specify in the **aws-account-finder.py** script  
   `vi ~/.aws/config`  
   Ensure the **region = YOUR_REGION** and **output = json** are set under [default] or a profile you will specify in the **aws-account-finder.py** script
   7. Test to ensure AWS CLI is configured correctly  
   `aws sts get-caller-identity`  
   *Remember to use a profile if you set one with `--profile <PROFILE_NAME>`
   8. Ensure you can assume the AWS account role you created earlier  
   `aws sts assume-role --role-arn "arn:aws:iam::<YOUR_ACCOUNT_ID>:role/<YOUR_ROLE>" --role-session-name "test"`  
   *Remember to use a profile if you set one with `--profile <PROFILE_NAME>`
   9. The **aws_account_finder.py** script relies on 2 environment variables that can be set with the following 2 commands  
   `export AWS_REGION='<YOUR_REGION>'`  
   `export ROLE_ARN='arn:aws:iam::<YOUR_ACCOUNT_ID>:role/<YOUR_ROLE>'`
   Alternatively, they can be set in your **.bash_profile** using `vi ~/.bash_profile`, adding the 2 lines above, and applying the changes by logging out and back in or running the command `source ~/.bash_profile`
   10. Run the **aws_account_finder.py** script  
   `python aws_account_finder.py <profile> <bucket>`

### Usage example

```bash
python aws_account_finder.py default bucket-name
```
  
## Acknowledgements

- [How to find the AWS Account ID of any S3 Bucket](https://tracebit.com/blog/2024/02/finding-aws-account-id-of-any-s3-bucket/) by Sam Cox  
- [The Final Answer: AWS Account IDs Are Secrets](https://blog.plerion.com/aws-account-ids-are-secrets/) by Daniel Grzelak  
- [Finding the Account ID of any public S3 bucket](https://cloudar.be/awsblog/finding-the-account-id-of-any-public-s3-bucket/) by Ben Bridts
