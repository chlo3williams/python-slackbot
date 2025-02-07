# Slack GitHub Discussions Bot (AWS Lambda)

## Overview 📌
**Language: Python**

This AWS Lambda function listens for Slack slash commands and fetches the latest GitHub Discussions from a repository and posts them to a Slack channel.

## Features 🚀 
- Listens for `/latest-discussions` command in Slack
- Fetches open discussions from a specified GitHub repository
- Posts the discussions to a Slack channel
- Uses AWS Lambda for serverless execution

## Environment Variables 🛠

This Lambda function requires the following environment variables:

| Variable Name     | Description                                             |
| ----------------- | ------------------------------------------------------- |
| `SLACK_BOT_TOKEN` | Slack bot token for authentication                      |
| `GITHUB_TOKEN`    | GitHub personal access token with GraphQL API access    |
| `SLACK_CHANNEL`   | The Slack channel ID where discussions should be posted |
| `REPO_OWNER`      | GitHub repository owner (organization/user)             |
| `REPO_NAME`       | GitHub repository name                                  |

## Installation & Setup 🐍

### Prerequisites

- Python 3.x installed

### Steps
1. **Clone the repository**  
   ```sh
   git clone https://github.com/chlo3williams/python-slackbot.git
   ```

2. **Install the required dependencies**  
   ```sh
   pip install -r requirements.txt -t .
   ```

3. **Package the code**  
   ```sh
   zip -r slack-github-discussions.zip .
   ```

4. **Deploy the code to AWS Lambda**  

   - If the function **does not exist**, create it using the following command:
     ```sh
     aws lambda create-function --function-name slack-github-discussions \
       --zip-file fileb://slack-github-discussions.zip \
       --handler slack_github_discussions.lambda_handler \
       --runtime python3.9 \
       --role arn:aws:iam::YOUR_ACCOUNT_ID:role/YOUR_LAMBDA_ROLE
     ```

   - If the function **already exists**, update it using:
     ```sh
     aws lambda update-function-code --function-name slack-github-discussions \
       --zip-file fileb://slack-github-discussions.zip
     ```

5. **Set the required environment variables in the AWS Lambda console.**  
   (Alternatively, you can set them via AWS CLI.)

## Deploying with `deploy.sh`

A `deploy.sh` script is included to automate deployment.

### **1️. Make the script executable**
```sh
chmod +x deploy.sh
```

### **2️. Run the script**
```sh
./deploy.sh
```

The script will:
- Package the Lambda function into a ZIP file
- Check if the Lambda function exists:
  - If **yes**, it updates the function code
  - If **no**, it creates the function
- Print a success message when complete

Note: Make sure your AWS CLI is configured with the necessary permissions before running the script

## How The Slackbot Works

1. A user in Slack types `/latest-discussions`.
2. Slack sends an event to this AWS Lambda function.
3. The function queries GitHub's GraphQL API for discussions in the specified repository.
4. The results are formatted into a message and sent back to the Slack channel.

## Example API Response

```json
{
  "statusCode": 200,
  "body": "Your request is being processed."
}
```

✨ Made by [Chloe Williams](https://github.com/chlo3williams)
