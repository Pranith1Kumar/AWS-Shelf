# Project: Create an AWS Application Load Balancer (ALB) for a Highly Available Web Application
## Project Objective

The purpose of this project is to create a web application that can be highly available through the use of an Application Load Balancer (ALB) on Amazon Web Services (AWS). The application will be hosted on two identical EC2 instances, and will receive an incoming HTTP request from the ALB. In the event of an EC2 instance becoming unhealthy or no longer responding to requests, the ALB will automatically redirect incoming traffic from the unhealthy instance to the other healthy EC2 instance, allowing for continuous access. Health checks will be performed, a custom maintenance display page will be created, access logging will be enabled, and metrics will be collected through Amazon CloudWatch.

                     Internet
                         │
                         ▼
             Application Load Balancer
                  (HTTP Port 80)
                         │
        ┌────────────────┴────────────────┐
        │                                 │
        ▼                                 ▼
    EC2 Instance 1                    EC2 Instance 2
    Apache Web Server                 Apache Web Server
    index.html                         index.html
    health.html                        health.html
        │                                 │
        └──────────────┬──────────────────┘
                       ▼
                 Target Group
               Health Checks
                       │
                CloudWatch Metrics
                       │
                 S3 Access Logs
                 
                 
## Step 1: Understand the Project Architecture

Before creating AWS resources, it's important to understand how they connect.

How the Architecture Works:
1. A user enters the ALB DNS name in a web browser.
2. The request reaches the Application Load Balancer.
3. The ALB checks which EC2 instances are healthy.
4. It forwards the request to one healthy server.
5. If one server fails, traffic is automatically redirected to the other server.
6. Every request is logged to Amazon S3.
7. CloudWatch collects performance metrics.


