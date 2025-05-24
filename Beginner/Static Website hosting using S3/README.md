# *Static Website Hosting on AWS S3*

This guide will help you host a static website (like one built with HTML/CSS/JS) on Amazon S3 

### Prerequisites
Before we begin, make sure you have:

- An AWS account (Free Tier works!), we are using AWS Console for this project.
- [Create a AWS Account if not](https://aws.amazon.com/)
- A basic website ready (like index.html, style.css, and maybe an error.html file)
- A browser and internet connection.


## Terminology used:

1. **Amazon S3 (Simple Storage Service):** An AWS object storage service used to store and serve static website files like HTML, CSS, and JavaScript.
2. **S3 Bucket:**	A container in S3 that stores data as objects, uniquely named and region-specific.	Acts as the "folder" that holds your website files.
3. **S3 Object:**	A single file (like index.html) stored in an S3 bucket, along with its metadata.	Represents your actual website content.
4. **Static Website Hosting (S3 Feature):** A configuration option in S3 that turns a bucket into a web server capable of serving static content via a public URL.
5. **Bucket Policy:** A JSON-based access control mechanism that makes your S3 files publicly readable so anyone can access the website.
6. **Index Document:** The main entry point (usually index.html) that loads by default when someone visits your website’s root URL.
7. **Error Document:** A fallback page (like error.html) shown when a user tries to access a non-existent file or page.
8. **AWS Management Console:** A web interface provided by AWS to interact with and manage AWS services like S3 without using the command line.

## Step 1: Get Your Website Files Ready
1. Create a folder on your computer — name it something like my-static-website.
2. Add your website files to this folder:

`index.html` – This is your homepage.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>ModernSite | Home</title>
  <style>
    body {
      margin: 0;
      font-family: 'Segoe UI', sans-serif;
      background: linear-gradient(to right, #1e3c72, #2a5298);
      color: #fff;
    }
    header {
      padding: 1em 2em;
      display: flex;
      justify-content: space-between;
      align-items: center;
      background-color: rgba(0,0,0,0.3);
    }
    nav a {
      margin: 0 1em;
      text-decoration: none;
      color: #fff;
      transition: color 0.3s;
    }
    nav a:hover {
      color: #ffd700;
    }
    .hero {
      text-align: center;
      padding: 100px 20px;
    }
    .hero h1 {
      font-size: 3em;
      margin-bottom: 0.5em;
    }
    .hero p {
      font-size: 1.2em;
      max-width: 600px;
      margin: 0 auto;
    }
    button {
      margin-top: 2em;
      padding: 0.75em 1.5em;
      font-size: 1em;
      border: none;
      border-radius: 5px;
      background-color: #ffd700;
      color: #000;
      cursor: pointer;
      transition: transform 0.2s;
    }
    button:hover {
      transform: scale(1.05);
    }
    footer {
      text-align: center;
      padding: 1em;
      background-color: rgba(0,0,0,0.2);
      position: fixed;
      bottom: 0;
      width: 100%;
    }
  </style>
</head>
<body>
  <header>
    <h2>ModernSite</h2>
    <nav>
      <a href="#">Home</a>
      <a href="#about">About</a>
      <a href="error.html">404 Test</a>
    </nav>
  </header>
  <section class="hero">
    <h1>Welcome to ModernSite</h1>
    <p>Your one-stop destination for elegant web experiences using only HTML, CSS, and JS.</p>
    <button onclick="showMessage()">Get Started</button>
  </section>
  <footer>
    &copy; 2025 ModernSite. All rights reserved.
  </footer>

  <script>
    function showMessage() {
      alert("Let's build something great together!");
    }
  </script>
</body>
</html>
```

`error.html` – Optional, used for error pages like 404.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Page Not Found</title>
  <style>
    body {
      margin: 0;
      background: #111;
      color: #fff;
      font-family: 'Segoe UI', sans-serif;
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100vh;
      flex-direction: column;
    }
    h1 {
      font-size: 6em;
      color: #ff4b5c;
      margin: 0;
    }
    p {
      font-size: 1.5em;
      margin: 0.5em 0;
    }
    a {
      margin-top: 1.5em;
      text-decoration: none;
      background-color: #ff4b5c;
      color: #fff;
      padding: 0.75em 1.5em;
      border-radius: 5px;
      transition: background 0.3s;
    }
    a:hover {
      background-color: #e33;
    }
  </style>
</head>
<body>
  <h1>404</h1>
  <p>Oops! Page not found.</p>
  <a href="index.html">Back to Home</a>
</body>
</html>
```



## Step 2: Create a Bucket in Amazon S3
1. Log in to the AWS Console.
2. Search for and go to S3.
3. Click the “Create bucket” button.
4. Fill in these details:

- `Bucket name:` Must be globally unique (e.g., mahaan) and should be only lowercase.

- `Region:` Choose a region closest to your city.

![Bucket name](https://github.com/user-attachments/assets/606cb56b-d7d7-4aab-8128-650310d7ac2b)


5. Uncheck the “Block all public access” option in the permissions section.

![Block public](https://github.com/user-attachments/assets/b6babebe-e470-42a7-9dc2-e6c0dd627ac1)

6. Add tages (Optional)

![Tag](https://github.com/user-attachments/assets/3bb4f4ae-c244-4b1a-bea5-ca1b2c555009)

7. Check the acknowledgment box and click Create bucket.

![Bucket created](https://github.com/user-attachments/assets/5acd97d0-4c62-43b4-93c9-01d5bea99709)

### Step 3: Upload Your Website Files to the Bucket
1. Click the name of the bucket you just created (modern-website).
2. Hit “Upload” → “Add files”, and select your index.html, error.html, etc.
3. Click Upload to complete the process.

![Upload files](https://github.com/user-attachments/assets/4d0e331b-28a8-4082-9fb3-39e0292eeaf5)

### Step 4: Make Your Website Public
1. By default, S3 keeps your files private. Let’s change that so anyone on the internet can access your site:
2. Go to the Permissions tab of your bucket.
3. Scroll to Bucket Policy and click Edit.
4. Paste the following policy (replace modern-website with your actual bucket name):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::modern-website/*"
    }
  ]
}
```

![Policy'](https://github.com/user-attachments/assets/c9aaff8c-647d-4d5e-8098-f27888eac08e)

4. Click Save changes.

### Step 5: Enable Static Website Hosting
1. Now, let’s turn the bucket into a real website
2. Go to the Properties tab of the bucket.
3. Scroll to the Static website hosting section.
4. Click Edit and do the following:
   - Choose Enable.
   - For Index document, type: index.html
   - For Error document, type: error.html (if you have one) it redirects to this object when website is not available.
  
![static](https://github.com/user-attachments/assets/af95d8dd-13c7-49cf-ab4a-3806032de017)

5. Click Save changes.
You’ll now see a “Bucket website endpoint” URL, this is your public website link.

### Step 6: Test Your Website
1. Copy the website endpoint URL (found in the static hosting section).
2. Paste it into your browser.
3. You should now see your hosted website live on the internet.

### Step 7: Destroy
1. Empty the bucket (remove objects from bucket) before deleting the bucket.
2. Then Delete Bucket


## Pricing for Amazon S3

Amazon S3 Pricing (as of 2025)

| Feature | Free Tier | Standard Pricing (after Free Tier) |
| :---:         |     :---:      |    :---: |
| Storage   | 5 GB/month     | $0.023 per GB/month (first 50 TB)   |
| PUT, COPY, POST, LIST requests     | 	2,000/month       | 	$0.005 per 1,000 requests  |
| GET, SELECT, and all other requests |	20,000/month |	$0.0004 per 1,000 requests |
| Data Transfer Out (to internet) |	1 GB/month | free	$0.09 per GB (first 10 TB/month) |
