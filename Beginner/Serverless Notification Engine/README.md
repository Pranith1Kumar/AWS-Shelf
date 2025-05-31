# *Serverless Notification Engine (SNS + Lambda)*

A project for beginners to learn how to send notifications using Amazon Simple Notification Service (SNS) through Email, SMS, and automate those notifications using AWS Lambda.

## Step 1: Login to AWS Console
1. Visit [https://aws.amazon.com](https://aws.amazon.com)
2. Click "Sign In to the Console using root account".
3. Enter your credentials (email & password).

## Step 2: Go to Amazon SNS Service
1. Once logged in, use the search bar at the top. 
2. Type SNS and click on Simple Notification Service.

   ![Search SNS](https://github.com/user-attachments/assets/4833f60b-e2db-491d-b892-5a4e9832c743)

## Step 3: Create a New SNS Topic
1. In the SNS Dashboard, click on "Topics" from the left menu.
2. Click the "Create topic" button.

   ![Create topic](https://github.com/user-attachments/assets/00a8795d-33cc-4976-95e2-af1f9f49894f)

3. Choose Standard as the topic type (default and recommended).
4. Enter a name for your topic: `MyFirstNotificationTopic`.
5. Leave other settings as default and click Create topic.

You’ll now see your topic listed.

![Topic created](https://github.com/user-attachments/assets/107c6a9e-b67b-4c10-a567-95e7d48899fb)

## Step 4: Create Subscriptions
### 4.1 For Email:
1. Click on your newly created topic `MyFirstNotificationTopic`.
2. Under the "Subscriptions" tab, click Create subscription.
3. Protocol: `Select Email`.

  ![Create subscription](https://github.com/user-attachments/assets/917d3571-4073-4a53-97c0-077b8f877abe)

4. Endpoint: Enter your email (e.g., `nnouser51@gmail.com`).
5. Click Create subscription.
6. Go to your email inbox and look for an AWS confirmation email.

   ![Sub confirmation](https://github.com/user-attachments/assets/fa8b979b-1ce5-4909-b740-afb30ecbf8de)


7. Click the confirmation link to activate the subscription.

  ![Confirmed](https://github.com/user-attachments/assets/a9a566b3-c5c7-4350-a253-4a77bb166986)

You’ll now see its Status: Confirmed in SNS console.

![Sub confirmation in console](https://github.com/user-attachments/assets/c36e6c6a-2d8e-4272-9c15-5e4d0c59f81b)

### 4.2 For SMS (optional if you want notification in SMS):
1. Click Create subscription again.
2. Protocol: `Select SMS`.
3. Endpoint: Enter your mobile number (e.g., `+919123456789`).
4. Click Create subscription.

No need to confirm SMS; it is activated immediately.

## Step 5: Publish a Test Notification
1. Go to your  `MyFirstNotificationTopic`.
2. Click Publish message.

  ![Publish](https://github.com/user-attachments/assets/61a9910d-d910-4c26-9982-b3ee5741b327)

3. Fill in the details:
4. Subject: `Dummy Notification`
5. Message body: `Hello! This is your manager our Company has declared that 2.5% hike for freshers and 1.5% hike for freshers.👍`

  ![Message body](https://github.com/user-attachments/assets/f05c058d-14a1-4d37-8e57-e52f7f2ce993)

6. Scroll down and click Publish message.

Check your email inbox or phone – you should receive the message.

![Notification from SNS](https://github.com/user-attachments/assets/08626c2c-a4fd-46a8-a1fb-081ff2b59cbe)

## Step 6: Automate Notification using AWS Lambda
If you want to send SNS messages automatically using code (e.g., triggered by an event):

### 6.1 Create a Lambda Function
1. Go to AWS Console Home > search and Lambda.
2. Click Create function.

   ![Create Function](https://github.com/user-attachments/assets/35d02894-e200-4470-8ebe-eb8770a56137)

3. Function name: `AutomateSNSwithLambda`
4. Runtime: `Python 3.13.3`
5. Permissions: Choose Create a new role with basic Lambda permissions.
6. Click Create function.

   ![Confg lambda](https://github.com/user-attachments/assets/e7942b17-b390-4f76-baf6-61f045109a47)

### 6.2 Add Code to Publish SNS Message
1. In the Lambda function code editor, paste this:

```python
import boto3

def lambda_handler(event, context):
    sns = boto3.client('sns')
    topic_arn = 'arn:aws:sns:us-east-1:123456789012:MyFirstNotificationTopic'  # Replace with your Topic ARN
    
    sns.publish(
        TopicArn=topic_arn,
        Message='Hello from Lambda!',
        Subject='Lambda Notification'
    )

    return {
        'statusCode': 200,
        'body': 'SNS message sent successfully!'
    }
```

Replace the `TopicArn` with the actual ARN of your SNS topic from the SNS Console.

2. Click Deploy to save the function.

  ![Code](https://github.com/user-attachments/assets/0ae8740b-11aa-4aba-86d1-44b9291195b5)

## Step 7: Test the Lambda Function
1. Click Test in the Lambda Console.
2. Create a new test event with default values.

  ![New test](https://github.com/user-attachments/assets/a9a5484e-3f61-4d4c-ad91-f1836ba79f8f)

3. Click Test to run the function.
4. Check your email/SMS again – you should receive the message.

  ![Notification successful](https://github.com/user-attachments/assets/e41c173a-dbfd-497f-aab2-9d7fdc0ff87a)

   
  ![Lambda SNS](https://github.com/user-attachments/assets/f9387708-0ce8-49e8-bd03-0639bd9932a3)


