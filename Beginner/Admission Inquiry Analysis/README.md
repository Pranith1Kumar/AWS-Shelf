# *Admission Inquiry Analysis*



### Proejct Workflow
![Project Workflow](https://github.com/user-attachments/assets/70e9877a-5849-492b-8ccf-01e434f10cd6)




# Step 1: Data Preparation

1. Identify Tools for Data Visualization.
- Choose Visualization Tool: Use Amazon QuickSight (free-tier eligible).
- Define Key Attributes: Identify key metrics to visualize, such as admission trends, B.Tech score distributions, and interest areas. (My dataset link is attached below)
- [Dataset Link](https://www.kaggle.com/datasets/praneethkumar007/b-tech-students-interest-on-technologies)

If you want to create your dataset on your own below you can refer and start building your schema for the analysis.

Define the Dataset Schema
- Create Dataset: Structure a dataset for at least 8000 B.Tech students with the following attributes:
- Student_ID: Unique identifier
- Name: Full Name
- Department: B.Tech Specialization (CSE, ECE, ME, CE, etc.)
- CGPA: Absolute integer between 6 and 10
- Contact_Number: Random 10-digit number
- College_Email: Generated in the format: name@college.edu
- BTech_Score: Between 50 and 300
- Interest_Area: Courses like AI, ML, Cybersecurity, etc.

Action: Create a CSV file named admission_enquiries.csv with the above attributes filled with synthetic data.

# Step 2: AWS S3 Bucket Setup

1. Create an S3 Bucket
- Log in to AWS Management Console.
- Navigate to S3 and create a new bucket (e.g., `admission-enquiries-data`).

2. Upload the Dataset
- Upload the admission_enquiries.csv file to the created S3 bucket.

![Bucket Uploaded successfully](https://github.com/user-attachments/assets/dad3d232-4592-4280-bf33-511a96478cba)




# Step 3: AWS Glue Setup

1. Create an AWS Glue Crawler
- Navigate to AWS Glue and create a new crawler.
- Set the data store to S3 and specify the bucket path.

![Crawler](https://github.com/user-attachments/assets/645f0168-820d-4f10-9afd-6e46100bcd7e)


1.1 Create an AWS Glue Database
- Navigate to AWS Glue → Click Databases under the Data Catalog.
- Click Add database → Enter a name (e.g., admission_db) → Click Create.

![Glue Database](https://github.com/user-attachments/assets/c5075ed0-df66-4c81-9755-a23b3df0df8a)



2. Create an AWS Glue Crawler

- In AWS Glue, go to Crawlers → Click Add Crawler.
- Name the crawler: admission_crawler.
- Choose Data Source: Select S3 and enter the S3 bucket path:

```
s3://admission-enquiries-data/
```

- Click Next → Select Create IAM Role → Name it AWSGlueServiceRole-admission.
- Choose Output Database: Select admission_db (created in Step 2).
- Set Schedule: Choose Run on Demand.
- Click Finish.

3. Run the Crawler & Verify Metadata
- In AWS Glue → Crawlers, select admission_crawler.
- Click Run Crawler.
Once completed, go to Tables under the Data Catalog.
- Verify that admission_enquiries_btech table is created with schema details.

![Table Schema](https://github.com/user-attachments/assets/ac63d423-a58b-474a-8683-f4f326e1b9e7)


In above image the error occurred is table is already created in my Data Catalog.


# Step 4: AWS Redshift Cluster Setup


1. Create an Amazon Redshift Cluster
- Go to Amazon Redshift and create a new cluster (DC2.large, free-tier eligible).

2. Create a Database and Tables
- Use the Redshift console to create a database.
- Define the table structure to store student inquiries.

3. Load Data from S3 to Redshift
- Use the following SQL command to load data from S3:

1. Search for Amazon Redshift → Click Clusters.
- Click Create Cluster.
- Configure the cluster:
- Cluster name: admission-cluster
- Node type: `dc2.large` (Free-tier eligible)
- Number of nodes: 1 (Single-node cluster for free-tier)
- Database name: `admission_db`
- Master username: `admin`
- Master password: `Invincibel23`
- Click Create Cluster and wait for the cluster to be provisioned (this may take a few minutes).

2. Configure IAM Role for Redshift to Access S3

- Go to AWS IAM Console → Click Roles → Create role.
- Select AWS Service → Choose Redshift → Click Next.

Attach policies:
- AmazonS3ReadOnlyAccess (Allows Redshift to read S3 data)
- AWSGlueConsoleFullAccess (Allows Redshift to access Glue Data Catalog)
- Name the role: RedshiftGlueS3Role → Click Create Role.
- Copy the IAM Role ARN (needed for loading data).

3. Connect Redshift to AWS Glue Data Catalog
- In the Redshift Console, go to Clusters → Select your cluster (admission-cluster).
- Click Query Editor v2 → Click Manage Settings.
- Under Data Catalog, choose AWS Glue Data Catalog.
- Select admission_db as the database → Click Save Changes.

4. Load Data from S3 into Redshift Using COPY Command

- Create a Table in Redshift
- Open Redshift Query Editor v2.
- Connect to the database admission_db.
- Run the following SQL to create a table:

```sql
CREATE TABLE admission_enquiries (
    Name VARCHAR(100),
    Department VARCHAR(50),
    CGPA INT,
    Contact_Number VARCHAR(15),
    College_Email VARCHAR(100),
    BTech_Score INT,
    Interest_Area VARCHAR(50)
);
```


![Table Creation](https://github.com/user-attachments/assets/b4a73628-c7e6-40dd-93cf-85f73f5984c6)


5. Load Data from S3 into Redshift
- Run the following COPY command (replace <your-bucket> and <your-role-arn>):

```sql
COPY admission_enquiries
FROM 's3://admission-enquiries-data/admission_enquiries.csv'
IAM_ROLE 'arn:aws:iam::<your-account-id>:role/RedshiftRole'
FORMAT AS CSV IGNOREHEADER 1;
```

![AWS RQ2](https://github.com/user-attachments/assets/43e3bc30-2fc1-4e3f-862b-df1e58b02a84)


Run the following query to verify the data

```sql
SELECT * FROM admission_enquiries WHERE interest_area = 'AI' AND BTech_score > 95;
```

![Verify](https://github.com/user-attachments/assets/db0530cb-4d27-4d16-869f-f2b2113ebddd)


# Step 5: Perform Analysis in Redshift
- SQL Queries for Insights
- Students who enquired for B.Tech admission

```sql
SELECT * FROM admission_enquiries WHERE department IS NOT NULL;
```

Students interested in B.Tech Computer Science

```sql
SELECT * FROM admission_enquiries WHERE department = 'CSE';
```

Students with BTech_Score above 100

```sql
SELECT * FROM admission_enquiries WHERE BTech_score > 100;
```

Students interested in Civil Engineering

```sql
SELECT * FROM admission_enquiries WHERE department = 'CE';
```

Students with interest in AI & BTech_Score > 100:
sql

```sql
SELECT * FROM admission_enquiries WHERE interest_area = 'AI' AND BTech_score > 100;
```

# Step 6: Create Visualizations in Amazon QuickSight

1. Sign Up for Amazon QuickSight

- Go to AWS Console → Search for Amazon QuickSight.
- Click Sign up for QuickSight (if not already signed up).
- Choose Standard Edition (free-tier available).
- Select Amazon S3, Athena, and Redshift as data sources.
- Click Finish and wait for QuickSight to be enabled.

2. Connect QuickSight to Redshift

- Grant QuickSight Access to Redshift
- Go to AWS IAM Console → Click Roles.
- Find the QuickSight service role (starts with aws-quicksight-service-role).
- Attach the policy AmazonRedshiftFullAccess to allow QuickSight to query Redshift.

3. Add Redshift as a Data Source in QuickSight

- Open Amazon QuickSight → Click Datasets.
- Click New Dataset → Select Redshift.
- Enter Redshift cluster details:
- Cluster Name: `admission-cluster`
- Database: `admission_db`
- Username: `admin`
- Password: `Invisibke123`
- Click Validate Connection → If successful, click Create Data Source.
- Choose the admission_enquiries table → Click Select.

4. Create Dashboards in QuickSight

- Prepare the Data
- After selecting the dataset, click Edit/Preview Data.
- Click Save & Visualize.

5. Build Charts & Insights

Use Below types of charts to Visualize.
- Admission Trends → Use a bar chart (Department vs. Count of Students).
- B.Tech Score Analysis → Use a histogram (B.Tech Score distribution).
- Interest Analysis → Use a pie chart (Interest Area count).

![Bar Plot](https://github.com/user-attachments/assets/0089a525-dbbf-4374-9f2b-0427d31edb8c)


![Stacked Bar Chart](https://github.com/user-attachments/assets/0f88d88c-5d9a-4dd4-bb59-54163e8c58c9)

### Destroy
1. Delete Tables in Data Catalog in Glue.
2. Delete AWS Glue Crawler.
3. Delete AWS Glue Database.
4. Delete AWS Redshift Cluster.
5. Delete data from AWS QuickSight and delete all the visual charts.

If you want to push to your GitHub account follow below commands.

```bash
git init
git add .
git commit -m "Initial commit of Admission Enquiries Analysis project"
git remote add origin <repository-url>
git push -u origin main
```
