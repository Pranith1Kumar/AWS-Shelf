# **LEVEL: INTERMEDIATE**

# *Intelligent Document Classification and Routing System Using AWS*                                                              

## Prerequisites
- AWS Account (Free Tier is sufficient)
  - [Sign up here](https://signin.aws.amazon.com/signup?request_type=register)
- Basic familiarity with AWS Console UI
- Use us-east-2 as your region (or you can use based on your preferences)

![Smart Document Classification and Routing System with AWS drawio](https://github.com/user-attachments/assets/eafda48e-0e4b-47b7-8a6c-b73fcf14e11f)

## Project Overview
This project is an automated serverless pipeline built using AWS services that intelligently processes and classifies incoming documents. When a document (e.g., PDF, Word) is uploaded to an S3 bucket, it automatically:

- Accepts documents (PDF/DOCX) via S3
- Uses Amazon Textract to extract text
- Classifies documents (Invoice, Resume, Contract) using keyword matching
- Moves documents to appropriate S3 buckets
- Sends email notifications using Amazon SNS
Perfect for automating HR document processing, financial records, or contracts.

## Architecture
![Project-flow](https://github.com/user-attachments/assets/1b4e2f4e-87c8-4d56-a37a-54e208beb116)

### Step 1: Create S3 Buckets
These will be used to upload documents and route them after classification.
Action:
- Go to AWS Console → S3 → Click Create bucket
Create these 4 buckets: (Bucket name should be in lowercase)
- incoming-docs-bucket
- classified-bucket-invoices
- classified-bucket-resumes
- classified-bucket-contracts

![Incoming-bucket](https://github.com/user-attachments/assets/cc9c1e02-e0f3-429b-8777-ed43e01d63c5)

- Continue with other three buckets don't uncheck the Block all public access beacause we are using it private

Bucket Settings:
Leave all settings default
DO NOT enable public access
Enable versioning for backup tracking
Repeat this 4 times for each bucket.

![4-Buckets](https://github.com/user-attachments/assets/42cc0c78-1ea1-444e-b8ad-29ac4c7f12d3)

### Step 2: Create an IAM Role for Lambda
This role allows your Lambda function to access S3, Textract, SNS, and logs.
Action:
- Go to AWS Console → IAM → Roles → Click Create role
- Choose Trusted Entity: AWS Service
- Choose Use Case: Lambda → Click Next

![IAM Role](https://github.com/user-attachments/assets/298e88d4-38c1-4ed5-9915-eeeb10106c5d)

Attach the following policies:
Search and select each of these:

- AmazonS3FullAccess
- AmazonTextractFullAccess
- ComprehendFullAccess
- AmazonSNSFullAccess
- CloudWatchLogsFullAccess
Click Next → Name the role: `LambdaDocumentProcessorRole `
Click Create Role

![Role Policies](https://github.com/user-attachments/assets/76b81944-e930-4dc2-b6df-b850b4d5686b)


### Step 3: Create SNS Topic (for Email Alerts)
Action:
1. Go to Amazon SNS → Topics → Click Create topic
2. Choose:
  - Type: Standard
  - Name: DocumentNotifications
3. Click Create Topic

![SNS-Topic](https://github.com/user-attachments/assets/3a83e670-f71c-4722-8860-1282821ad2c3)

Create Subscription:
1. Go to the topic → Click Create subscription
2. Choose:
  - Protocol: Email
  - Endpoint: Your email (e.g., you@example.com)
3. Go to your inbox and click Confirm subscription

![Sub-Conf](https://github.com/user-attachments/assets/79cb4e5b-07df-48ee-b5db-e155b7ddfdf5)

### Step 4: Create the Lambda Function
Action:
- Go to AWS Lambda → Create Function
- Choose:
- Name: DocumentClassifier
- Runtime: Python 3.10
- Execution Role: Use existing role → Select ```LambdaDocumentProcessorRole```
- Click Create Function

### Step 5: Add Classification Code to Lambda

Scroll to Function Code section
Replace everything in the code editor with this:

```python
import json, boto3
import urllib.parse

s3 = boto3.client('s3')
textract = boto3.client('textract')
sns = boto3.client('sns')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    # Extract text from document using Textract
    response = textract.detect_document_text(
        Document={'S3Object': {'Bucket': bucket, 'Name': key}}
    )
    
    lines = [item['Text'] for item in response['Blocks'] if item['BlockType'] == 'LINE']
    extracted_text = " ".join(lines).lower()

    # Simple classification logic
    if "invoice" in extracted_text:
        doc_type = "Invoice"
        target_bucket = "classified-bucket-invoices"
    elif "resume" in extracted_text or "curriculum" in extracted_text:
        doc_type = "Resume"
        target_bucket = "classified-bucket-resumes"
    elif "contract" in extracted_text or "agreement" in extracted_text:
        doc_type = "Contract"
        target_bucket = "classified-bucket-contracts"
    else:
        doc_type = "Unknown"
        target_bucket = "classified-bucket-contracts"  # fallback

    # Move file to the classified bucket
    s3.copy_object(
        CopySource={'Bucket': bucket, 'Key': key},
        Bucket=target_bucket,
        Key=key
    )
    s3.delete_object(Bucket=bucket, Key=key)

    # Send notification
    sns.publish(
        TopicArn='arn:aws:sns:us-east-2:YOUR_ACCOUNT_ID:DocumentNotifications',
        Message=f"Document '{key}' classified as {doc_type} and moved to {target_bucket}.",
        Subject="New Document Routed"
    )

    return {'statusCode': 200, 'body': json.dumps('Success')}

```

- Replace YOUR_ACCOUNT_ID with your actual AWS account ID (find it in top-right corner of AWS console).
- Replace Topic Arn=`arn:aws:sns:us-east-2:YOUR_ACCOUNT_ID:DocumentNotifications`, copy and paste your Arn from SNS ( Check your Region ed; us-east-2).
- Click Deploy to save. (If you update any code you should deploy again).

### Step 6: Add Trigger for S3 Upload
This tells AWS to run the Lambda function when a file is uploaded.

Action:
1. Go to S3 → incoming-docs-bucket
2. Click Properties → Scroll down to Event notifications
3. Click Create event notification
  - Name: TriggerLambda
  - Event type: PUT
4. Prefix/Suffix: Leave empty
5. Destination: Lambda function
6. Select DocumentClassifier
7. Save.

![S3-Event](https://github.com/user-attachments/assets/252caafc-ac2d-4559-8654-1a3142a86aee)

## Testing 
1. Upload a Sample File:
2. Go to S3 → incoming-docs-bucket → Click Upload
3. Use one of these sample texts in a .txt, .pdf, or .docx:

![Contract](https://github.com/user-attachments/assets/78c1fc8d-f7d0-4ea5-a7b8-c6dbc24c805f)

4. ```“This is an invoice for $5000.”``` → Should go to classified-invoices-bucket
5. ```“My name is John Doe. Attached is my resume.”``` → Should go to classified-resumes-bucket
6. ```“This contract is signed on March 15.”``` → Should go to classified-contracts-bucket
7. Here I have uploaded Invoices.pdf so my document is moved to classified-bucket-invoices.

Check the Output:
- Go to the correct target bucket – your file should now be there

![Contract in Conbuc](https://github.com/user-attachments/assets/77968352-2145-4065-9451-6fa5381bb53b)

- Check your email inbox – you'll get a message like:
- "Document 'invoice.pdf' classified as Invoice and moved to classified-bucket-invoices."

- SNS Alert for Invoice
  
![Invoice-SNS](https://github.com/user-attachments/assets/9bd90ffd-2c88-4efd-ace3-11d4662f707f)

- SNS Alert for Contract
  
![Contract-SNS](https://github.com/user-attachments/assets/695a13eb-d550-40b7-b435-99e278e6a114)

- SNS Alert for Resume
  
![Resume-SNS](https://github.com/user-attachments/assets/523f5407-98b0-4dba-9adc-5c9a1fee9b10)


View Logs:
- Go to CloudWatch → Logs → Lambda → Select your function.
- View logs for detailed success/failure messages.

🎯 What You Achieved
- Built an automated document classification system.
- Used AWS S3, Lambda, Textract, SNS together.
- Learned how to classify text using Python.
- Learned how to route and manage files using AWS.
- Got real-time email alerts when files were processed.
