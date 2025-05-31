# *Serverless Notification Engine (SNS + Lambda)*

A project for beginners to learn how to send notifications using Amazon Simple Notification Service (SNS) through Email, SMS, and automate those notifications using AWS Lambda.

## AWS Terminology
1. **Amazon SNS (Simple Notification Service):** Amazon SNS is a fully managed pub/sub messaging service used to decouple and fan-out messages to multiple subscribers via email, SMS, or Lambda for real-time alerts or notifications.
2. **SNS Topic:** A Topic in SNS is a communication channel to group and manage multiple subscribers, allowing a single message to be sent to all endpoints subscribed to it.
3. **SNS Subscription:** A Subscription is the endpoint (email, SMS, Lambda, etc.) where messages published to an SNS topic are delivered.
4. **Publish Message:** Publishing a message means sending a payload to the SNS topic which then distributes it to all subscribed endpoints.
5. **AWS Lambda:** AWS Lambda is a serverless compute service that runs backend code in response to triggers (like SNS events) without provisioning servers.
6. **IAM (Identity and Access Management):** IAM manages access to AWS services and resources securely using roles, users, and policies for granting necessary permissions.
7. **EventBridge (Optional):** Amazon EventBridge is a serverless event bus that connects application data from AWS services and triggers targets like Lambda or SNS based on defined rules.
8. **CloudWatch (Optional):** Amazon CloudWatch is a monitoring and observability service that can trigger alarms or actions like invoking Lambda functions or sending SNS alerts based on metrics or logs.



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

### 6.2 Search for IAM
1. Navigate for IAM Role in left side bar.
2. Search for name similar to `AutomateSNSwithLambda-role-hkt1m6nq`.
3. Attach the `AmazonSNSFullAccess` for the role.

### 6.3 Add Code to Publish SNS Message
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


## Step 8: Destroy
1. Go to Subscribed Email and first Unsubscribe from the Topic
2. Navigate to Topic and delete the Topic then in Topic delete the Subscription.

   
   ![image](https://github.com/user-attachments/assets/1bd70fdd-9d2a-4318-8029-0ab6301830b5)

3. Navigate to Topic Delete the Topic created `MyFirstNotificationTopic`.
4. Delete the Subscription.
5. Search for AWS Lambda.
6. Check on `AutomateSNSwithLambda` and in actions section click on delete.
7. Search for IAM, Navigate to IAM Roles.
8. Search for Role look like `AutomateSNSwithLambda-role-hkt1m6nq` created by AWS Lambda Function.
9. Click on checkbox and Delete the role.


## AWS SNS Pricing Table (Quick View - as of 2025)

| Feature                      | Free Tier                 | Pricing (Beyond Free Tier)                     |
| ---------------------------- | ------------------------- | ---------------------------------------------- |
| **Email notifications**      | Unlimited                 | Free                                           |
| **SMS - First 100 messages** | 100 SMS/month             | Varies by destination (e.g., \$0.00645/SMS US) |
| **Mobile Push (FCM/APNS)**   | 1 million requests/month  | \$0.50 per million requests                    |
| **HTTP/HTTPS delivery**      | 1 million publishes/month | \$0.50 per million publishes                   |
| **Data transfer (out)**      | First 1GB free            | \$0.09/GB up to 10TB/month                     |


SMS pricing depends on country. Check the [SNS SMS pricing page](https://aws.amazon.com/sns/sms-pricing/) for exact rates.

## AWS Lambda Pricing Table

| Pricing Component        | Free Tier                        | Paid Tier                               |
| ------------------------ | -------------------------------- | --------------------------------------- |
| **Requests**                 | 1 million requests/month         | \$0.20 per 1 million requests           |
| **Duration**                 | 400,000 GB-seconds/month         | \$0.00001667 per GB-second              |
| **Example Cost (low usage)** | Usually FREE for simple projects | Cost depends on usage duration & memory |
