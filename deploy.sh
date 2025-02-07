#!/bin/bash

set -e # Exit on error

FUNCTION_NAME="slack-github-discussions"
ZIP_FILE="slack-github-discussions.zip"
HANDLER="slack_github_discussions.lambda_handler"
RUNTIME="python3.9"
ROLE_ARN="arn:aws:iam::YOUR_ACCOUNT_ID:role/YOUR_LAMBDA_ROLE"

# Remove old package if exists
rm -f $ZIP_FILE

# Package the code
zip -r $ZIP_FILE .

# Check if the function exists
if aws lambda get-function --function-name $FUNCTION_NAME > /dev/null 2>&1; then
    echo "Updating existing lambda function"
    aws lambda update-function-code --function-name $FUNCTION_NAME --zip-file fileb://$ZIP_FILE
else
    echo "Creating new lambda function"
    aws lambda create-function --function-name $FUNCTION_NAME \
        --zip-file fileb://$ZIP_FILE \
        --handler $HANDLER \
        --runtime $RUNTIME \
        --role $ROLE_ARN
fi

echo "Deployment complete"
