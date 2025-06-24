# **Serverless File Backup System on AWS**

### This project implements an automated, serverless solution to back up files from one Amazon S3 bucket to another using AWS Lambda and CloudWatch Events/Event Bridge. It ensures secure, scalable, and cost-effective file backup with no server management.


![Archi](https://github.com/user-attachments/assets/17b8443b-b906-41a5-9600-8d18bdbd6caf)


## **Step 1: Create Two S3 Buckets**


- Go to the Amazon S3 Console.
- Choose region (Asia Pacific (Hyderabad)).

  ![Source-bucket](https://github.com/user-attachments/assets/1d079566-cd37-42e7-af6d-70f5a50f81d0)

- Click`Create bucket`.
- Enter a unique bucket name (e.g., my-file-backup-bucket (`bg-4`)).
- Choose the region and keep `Block all public access` enabled.
- Click `Create bucket`.
- Repeat above steps twice for backup bucket.

  ![Buckets](https://github.com/user-attachments/assets/319dc5bb-3d7b-4326-a052-502ca2b805f5)


`Source Bucket:` This is where your original files are stored. In my case it is `bg-4`.

`Backup Bucket:` This will store copies of the files for backup. In my case it is `bg-4-backup`.


## **Step 2: Upload Files to Source Bucket**


- Open source-file-bucket (bg-4).
- Click Upload > Add files > Choose local files (audio, media, project files).
- Click Upload.


## **Step 3: Create IAM Role for Lambda**


- Go to IAM choose Roles click on Create Role.

  ![IAM role](https://github.com/user-attachments/assets/d15606c2-31a5-44e0-af97-1fa00ad03598)
  
- Select Lambda as the trusted entity.
- Attach policies:
    - `AmazonS3FullAccess`
    - `CloudWatchLogsFullAccess`
 
  ![Per-IAM](https://github.com/user-attachments/assets/7001ddad-1872-4471-add7-60af15eab97c)

- Name the role: `LambdaS3BackupRole`.
- Click Create Role.


## **Step 4: Create Lambda Function**

- Go to AWS Lambda Console.
- Click Create function.
- Choose:
    - Author from scratch.
    - Function name: `S3FileBackup`.
    - Runtime: `Python 3.10+` to run boto function.
    - Permissions: Use existing role click on dropdown and select `LambdaS3BackupRole`.
- Click Create Function.

  ![Lambda Function](https://github.com/user-attachments/assets/c08162a6-2645-40fd-bca0-3829d9c51d0b)


## **Step 5: Add Python Backup Code to Lambda**


```python
import boto3
import datetime

SOURCE_BUCKET = 'bg-4'      # Replace with your source bucket name
DEST_BUCKET = 'bg-4-backup'        # Replace with your destination bucket name

s3 = boto3.client('s3')

def lambda_handler(event, context):
    date_prefix = datetime.datetime.now().strftime("%Y-%m-%d")

    response = s3.list_objects_v2(Bucket=SOURCE_BUCKET)

    if 'Contents' in response:
        for obj in response['Contents']:
            key = obj['Key']
            copy_source = {'Bucket': SOURCE_BUCKET, 'Key': key}
            dest_key = f"backup/{date_prefix}/{key}"
            s3.copy_object(CopySource=copy_source, Bucket=DEST_BUCKET, Key=dest_key)
            print(f"Copied: {key} → {dest_key}")
    else:
        print("No files to back up.")

```


- Click Deploy.


## **Step 6: Test Lambda Function**

- Click Test.
- Configure test event.
- Name it `TestBackup`.
- Click Create.
- Click Test

  ![deployTest](https://github.com/user-attachments/assets/79a09aa5-3d3b-42b8-bab0-56adece44dd7)

Go to backup-file-bucket (bg-4-backup) in S3 to verify files under backup/YYYY-MM-DD/ folder.

You can automate this daily as a scheduler using AWS Eventbridge Scheduler

![bg-4-backup](https://github.com/user-attachments/assets/ab162895-2cfe-4223-8028-a92112763602)

## **Step 7: Schedule Automated Backup with EventBridge**

1. Go to EventBridge.
- Navigate to Amazon EventBridge (under Services).
- On the left-hand menu, click `Scheduler`.

If you're using the older CloudWatch Events:
- Go to CloudWatch > Rules.
- Click `Create rule`.

2. Create a Rule/Schedule

- Click "Create schedule" (in EventBridge Scheduler).

3. Set the Schedule Pattern

- Choose `Recurring schedule`.

  ![Scheduler](https://github.com/user-attachments/assets/7c48a576-90c0-4b02-b91a-fe6930771651)
  
- Rate-based schedule:
- Select `Rate` and enter 1 day rate(1 day).

    OR

- Choose `Cron expression` and enter:
  - `cron(0 4 * * ? *)`
  (This runs every day at 2:00 AM UTC).

  ![Schedule type](https://github.com/user-attachments/assets/4061528f-c437-4bdf-a2c9-a323b08e6092)


4. Configure the Target

- Under `Target`, select `Lambda function`.
- In the Lambda function dropdown, choose: `S3FileBackup`.

  ![Target](https://github.com/user-attachments/assets/52deb76f-baac-42c3-b3fe-2f3325a4a3cd)

5. Configure Permissions

- Ensure the scheduler is allowed to invoke your Lambda function:
  - Check `Create a new role for this schedule` (or use an existing one with lambda:InvokeFunction permission).

6. Review and Create

- Give your schedule a name (e.g., DailyS3Backup).
- Review the configuration.
- Click `Create schedule`.

![Daily_scheduler](https://github.com/user-attachments/assets/fc76f25b-67ae-4c22-bb78-4f1577813719)

## **Step 8: Monitor Backups via CloudWatch Logs**

- Go to CloudWatch navigate to Logs check for Log Groups.
- Click /aws/lambda/S3FileBackup, created few minutes ago.
- Check logs for each execution (success/failure).

![logs](https://github.com/user-attachments/assets/ecc75095-c899-4264-85f5-e20edf7c8d49)



# **AWS Terminologies (Explained in One Sentence Each)**

**1. Amazon S3 (Simple Storage Service)**

<p> A scalable object storage service used to store and retrieve any amount of data at any time, which is used in this project to store automated file backups securely and reliably.</p>

**2. AWS Lambda**

<p> A serverless compute service that lets you run code without provisioning servers, used here to automatically execute backup scripts on a schedule.</p>

**3. Amazon EC2 (Elastic Compute Cloud)**

<p> A virtual server in the cloud that can run applications or scripts like the Python backup job, allowing on-demand computing power.</p>

**4. AWS CloudWatch**

<p> A monitoring and observability service that collects logs, metrics, and events, and is used here to schedule backups and track the automation logs.</p>

**5. IAM (Identity and Access Management)**

<p> A security service that helps you manage users, roles, and their access permissions, ensuring that only authorized entities can access S3 and other AWS services.</p>

**6. CloudWatch Events (EventBridge)**

<p> A scheduler and event bus service that triggers actions (e.g., Lambda execution or EC2 cron monitoring) based on defined time intervals or event patterns.</p>


## Quick Pricing Overview (as of 2025)

| AWS Service    | Free Tier                              | Approximate Paid Cost                                              |
| -------------- | -------------------------------------- | ------------------------------------------------------------------ |
| **Amazon S3**  | 5 GB Standard storage/month            | \~\$0.023/GB/month (Standard), \~\$0.0125/GB for infrequent access |
| **AWS Lambda** | 1M requests + 400,000 GB-seconds/month | \$0.20 per 1M requests + \$0.00001667 per GB-second                |
| **Amazon EC2** | 750 hours/month (t2.micro/t3.micro)    | From \~\$0.0116/hr for t3.micro (US East)                          |
| **CloudWatch** | 5GB log data ingestion/month           | \~\$0.50/GB ingested + \$0.03/GB archived/month                    |
| **IAM**        | Always Free                            | Free (part of account management)                                  |


# ** NOTE 1:** Tip: This project stays mostly within the free tier limits if you’re backing up small files or using small EC2 instances.
# ** NOTE 2:** Make sure to stop all services and terminate any running resources used in the project.
**7. CloudWatch Logs**

<p> A logging service that captures log data from EC2 or Lambda, used here for debugging and verifying backup execution.</p>
