# AWS Account Finder
Find the AWS Account ID of any S3 Bucket

1. Find the region for the S3 bucket  
    `curl -I bucket-name.s3.amazonaws.com`  
           Look for the `x-amz-bucket-region header` in the response.

3. Login to your AWS Console
   1. Set the region to the same region as the S3 bucket in the dropdown at the top of the page.
   2. Under `VPC > Your VPCs` click `Create a VPC`
      1. Select VPC only
      2. Click `Create VPC`
   3. Under Under `VPC > Subnets` click `Create subnet`
      1. For the `VPC ID` select the VPC you just created
      2. Click `Create subnet`
   4. Under `EC2 > Instances` click `Launch instances`
      1. Select Amazon Linux (Default settings including t2.micro are OK)
      2. Under `Key pair` select an existing key pair name or create a new key pair
      3. Under `Network settings` ensure the `Network` and `Subnet` are set to the VPC and subnet you created earlier
      4. Under `Firewall` select `Create security group` and check `Allow SSH traffic from` `Anywhere` and `Allow HTTPS traffic from the internet` are checked.
      5. Click `Launch instance`
      6. After the instance has been created select the instance and under `Instance state` select `Start instance`
   5. Under `VPC > Endpoints` click `Create endpoint`
      1. Select AWS services
      2. Under `Services` find and select the `com.amazonaws.us-west-1.s3 amazon Interface` service
      3. Under `VPC` select your VPC
      4. Under `Additional settings`
         1. Check `Enable DNS name`
         2. Uncheck `Enable private DNS only for inbound endpoint`
      5. In `Subnets` check the box for the `Availability Zone` with your subnet in the dropdown
      6. In Security groups select the security group you created with your EC2 instance
      7. In the Policy select Custom and copy the policy.py from the GitHub repository
      8. Click `Create endpoint`
   6. Under `VPC > Elastic IPs` click `Allocate Elastic IP address`
      1. Click `Allocate`
      2. After the IP address is allocated select it and under `Actions` select `Associate Elastic IP address`
      3. Select Instance
      4. Under `Instance` choose your EC2 instance
      5. Under `Private IP address` choose the IP address in the dropdown
      6. Click `Associate`
   7. Under `IAM > Roles` click `Create role`
      1. Select AWS Service
      2. Under `Use Case` in `Service or use case` select EC2
      3. Click `Next`
      4. Under `Permissions policies` find and select `AdministratorAccess` and `AWSCloudTrail_FullAccess`
      5. Click `Next`
      6. Give your role the name `ec2-role`
      7. Click `Create role`
   8. Under `EC2 > Instances` select your instance
      1. Under `Actions > Security` select `Modify IAM role`
      2. In the `IAM role` dropdown select the role you just created `ec2-role`
      3. Click `Update IAM role`
   9. Under `IAM > Roles` click `Create role`
       1. Select AWS account
       2. Under `An AWS account` select `This account (YOUR_ACCOUNT_NUMBER)`
       3. Click `Next`
       4. Under `Permissions policies` find and select `AdministratorAccess`
       5. Click `Next`
       6. Input a Role name and Description
       7. Click `Create role`
   10. Under `CloudTrail > Trails` click `Create trail`
       1. Input a Trail name
       2. Select `Create new s3 bucket`
       3. Under `Log file SSE-KMS encryption` uncheck `Enabled`
       4. Click `Next`
       5. Under `Events` check `Management events` and `Data events`
       6. Under `Data events > Data event > Data event type` in the `Select a source` dropdown select `S3`
       7. Click `Next`
       8. Click `Create trail`
4. Connect to EC2 instance using SSH
   1. Install pip `sudo yum install python3-pip -y`
   2. Install boto3 `pip3 install boto3`
   3. Install git `sudo yum install git -y`
   4. Clone this Githib repository `git clone https://github.com/marksowell/aws-account-finder.git`
   5. `cd aws-account-finder.git`
   6. Configure and aws cli
      1. `vi ~/.aws/credentials` set from your user creds
         1. Ensure the `aws_access_key_id`, `aws_secret_access_key`, and `aws_session_token` are set under [default] or a profile you will specify in the `aws-account-finder.py` script
         2. Test by using `aws sts get-caller-identity` Remember to use a profile if you set one
  
## Acknowledgements

- This project was inspired by
  - [How to find the AWS Account ID of any S3 Bucket](https://tracebit.com/blog/2024/02/finding-aws-account-id-of-any-s3-bucket/) by Sam Cox
  - [The Final Answer: AWS Account IDs Are Secrets](https://blog.plerion.com/aws-account-ids-are-secrets/) by Daniel Grzelak
  - [Finding the Account ID of any public S3 bucket](https://cloudar.be/awsblog/finding-the-account-id-of-any-public-s3-bucket/) by Ben Bridts
