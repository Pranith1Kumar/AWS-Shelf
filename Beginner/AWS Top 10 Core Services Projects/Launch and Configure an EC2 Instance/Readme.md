# *Hosting a Personal Python App on AWS EC2*


## Prerequisites
1. AWS Account [Create Here](https://signin.aws.amazon.com/signup?request_type=register)
2. AWS CLI configured locally
3. Key pair (for SSH access)
4. Python installed locally

## Terminology

1. **EC2 (Elastic Compute Cloud):** EC2 is a virtual server in the cloud that you can use to deploy and run applications like a Python app, offering scalable computing capacity on-demand. Instances are of various types [Click Here to explore.](https://aws.amazon.com/ec2/instance-types/)
2. **AMI (Amazon Machine Image):** An AMI is a pre-configured template containing the OS and software used to launch EC2 instances, helping you start with a ready environment like Amazon Linux 2, Ubuntu, etc.
3. **t2.micro Instance:** A t2.micro is a cost-effective, burstable compute instance type in EC2 ideal for low-traffic applications and is part of AWS Free Tier for new users.
4. **Key Pair (.pem file):** A key pair is used for secure SSH access to your EC2 instance, consisting of a public and private key to authenticate connections.
5. **Security Group:** A Security Group acts as a virtual firewall controlling inbound and outbound traffic for your EC2 instance, where you allow ports like 22 (SSH) and 5000 (Flask).
6. **Elastic IP (optional):** An Elastic IP is a static public IPv4 address you can associate with your EC2 instance to maintain a consistent IP even if the instance restarts.
7. **SSH (Secure Shell):** SSH is a protocol used to securely connect and manage your EC2 instance from your local machine using a terminal and your key pair.

## Step 1: Create Python Application Locally

1. Create a Directory named Python-EC2 in my case. (e.g., python-app/).
2. If using CLI like Command Prompt or Powershell for creating and change of  directory to project folder in my case it is Python-EC2.
   
     - If you want to create using CLI follow below commands:
       
         ```bash
         mkdir Python-EC2 && cd Python-EC2
         ```
         
      - Replace your Directory name `Python-EC2` to your directory name.
        
3. Create `app.py`

    ```python
    from flask import Flask # type: ignore
  
    app = Flask(__name__)
    
    @app.route('/')
    def hello():
        return "Hello from your EC2 Python App!"
    
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)
    ```

4. Create `requirements.txt`:

    ```txt
    flask
    ```

## Step 2: Launch EC2 Instance

1. Go to AWS Console search for EC2 then hit on Launch Instance.
2. Name the Instance in my case it is `my-first-vm` (You can use any name for your VM).

   ![Instance name](https://github.com/user-attachments/assets/fdcf706c-aee1-436d-b857-a218518527f8)
   
3. Select AMI, AMI is used as OS for your VM in my case it is `Ubuntu Server 24.04 LTS (HVM)` (Free Tier available).

   ![AMI](https://github.com/user-attachments/assets/85e3b581-f71a-46f5-88d5-311bbdc23d84)

4. Select Instance type this is also known as family types where each character describe the importance (`t`- refers to instance family, `2` is the family generation and `micro` refers to instance size Instance `t2.micro` (Free-Tier avialable).
   
    ![Family](https://github.com/user-attachments/assets/88ce07a3-3d9d-4dd5-be56-0132a7aa7dcb)
   
5. Key value pair is used to encrypt the Instance to avoid explicit and unauthorized connection woth instance, it is a protected key we need this key to connect to our vm in my case it is, create new (`pythonkey.pem`) keep remaining as default, if ypu use putty select  `.ppk` else select  `.pem`.
   
    ![Key pair](https://github.com/user-attachments/assets/69fe0d2f-d615-4ede-87d6-ec95f21ca484)

6. In security group section allow 
    - SSH (port 22)
    - HTTP (port 80)
    - Custom TCP (port 5000) (Allow in Security groups in inbound rules add the above rules).

7. Select Storage for VM it is EBS volumes, consider and select `8 GiB gp2` (which is not default select according) `gp2` is in free-tier not `gp3`.
8. Launch the instance and note its Public IPv4 Address.

   ![Launch](https://github.com/user-attachments/assets/154c1943-90c5-4c8b-afee-8b1e0944df40)

9. In Instances section ceck for status if your Instance pass 2/2 Checks in console then you are ready to connect to instance.

## Step 3: Connect to EC2 via SSH

If you are unable to connect to your instance directly using ssh -i <key-file> ubuntu@<EC2-public-ip>, please follow the steps starting from point 1. Otherwise, you can proceed directly to step 2.

![No access](https://github.com/user-attachments/assets/762a0b04-0107-433c-9ecd-9a33d8975dcc)

1. Change permissions for `.pem` file using `chmod 400 your-key.pem` if you use Unix/Linux if you use Windows follow below commands:
   
    - ```bash
      icacls.exe “pythonkey.pem” /reset
      ```
    - ```bash
      icacls.exe “pythonkey.pem” /grant:r “$($env:username):(r)”
      ```
    - ```bash
      icacls.exe “pythonkey.pem” /inheritance:r
      ```
    
Replace  `pythonkey.pem` with your key pair file name.

This `chmod 400 pythonkey.pem` allow us to connect to instance, if we have not change the permissions it will not allow us to SSH the Instance.

  ![chmod](https://github.com/user-attachments/assets/304100e8-097f-4814-a3ad-ce4f9892853d)

2. Connect to Instance using `ssh -i "pythonkey.pem" ubuntu@<EC2-Public-IP>` . (Replace `pythonkey.pem` with your `.pem` file and public IP of instance find your Public IP in Console).

     ![Success launch](https://github.com/user-attachments/assets/de2af1da-01a7-4f28-a801-84b2cc5f96ca)

## Step 4: Set Up Python Environment on EC2

Update and install Python, pip, virtualenv using below command
  
  ```bash
  sudo apt update && sudo apt install -y python3-pip python3-venv
  ```

  ![python3 d](https://github.com/user-attachments/assets/92d4c25e-0648-4890-9802-074aee4fc388)

  - Create project directory in Instance
   
     ```bash
     mkdir python-app && cd python-app
     ```

  - Create virtual environment using below commands
  
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

  - Install Flask used for deploy python application
      
     ```bash
     pip install flask
     ```

     ![bin](https://github.com/user-attachments/assets/3a190b22-7d07-4007-984e-68337a9354c4)

## Step 5: Transfer App Files to EC2

From your local terminal: This command used in our local machine is used for copying files from Local Machine to EC2 pyhton-app directory `scp` refers to `securecopy`

   ```bash
   scp -i "pythonkey.pem" app.py requirements.txt ubuntu@<EC2-Public-IP>:~/python-app/
   ```

  ![scp](https://github.com/user-attachments/assets/68096c53-cb4e-4198-b90d-ad8fa9343138)

Replace `pythonkey` with your `.pem` file name and replace your Public IP

SSH again and install requirements: This install  the flask and any dependencies in requirements file.

```
cd python-app
source venv/bin/activate
pip install -r requirements.txt
```

![requirements](https://github.com/user-attachments/assets/6fae64bb-abed-4503-9830-39e8eeb7f852)

## Step 6: Run Your Python App
1. Start your application using

   ```bash
   python3 app.py
   ```

   ![deploy](https://github.com/user-attachments/assets/489df561-54ac-40a7-950a-b649bcdb6cc9)

Your app will be running at:

2. `http://<EC2-Public-IP>:5000/` Replace `<EC2-Public-IP>` with your public IP (If your application is not live your hav not configured the inbound rules of instance).

    ![Successful](https://github.com/user-attachments/assets/ad31a162-219b-4155-899c-7fe5901dd117)

**NOTE: Ensure that only necessary ports are open in the Security Group and never expose your EC2 with wide-open rules in production.**

## Step 7: If you want to run app in background use nohup

```bash
nohup python3 app.py &
```
It isn use to run your application in detached mode.

## Step 8: Destroy
1. Close your application from CLI using `CTRL+C`.
2. Logout from your Instance using `exit`.
3. In Console check the instance for terminate the session.
4. Check after termination check wheather instance is deleted or not.

     ![Terminate](https://github.com/user-attachments/assets/298f2f2e-5c29-4a44-b333-d9b6cffd0229)

5. In Left navigation basr check for Elastic Block Store in that check wheather Volume is deleted or not.
6. In Key Pair Section delete the key pair.

# *EC2 Pricing Quick View (as of 2025 – US East, Linux On-Demand)*
| Instance Type | vCPU | RAM  | Hourly Rate (USD) | Monthly (Approx) |
| ------------- | ---- | ---- | ----------------- | ---------------- |
| **t2.micro**  | 1    | 1 GB | \$0.0116          | \~\$8.35         |
| **t3.micro**  | 2    | 1 GB | \$0.0104          | \~\$7.75         |
| **t3.small**  | 2    | 2 GB | \$0.0208          | \~\$15.00        |

For more Pricing and Instance options refer: [Click Here](https://aws.amazon.com/ec2/pricing/on-demand/)

**`t2.micro` is eligible for AWS Free Tier: 750 hours/month free for the first 12 months.**