![ALB Architecture](https://github.com/Pranith1Kumar/AWS-Shelf/blob/96b0076705f68edfa8f0b8861f7758689184fe0c/Beginner/AWS%20Top%2010%20Core%20Services%20Projects/Create%20an%20Application%20Load%20Balancer/Assets/ALB%20Architecture.png)



## Step 2: AWS Services Used

| AWS Service               | Purpose                                 |
| ------------------------- | --------------------------------------- |
| VPC                       | Creates a private network for resources |
| Public Subnets            | Place EC2 instances and ALB             |
| Internet Gateway          | Provides Internet connectivity          |
| Route Table               | Directs traffic to the Internet         |
| Security Groups           | Acts as a firewall                      |
| EC2                       | Hosts the web application               |
| Target Group              | Groups EC2 instances for the ALB        |
| Application Load Balancer | Distributes traffic                     |
| S3                        | Stores ALB access logs                  |
| CloudWatch                | Monitors ALB and EC2                    |


## Step 3: Prerequisites

Before starting, ensure you have the following:

#### AWS Account

Create a free AWS account if you don't already have one.

#### Basic Knowledge

You should know:

- What is a web server?
- What is an IP address?
- Basic Linux commands
- Basic AWS navigation

No advanced AWS knowledge is required.

#### Required Software

Windows

- Google Chrome or Microsoft Edge
- PuTTY or MobaXterm or powershell
  
Linux/macOS
- Terminal
- SSH client

## Step 4: Region Selection

- Sign in to the AWS Management Console.
- Select a region where all resources will be created.

For example:

`Asia Pacific (Mumbai)
ap-south-1
`

- Using the same region for all services avoids connectivity issues and additional costs.

## Step 5: Naming Convention

For easy understanding copy paste the name in the relevant step, or you can use your own naming convention.

To keep resources organized, use consistent names.

| Resource           | Name                     |
| ------------------ | ------------------------ |
| VPC                | ALB-Project-VPC          |
| Internet Gateway   | ALB-IGW                  |
| Public Subnet 1    | Public-Subnet-A          |
| Public Subnet 2    | Public-Subnet-B          |
| Route Table        | Public-RT                |
| EC2 Instance 1     | WebServer-1              |
| EC2 Instance 2     | WebServer-2              |
| Security Group     | WebServer-SG             |
| ALB Security Group | ALB-SG                   |
| Target Group       | Web-TG                   |
| Load Balancer      | Web-ALB                  |
| S3 Bucket          | alb-access-logs-yourname |



## Step 6: Create a Custom VPC

An Amazon VPC (Virtual Private Cloud) is a secure, logically isolated virtual network that you control within the AWS cloud. It allows you to run your cloud resources, like virtual servers and databases, in a custom network environment where you define the IP address ranges, subnets, route tables, and network gateways. Essentially, it acts as your own private data center inside AWS, giving you total control over how your applications connect to each other and the public internet.

In simple: A Virtual Private Cloud (VPC) is a logically isolated virtual network in AWS where you'll deploy all project resources.

#### **Why Create a Custom VPC?**

Creating a custom VPC gives you full control over networking, IP address ranges, subnets, and routing. It also reflects real-world AWS environments where organizations do not rely on the default VPC.

Create the VPC
1. Sign in to the AWS Management Console.
2. In the search bar, type VPC and open the VPC service.
3. In the left navigation pane, click Your VPCs.
4. Click Create VPC.
5. Choose VPC only.

Fill in the details:

- **Name tag:** ALB-Project-VPC
- **IPv4 CIDR block:** 10.0.0.0/16
- **IPv6 CIDR:** No IPv6 CIDR Block
- **Tenancy:** Default
- Click Create VPC.

**Explanation:** The 10.0.0.0/16 block allocates 65,536 private IPs. This capacity handles current project needs and future growth. Selecting default tenancy keeps infrastructure costs down by utilizing shared AWS host servers.

**Expected Outcome:** Your active AWS resource list will display a new VPC. It is named ALB-Project-VPC. It uses the 10.0.0.0/16 network range.

Check below image for configurations.

![Create VPC](https://github.com/Pranith1Kumar/AWS-Shelf/blob/96b0076705f68edfa8f0b8861f7758689184fe0c/Beginner/AWS%20Top%2010%20Core%20Services%20Projects/Create%20an%20Application%20Load%20Balancer/Assets/Create%20VPC.png)


## Step 7: Create Two Public Subnets

An AWS subnet is a smaller, logical segment of a Virtual Private Cloud (VPC) that groups your resources based on security and networking needs using a specific range of IP addresses (CIDR block). Each subnet must reside entirely within a single physical Availability Zone and is categorized as either public, which routes directly to the internet via an Internet Gateway, or private, which isolates backend systems like databases from external access. Network traffic flowing into and out of these subnets is controlled and secured through associated route tables and Network Access Control Lists (NACLs).

In simple terms: Subnets divide the VPC into smaller networks. We'll create two public subnets in different Availability Zones to achieve high availability.

Create Public Subnet A
1. In the VPC console, click Subnets.
2. Click Create subnet.
3. Select the VPC ALB-Project-VPC.

4. Enter the following:

- **Subnet name:** Public-Subnet-
- **Availability Zone:** ap-south-1
- **IPv4 CIDR block:** 10.0.1.0/24

5. Click Create subnet.
6. Create Public Subnet B

![Subnet1](https://github.com/Pranith1Kumar/AWS-Shelf/blob/96b0076705f68edfa8f0b8861f7758689184fe0c/Beginner/AWS%20Top%2010%20Core%20Services%20Projects/Create%20an%20Application%20Load%20Balancer/Assets/Create%20Sub1.png)

Config Subnet 1

![Congig Subnet1](https://github.com/Pranith1Kumar/AWS-Shelf/blob/96b0076705f68edfa8f0b8861f7758689184fe0c/Beginner/AWS%20Top%2010%20Core%20Services%20Projects/Create%20an%20Application%20Load%20Balancer/Assets/Config%20Sub1.png)

7. Repeat the process with:
   - **Subnet name:** Public-Subnet-B
   - **Availability Zone:** ap-south-1b
   - **IPv4 CIDR block:** 10.0.2.0/24
8. Click Create subnet.

![Subnet2](https://github.com/Pranith1Kumar/AWS-Shelf/blob/96b0076705f68edfa8f0b8861f7758689184fe0c/Beginner/AWS%20Top%2010%20Core%20Services%20Projects/Create%20an%20Application%20Load%20Balancer/Assets/Create%20Sub2.png)

**Explanation**

Each /24 subnet yields 256 IP addresses, with 251 available for your resources after AWS reserves five. Distributing these subnets across multiple Availability Zones ensures high availability and shields your infrastructure from localized zone failures.

## Step 8: Verify Resources

At this stage, your network should contain:

- **VPC:** Create
- **Public Subnet A:** Create
- **Public Subnet B:** Created

## Step 9: Create an Internet Gateway (IGW)

An Internet Gateway (IGW) in AWS is a highly available, horizontally scaled VPC component that acts as a redundant, bidirectional bridge between your cloud network and the public internet. It allows resources in your public subnets, like EC2 instances with public IP addresses, to connect out to the web while simultaneously permitting external users to initiate connections into those resources. To make it operational, you must attach the gateway to your VPC and update your subnet’s route table to direct all internet-bound traffic (destination 0.0.0.0/0) straight to the IGW.

In simple terms:
An Internet Gateway (IGW) is an AWS-managed component that allows resources inside a VPC to communicate with the Internet.

- Without an Internet Gateway:
- EC2 instances cannot access the Internet.
- Users cannot access your website.
- The Application Load Balancer cannot receive traffic from the Internet.
- Package installation (yum, apt, etc.) will fail because the instances cannot reach external repositories.

Think of the Internet Gateway as the main entrance and exit of your AWS network.

### **Why Do We Need an Internet Gateway?**

An Internet Gateway is required for a VPC to communicate with the public internet, acting as an edge router that allows external traffic to enter the private network. It enables network address translation for outbound traffic and enables the VPC route table to direct internet-bound data outside the boundary. You can explore the AWS documentation to learn more about VPC internet gateways.

Suppose a user opens your website:

`https://your-website.com`

The request follows this path:

```
    Internet
        ↓
Internet Gateway
        ↓
    Route Table
        ↓
  Public Subnet
        ↓
Application Load Balancer
        ↓
  EC2 Instance
```

Without the Internet Gateway, the request stops at the VPC boundary.

![WorkFlow IGW](https://github.com/Pranith1Kumar/AWS-Shelf/blob/96b0076705f68edfa8f0b8861f7758689184fe0c/Beginner/AWS%20Top%2010%20Core%20Services%20Projects/Create%20an%20Application%20Load%20Balancer/Assets/IGW%20Work%20Flow.png)

### Create the Internet Gateway

1. Open the AWS Management Console.
   - Search for VPC.
   - Click VPC Dashboard.

2. In the left navigation pane, click
   - Internet Gateways

3. Click
   - Create Internet Gateway
4. Provide the following details.
   
   **Name Tag:** ALB-IGW
  Click
  - Create Internet Gateway

5. Expected Output

  - You should now see
    `
    ALB-IGW
    State: Detached`
    
This is expected because it has not yet been attached to the VPC.

![Create IGW](https://github.com/Pranith1Kumar/AWS-Shelf/blob/c840bb1747ec0bd7ca41cc787b4ac3867196b81d/Beginner/AWS%20Top%2010%20Core%20Services%20Projects/Create%20an%20Application%20Load%20Balancer/Assets/Create%20IGW.png)


## Step 10: Attach the Internet Gateway to the VPC

An Internet Gateway must be attached to a VPC before it can be used.

1. Select: ALB-IGW
2. Click Actions --> Actions --> Attach to VPC
3. Select: ALB-Project-VPC (In my case it is ALB for Top 10)
4. Click: Attach Internet Gateway

Expected Result: ALB-IGW State should be Attached

Congratulations! Your VPC is now connected to the Internet.

![Attach IGW to VPC](https://github.com/Pranith1Kumar/AWS-Shelf/blob/c840bb1747ec0bd7ca41cc787b4ac3867196b81d/Beginner/AWS%20Top%2010%20Core%20Services%20Projects/Create%20an%20Application%20Load%20Balancer/Assets/Attach%20IGW%20to%20VPC.png)

## Step 11: Create a Route Table

Your Virtual Private Cloud (VPC) will have a Route Table to act as a set of instructions (routes) based on GPS coordinates of where the network traffic should travel as a request was made from that subnet or gateway. For example, the route table will determine if your network traffic is staying on the network, going to the Internet, or reaching your physical location.

In simple terms: A Route Table tells AWS where network traffic should go.

Think of it as Google Maps for your network.

Example:



```
Destination

10.0.0.0/16

↓

Stay inside VPC

0.0.0.0/0

↓

Go to Internet
```

#### **Why Do We Need a Route Table?**

- Suppose an EC2 instance wants to install Apache.
- It sends a request to: `archive.ubuntu.com`
  
How does AWS know where to send this network traffic?
- The answer is the Route Table.Without a route table, AWS cannot direct your traffic, and your EC2 instance will have no way to reach the Internet.

![RT Workflow](https://github.com/Pranith1Kumar/AWS-Shelf/blob/96b0076705f68edfa8f0b8861f7758689184fe0c/Beginner/AWS%20Top%2010%20Core%20Services%20Projects/Create%20an%20Application%20Load%20Balancer/Assets/RT%20Work%20Flow.png)

#### Create Route Table
- Go to: VPC Dashboard --> Route Tables --> Create Route Table

Provide these details

- **Name:** Public-RT
- **VPC:** ALB-Project-VPC

Click: Create Route Table
- Expected Output: `Public-RT`

![Route Table](https://github.com/Pranith1Kumar/AWS-Shelf/blob/96b0076705f68edfa8f0b8861f7758689184fe0c/Beginner/AWS%20Top%2010%20Core%20Services%20Projects/Create%20an%20Application%20Load%20Balancer/Assets/Create%20RT.png)

## Step 12: Configure Internet Route

Currently, the Route Table only contains

**Destination:** 10.0.0.0/16

**Target:** local

This means: Traffic stays inside the VPC only.

Now we must add Internet access.

1. Open: `Public-RT`.
2. Select the `Routes` tab.
3. Click `Edit Routes`
4. Click `Add Route`
5. Fill:
   - **Destination:** 0.0.0.0/0
   - **Target:** Internet Gateway
6. Choose: `ALB-IGW`
7. Click `Save Changes`

![Edit Route](https://github.com/Pranith1Kumar/AWS-Shelf/blob/96b0076705f68edfa8f0b8861f7758689184fe0c/Beginner/AWS%20Top%2010%20Core%20Services%20Projects/Create%20an%20Application%20Load%20Balancer/Assets/Edit%20Routes%20in%20RT.png)

Explanation: `0.0.0.0/0` means **Any destination Anywhere on the Internet**

```
Any Internet traffic

        ↓

Send through ALB-IGW
```

Your Route Table Should Look Like:

| Destination | Target  |
| ----------- | ------- |
| 10.0.0.0/16 | Local   |
| 0.0.0.0/0   | ALB-IGW |

![subnets](https://github.com/Pranith1Kumar/AWS-Shelf/blob/96b0076705f68edfa8f0b8861f7758689184fe0c/Beginner/AWS%20Top%2010%20Core%20Services%20Projects/Create%20an%20Application%20Load%20Balancer/Assets/Subnets.png)

## Step 13: Associate Route Table with Public Subnets

Currently

Your Route Table exists

but

No subnet is using it.

Associate Public Subnet A

- **Open:** `Public-RT`
- **Go to:** Subnet Associations
- Click on Edit Subnet Associations
- Select: `Public-Subnet-A`
- Click Save Associations


Associate Public Subnet B
- Repeat the process
- Select: `Public-Subnet-B`
- Save Changes.

![Subnet associations](https://github.com/Pranith1Kumar/AWS-Shelf/blob/96b0076705f68edfa8f0b8861f7758689184fe0c/Beginner/AWS%20Top%2010%20Core%20Services%20Projects/Create%20an%20Application%20Load%20Balancer/Assets/Associate%20Subnets.png)

##### **Why Is This Important?**

Without associating the route table, your subnets still cannot access the Internet. This is one of the most common mistakes beginners make.

## Step 14: Enable Auto-Assign Public IPv4

When launching EC2 instances, they need a public IP address. Otherwise, SSH and browser access won't work.

Configure Public Subnet A
- Go to Subnets section
- Select: `Public-Subnet-A`
- Click on Actions, clcik on Edit Subnet Settings
- Enable: `Auto-assign Public IPv4 Address`
- Save the changes.

Configure Public Subnet B
- Repeat the same steps.
- Enable: `Auto-assign Public IPv4 Address`
- Save changes.

**Verification**

Open each subnet.

You should see `Auto Assign Public IPv4` **Enabled**

![enable IPv4](https://github.com/Pranith1Kumar/AWS-Shelf/blob/96b0076705f68edfa8f0b8861f7758689184fe0c/Beginner/AWS%20Top%2010%20Core%20Services%20Projects/Create%20an%20Application%20Load%20Balancer/Assets/Enable%20IPv4.png)

## Step 15: Verify Your Networking

At this point, your networking should look like this:

`VPC (ALB for Top 10) with 10.0.0/16 --> Subnet A & B with 10.0.1.0/24 and 10.0.2.0/24 respectivley --> both subets connected to Route Table (Public RT) --> RT connected to Internet Gateway (ALB-IGW) --> Internet`


## Step 16: Create Security Groups

#### **What is a Security Group?**

An AWS Security Group is like a digital security guard for your cloud servers. It acts as a virtual firewall that decides exactly who is allowed to enter (inbound traffic) and who is allowed to leave (outbound traffic) based on a list of approved rules you create. By default, it locks all the front doors to keep strangers out, but leaves the exit doors open so your server can talk to the internet. It is also smart and stateful, meaning if you let a visitor come inside, the guard automatically remembers them and lets them walk back out without checking their ID again.

In simple terms: A Security Group (SG) is a virtual firewall that controls inbound (incoming) and outbound (outgoing) traffic for AWS resources such as EC2 instances and the Application Load Balancer.

Unlike a traditional firewall, Security Groups are stateful, meaning if you allow incoming traffic, the corresponding response traffic is automatically allowed.

For this project, we will create **two separate Security Groups**:

1. ALB-SG – attached to the Application Load Balancer.
2. WebServer-SG – attached to the EC2 instances.

This separation follows AWS security best practices because the ALB is the only component exposed to the Internet, while the EC2 instances only accept traffic forwarded by the ALB.

## Step 17: Create the Application Load Balancer Security Group

#### **Why is this Security Group needed?**

The Application Load Balancer must accept HTTP requests from users on the Internet.

When a user types the ALB DNS name into a browser:

```Browser --> Application Load Balancer```

The request reaches the ALB only if its Security Group allows HTTP traffic.

**Create ALB-SG**

1. Open the AWS Console.

Search for: EC2 Open the EC2 Dashboard.

2. In the left menu, click: Network & Security --> Security Groups
3. Click: Create Security Group
4. Fill in the details.
  | Setting             | Value                                        |
  | ------------------- | -------------------------------------------- |
  | Security Group Name | ALB-SG                                       |
  | Description         | Security Group for Application Load Balancer |
  | VPC                 | ALB-Project-VPC                              |
5. Configure Inbound Rules, Click Add Rule.

Rule 1
| Property | Value                     |
| -------- | ------------------------- |
| Type     | HTTP                      |
| Protocol | TCP                       |
| Port     | 80                        |
| Source   | Anywhere IPv4 (0.0.0.0/0) |

Click Add Rule again.

Rule 2 (Optional but Recommended)

| Property | Value         |
| -------- | ------------- |
| Type     | HTTPS         |
| Protocol | TCP           |
| Port     | 443           |
| Source   | Anywhere IPv4 |

> [!IMPORTANT]
> We won't configure HTTPS in this beginner project, but adding this rule prepares the ALB for future SSL/TLS implementation.

Configure Outbound Rules

Leave the default rule:

- Type: All Traffic
- Destination: 0.0.0.0/0

This allows the ALB to communicate with backend EC2 instances.

Click: `Create Security Group`

Expected Result You should now have: `ALB-SG`

![SG1](https://github.com/Pranith1Kumar/AWS-Shelf/blob/96b0076705f68edfa8f0b8861f7758689184fe0c/Beginner/AWS%20Top%2010%20Core%20Services%20Projects/Create%20an%20Application%20Load%20Balancer/Assets/Create%20SG1.png)

## ****Step 18: Create the EC2 Security Group****

#### **Why is a Separate Security Group Needed?**

The EC2 instances should not accept direct HTTP requests from the Internet. Instead, only the ALB should communicate with them.

For learning purposes, we'll also allow SSH access so you can connect to the servers.

1. Create WebServer-SG
- Click:
- Create Security Group

Fill below details:
| Setting             | Value                                 |
| ------------------- | ------------------------------------- |
| Security Group Name | WebServer-SG                          |
| Description         | Security Group for Ubuntu Web Servers |
| VPC                 | ALB-Project-VPC                       |

Configure Inbound Rules

**Rule 1: SSH**, This allows you to connect to the EC2 instance

| Property | Value |
| -------- | ----- |
| Type     | SSH   |
| Protocol | TCP   |
| Port     | 22    |
| Source   | My IP |


**Rule 2: HTTP**, This allows web traffic from the ALB.

| Property | Value  |
| -------- | ------ |
| Type     | HTTP   |
| Protocol | TCP    |
| Port     | 80     |
| Source   | ALB-SG |

>[IMPORTANT]
> When selecting the source, choose Security Group and select ALB-SG. This ensures only the ALB can access the web servers on port 80.

Outbound Rules

Keep the default rule: Type: All Traffic, Destination: Anywhere

Click on `Create Security Group`

![SG2](https://github.com/Pranith1Kumar/AWS-Shelf/blob/96b0076705f68edfa8f0b8861f7758689184fe0c/Beginner/AWS%20Top%2010%20Core%20Services%20Projects/Create%20an%20Application%20Load%20Balancer/Assets/Create%20SG2.png)

check both SG's

![SG1&2](https://github.com/Pranith1Kumar/AWS-Shelf/blob/96b0076705f68edfa8f0b8861f7758689184fe0c/Beginner/AWS%20Top%2010%20Core%20Services%20Projects/Create%20an%20Application%20Load%20Balancer/Assets/Create%20SG1%262.png)


## Step 19: Launch EC2 Instance 1

Open the EC2 Dashboard.

- Click: Launch Instance
- Enter VM Name: `WebServer-1`
- Choose an AMI choose `Ubuntu Server 26.04 LTS` or for best results use 24 version.
- Instance Type Choose: `t3.micro` depending on Free Tier eligibility.
- Key Pair: Create a new key pair or use an existing one.
  - Example: `alb-keypair`
  - Download the `.pem` file and store it safely.
- Network Settings
- Click Edit.
Configure: For best View check image

| Setting               | Value           |
| --------------------- | --------------- |
| VPC                   | ALB-Project-VPC |
| Subnet                | Public-Subnet-A |
| Auto-assign Public IP | Enabled         |
| Security Group        | Select Existing |
| Security Group        | WebServer-SG    |

Storage

Keep the default: Volume: gp3, Size 8GB, in my case I use gp2 with 8GB

- Click on launch instance.

![Network settings for VM1](https://github.com/Pranith1Kumar/AWS-Shelf/blob/96b0076705f68edfa8f0b8861f7758689184fe0c/Beginner/AWS%20Top%2010%20Core%20Services%20Projects/Create%20an%20Application%20Load%20Balancer/Assets/Network%20settings%20for%20VM%201.png)

## Step 20: Launch EC2 Instance 2

- Repeat the same process.

Use these values:

| Setting        | Value           |
| -------------- | --------------- |
| Name           | WebServer-2     |
| AMI            | Ubuntu 26.04    |
| Instance Type  | t2.micro        |
| VPC            | ALB-Project-VPC |
| Subnet         | Public-Subnet-B |
| Security Group | WebServer-SG    |
| Key Pair       | alb-keypair     |

- Click on Launch Instance

![Nwtwork config for VM2](https://github.com/Pranith1Kumar/AWS-Shelf/blob/96b0076705f68edfa8f0b8861f7758689184fe0c/Beginner/AWS%20Top%2010%20Core%20Services%20Projects/Create%20an%20Application%20Load%20Balancer/Assets/Network%20Settings%20for%20VM%202.png)

## Step 21: Verify Both Instances

Wait until both instances show:

![Checks passed](https://github.com/Pranith1Kumar/AWS-Shelf/blob/96b0076705f68edfa8f0b8861f7758689184fe0c/Beginner/AWS%20Top%2010%20Core%20Services%20Projects/Create%20an%20Application%20Load%20Balancer/Assets/Vm%201%26%202.png)


## Step 22: Connect to Ubuntu via SSH

- Open a terminal on your local machine.
- Navigate to the directory containing your key pair.

Example:

```bash
cd ~/Downloads
```

- Set the correct permissions:

```bash
chmod 400 alb-keypair.pem
```

- Connect to WebServer-1:

```bash
ssh -i alb-keypair.pem ubuntu@<PUBLIC_IP_OF_WEBSERVER_1>
```

Example:

```bash
ssh -i alb-keypair.pem ubuntu@13.126.250.203
```
- When prompted:
Are you sure you want to continue connecting (yes/no)?

- Type: Yes
- You should now see a prompt similar to: `ubuntu@WebServer-1:~$`

Repeat the same process for WebServer-2 using its public IP.

## Step 23: Update Ubuntu Packages

Run the following commands on both EC2 instances.

Update the package index:

```bash
sudo apt update
```

Upgrade installed packages:

```bash
sudo apt upgrade -y
```

This ensures the operating system is up to date before installing software.

## Step 24: Install Apache Web Server

Apache is the web server software that will host our website.

Install Apache:

```bash
sudo apt install apache2 -y
```

Start Apache

```bash
sudo systemctl start apache2
```

Enable Apache to start automatically after reboot:

```bash
sudo systemctl enable apache2
```

Verify Apache Status

Run:

```bash
sudo systemctl status apache2
```
You should see output indicating:

Active: active (running)

![Apache Status](https://github.com/Pranith1Kumar/AWS-Shelf/blob/96b0076705f68edfa8f0b8861f7758689184fe0c/Beginner/AWS%20Top%2010%20Core%20Services%20Projects/Create%20an%20Application%20Load%20Balancer/Assets/Apache%20active.png)

Press: q to exit the status screen or ctrl + c.

## Step 25: Test Apache

- Open a browser and visit:

`http://<PUBLIC_IP_OF_WEBSERVER_1>`

You should see the default Apache page:

`Apache2 Ubuntu Default Page`

Repeat for WebServer-2.

If you can access both pages, your Ubuntu web servers are correctly configured and ready for the next stage.

## **Step 26: Verify Apache Document Root**

On both EC2 instances, Apache stores website files in:

```bash
/var/www/html
```
- Check the existing files:

```bash
cd /var/www/html
ls -la
```

You should see something similar to: `index.html`

This is the default Apache page that we'll replace.

## **Step 27: Remove the Default Apache Page**

- Run the following command on both servers:

```bash
sudo rm -f /var/www/html/index.html
```
- Verify the directory is empty:

```bash
ls -la /var/www/html
```


## **Step 28: Create the Website**

WebServer-1

Create the HTML file:

```bash
sudo nano /var/www/html/index.html
```

Paste the following code exactly:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AWS Application Load Balancer Project</title>

<style>

body{
    margin:0;
    padding:0;
    background:#f5f7fa;
    font-family:Arial,Helvetica,sans-serif;
}

.container{
    width:80%;
    margin:auto;
    margin-top:50px;
    text-align:center;
}

.card{
    background:white;
    padding:40px;
    border-radius:10px;
    box-shadow:0px 0px 20px rgba(0,0,0,0.2);
}

h1{
    color:#232f3e;
}

.server{
    font-size:40px;
    color:#ff9900;
    margin:20px;
}

.status{
    color:green;
    font-weight:bold;
    font-size:24px;
}

.info{
    margin-top:30px;
    font-size:18px;
}

.footer{
    margin-top:30px;
    color:gray;
}

</style>

</head>

<body>

<div class="container">

<div class="card">

<h1>AWS Application Load Balancer Project</h1>

<div class="server">

Web Server 1

</div>

<div class="status">

Server Status : Healthy

</div>

<div class="info">

<p><strong>Hostname:</strong></p>

<pre>
<script>
document.write(window.location.hostname);
</script>
</pre>

<p>This request has been served by EC2 Instance 1.</p>

<p>After configuring the Application Load Balancer, refreshing the browser should alternate between Web Server 1 and Web Server 2 depending on load balancing and health status.</p>

</div>

<div class="footer">

Project Created Using

Ubuntu Server • Apache2 • AWS EC2 • Application Load Balancer

</div>

</div>

</div>

</body>
</html>
```

- Save the File
- Press: `CTRL + O`
- Press: Enter
- Exit Nano: `CTRL + X`

## **Step 29: Create the Website on WebServer-2**

- Repeat the same steps on WebServer-2:

```bash
sudo nano /var/www/html/index.html
```

- Paste the same HTML code, but change only this section:
- Replace: `Web Server 1` with `Web Server 2`
- Replace: `This request has been served by EC2 Instance` 1. with `This request has been served by EC2 Instance 2.`
- Save the file using:
  - CTRL + O
  - Enter
  - CTRL + X

##** Step 30: Set File Permissions**

Run the following command on both servers:

```bash
sudo chmod 644 /var/www/html/index.html
```

## **Step 31: Restart Apache**

- Restart Apache on both servers to ensure the new page is served:

```bash
sudo systemctl restart apache2
```

- Check its status:

```bash
sudo systemctl status apache2
```

- You should see: `Active: active (running)`
- Press: q to exit.

![Apache Active](https://github.com/Pranith1Kumar/AWS-Shelf/blob/96b0076705f68edfa8f0b8861f7758689184fe0c/Beginner/AWS%20Top%2010%20Core%20Services%20Projects/Create%20an%20Application%20Load%20Balancer/Assets/Apache%20active.png)


## **Step 32: Test the Website**

- Open your browser.

Visit the public IP of WebServer-1: `http://<WebServer-1-Public-IP>`

Expected output:

Title: AWS Application Load Balancer Project

Large heading: Web Server 1

Status: Healthy

Footer mentioning Ubuntu, Apache2, EC2, and ALB.

As per my HTMl code

![ALB VM1](https://github.com/Pranith1Kumar/AWS-Shelf/blob/96b0076705f68edfa8f0b8861f7758689184fe0c/Beginner/AWS%20Top%2010%20Core%20Services%20Projects/Create%20an%20Application%20Load%20Balancer/Assets/ALB%20Web%201.png)


- Now visit: `http://<WebServer-2-Public-IP>`
  
Expected output:

The same design.

The heading should display Web Server 2.

![ALB VM2](https://github.com/Pranith1Kumar/AWS-Shelf/blob/96b0076705f68edfa8f0b8861f7758689184fe0c/Beginner/AWS%20Top%2010%20Core%20Services%20Projects/Create%20an%20Application%20Load%20Balancer/Assets/ALB%20Web%202.png)

This confirms that each server serves its own page, which will later help you verify that the ALB is distributing traffic correctly.

## **Step 33: Verify Apache Listens on Port 80**

- On either server, run:

```bash
sudo ss -tulnp | grep :80
```
- Expected output: LISTEN

## **Step 34: Confirm Web Accessibility**

At this stage:

- Both EC2 instances are reachable via their public IPs.
- Apache is serving your custom page.
- Each page clearly identifies the server.
- The root path (/) returns HTTP 200 OK, which will be used by the ALB health checks.
- This confirms Apache is actively listening for HTTP requests.

## **Step 35: Create a Target Group**

What is a Target Group?

A Target Group is a logical collection of backend servers (targets) that receive traffic from the Application Load Balancer.

Think of it as a team of web servers.

```
                Application Load Balancer
                          │
                          ▼
                  Target Group (Web-TG)
                   ┌────────┴────────┐
                   │                 │
                   ▼                 ▼
             WebServer-1       WebServer-2
```

Instead of the ALB sending traffic directly to EC2 instances, it always sends traffic to a Target Group, which then forwards it to healthy targets.


#### **Why Do We Need a Target Group?**

The Target Group is responsible for:

- Registering EC2 instances.
- Performing health checks.
- Forwarding requests only to healthy instances.
- Automatically stopping traffic to failed servers.
- Enabling future auto scaling.

Without a Target Group, the ALB has nowhere to send requests.

## **Step 36: Create the Target Group**

- Open the EC2 Console
- Log in to the AWS Management Console.
- Search for EC2.
- Open the EC2 Dashboard.
- In the left menu, scroll to Load Balancing.
- Click Target Groups.

Create a New Target Group

Click: Create Target Group

Basic Configuration
Choose Target Type

Select: **Target Type:** Instances
This means our backend servers are EC2 instances.
- Click Next.


Target Group Details

| Setting           | Value           |
| ----------------- | --------------- |
| Target Group Name | Web-TG          |
| Protocol          | HTTP            |
| Port              | 80              |
| IP Address Type   | IPv4            |
| VPC               | ALB-Project-VPC |
| Protocol Version  | HTTP1           |

- Health Check Configuration
- Scroll down to the Health Checks section.
- Configure the following values.

| Setting               | Value        |
| --------------------- | ------------ |
| Health Check Protocol | HTTP         |
| Health Check Path     | /            |
| Port                  | Traffic Port |
| Healthy Threshold     | 2            |
| Unhealthy Threshold   | 2            |
| Timeout               | 5 Seconds    |
| Interval              | 30 Seconds   |
| Success Codes         | 200          |

#### **Why are we using /?**

Our website is served from:

`http://server-ip/`

The server returns: `HTTP 200 OK`

Since the page is always available when Apache is healthy, using / as the health check path is simple and effective for this project.

## **Step 37: Register EC2 Instances**

AWS now displays all available EC2 instances.

You should see:

- WebServer-1
- WebServer-2

Select both instances.

Click: Include as Pending Below

The instances will appear under Targets.

Click: Create Target Group

## **Step 38: Verify Target Group**

- Open: `Web-TG`
- Go to: `Targets`

Initially, the status may be: `Initial`

Wait approximately 30–60 seconds while AWS performs the first health check.

The status should then change to:

`Healthy`

Both instances should display:

`
Health Status:
Healthy`

**Troubleshooting Target Health**

If the instances remain Unhealthy, check the following:

1. Apache Service

SSH into the instance and verify:

```bash
sudo systemctl status apache2
```

The status must be: `Active: active (running)`

2. Test the Website

- Run: 

```bash
curl http://localhost
```

You should receive the HTML content of your page.

3. Verify Security Group

The EC2 Security Group must allow:

| Type | Port | Source |
| ---- | ---- | ------ |
| HTTP | 80   | ALB-SG |


If the source is incorrect (for example, Anywhere instead of ALB-SG), update it.

4. Confirm Apache is Listening

Run:

```bash
sudo ss -tulnp | grep :80
```

Expected output: `LISTEN`

## **Step 39: Create the Application Load Balancer**

Now we'll create the Application Load Balancer.

Go to:

```
EC2 Dashboard

    ↓

Load Balancers

    ↓

Create Load Balancer
```

- Choose: `Application Load Balancer`
- Click: Create

Basic Configuration

| Setting            | Value           |
| ------------------ | --------------- |
| Load Balancer Name | Web-ALB         |
| Scheme             | Internet-facing |
| IP Address Type    | IPv4            |

Network Mapping

Choose: VPC --> ALB-Project-VPC

Select both public subnets:

- Public-Subnet-A
- Public-Subnet-B

AWS automatically deploys one ALB node in each selected Availability Zone.


**Security Groups**

Choose: `ALB-SG`

This Security Group allows the ALB to receive HTTP traffic from users.

**Listener Configuration**

Leave the default listener: `HTTP -->	80`

**Default Action**

- Choose: Forward To
- Select: `Web-TG`

This tells the ALB to forward incoming HTTP requests to the Target Group you created.

- Click: `Create Load Balancer`

## **Step 40: Wait for the ALB to Become Active**

The ALB status will initially be: `Provisioning`

Wait a few minutes.

Refresh the page.

The status should become: `Active`

## **Step 41: Copy the ALB DNS Name
**
- Open: `Web-ALB`
- Locate the field: `DNS Name`

Example:

`
Web-ALB-123456789.ap-south-1.elb.amazonaws.com
`  

- Copy this value.

## **Step 42: Test the Application Load Balancer**

- Open your browser.
- Visit: `http://<ALB-DNS-Name>`
- Example: `http://Web-ALB-123456789.ap-south-1.elb.amazonaws.com`

You should see your custom web page.

## **Step 43: Verify Load Balancing**

Refresh the page multiple times.

Depending on the ALB's round-robin algorithm, you should observe:

Refresh 1 --> Web Server 1 
Refresh 2 --> Web Server 2
Refresh 3 --> Web Server 1
Refresh 4 --> Web Server 2

**Note:** Modern browsers may cache content or reuse TCP connections, so alternating on every refresh is not guaranteed. If you keep seeing the same server:

- Open the ALB DNS in an Incognito/Private window
- Use another browser.
- Or use the following command repeatedly:

```bash
curl http://<ALB-DNS-Name>
```

This often makes the distribution easier to observe.

## **Step 44: Validate High Availability**

Now we'll verify the ALB's health monitoring.

- Go to the EC2 Dashboard.
Select WebServer-1.
- Click: `Instance State --> Stop Instance`
- Wait until the instance is fully stopped.
Then:
- Open Target Groups.
- Select Web-TG.
- Open the Targets tab.

After a short period, you should see:
- Instance	Health Status
- WebServer-1	Unhealthy
- WebServer-2	Healthy
- Now access the ALB DNS name again.
- You should still see your website, but it will always be served by WebServer-2.

This demonstrates that the Application Load Balancer automatically routes traffic only to healthy instances, ensuring high availability without manual intervention.

# **Done You have successfully created ALB with managing traffic with EC2 instances and chcecking health checks.**


## **AWS ALB Project Cleanup**

Resources You Have Created

| Resource         | Example Name                       |
| ---------------- | ---------------------------------- |
| VPC              | `ALB-Project-VPC`                  |
| Internet Gateway | `ALB-IGW`                          |
| Route Table      | `Public-RT`                        |
| Public Subnet A  | `Public-Subnet-A`                  |
| Public Subnet B  | `Public-Subnet-B`                  |
| Security Group   | `ALB-SG`                           |
| Security Group   | `WebServer-SG`                     |
| EC2 Instance     | `WebServer-1`                      |
| EC2 Instance     | `WebServer-2`                      |
| Key Pair         | `alb-keypair` (optional to delete) |
| EBS Volumes      | Attached to the EC2 instances      |


**Step 1:** Terminate EC2 Instances (Most Important)
- Open the AWS Management Console.
- Search for EC2
- Click Instances
- Select: `WebServer-1`, `WebServer-2`
- Click: Instance State --> Terminate Instance
- Confirm by clicking Terminate.
- Wait for Completion

The instance state should change:

Running --> Shutting Down --> Terminated

Do not continue until both instances show Terminated.

**Step 2: Verify EBS Volumes Are Deleted**

Normally, the root EBS volume is deleted automatically when an EC2 instance is terminated if Delete on Termination was enabled (it is by default).

To verify:

1. In the EC2 Dashboard, click Volumes
2. Check whether any volumes remain.

If you see leftover volumes:

- Select the volume.
- Click: Actions --> Delete Volume
  
3. Confirm the deletion.

If there are no volumes, you can skip this step.

**Step 3: Delete Security Groups**

Go to: `EC2 --> Security Groups`

Delete:

- ALB-S
- WebServer-SG

If you receive a message saying a Security Group is in use, ensure the EC2 instances are fully terminated and refresh the page before trying again.

**Step 4: Delete Route Table**

- Go to: VPC --> Route Tables
- Select: Public-RT
- Click: Actions --> Delete Route Table

>[IMPORTANT]
> If AWS reports that the Route Table has subnet associations, first remove those associations from the Subnet Associations tab, leaving only the main route table associated with the VPC.

**Step 5: Detach and Delete the Internet Gateway**

- Go to: VPC --> Internet Gateways
- Select: `ALB-IGW
- Click: Actions --> Detach Internet Gateway
- Choose: `ALB-Project-VPC`
- Click Detach.
- After it is detached: Actions -->Delete Internet Gateway
- Confirm the deletion.

**Step 6: Delete Public Subnets**

- Go to: VPC --> Subnets
- Delete:
  - Public-Subnet-A
  - Public-Subnet-B
- Click: Actions --> Delete Subnet
- Confirm for each subnet.


**Step 7: Delete the Custom VPC**

- Go to: VPC --> Your VPCs
- Select: `ALB-Project-VPC`
- Click: Actions --> Delete VPC

Type the confirmation text if prompted and confirm the deletion.

**Step 8: Delete the Key Pair (Optional)**

Deleting the key pair from AWS does not delete the `.pem` file stored on your computer.

- Go to: EC2 --> Key Pairs
- Select: `alb-keypair`
- Click: Actions --> Delete

If you don't plan to reuse it, you can also delete the .pem file from your local machine.

