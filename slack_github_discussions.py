import json
import os
import requests
from urllib.parse import parse_qs
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Fetch environment variables
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']
REPO_OWNER = os.environ['REPO_OWNER']
REPO_NAME = os.environ['REPO_NAME']

def lambda_handler(event, context):
    try:
        # Log the incoming event for debugging
        logger.info(f"Received event: {event}")

        # Parse Slack URL-encoded data
        body = parse_qs(event['body'])

        logger.info(f"Parsed body: {body}")

        # Slack URL verification
        if 'challenge' in body:
            return {
                'statusCode': 200,
                'body': body['challenge'][0]
            }

        # Handle slash command "/latest-discussions"
        if 'command' in body and body['command'][0] == '/latest-discussions':
            # Fetch discussions from the repository specified in environment variables
            discussions = get_github_discussions(REPO_OWNER, REPO_NAME)
            message = f"Here are the latest GitHub discussions!\n"
            for discussion in discussions:
                message += f"<{discussion['node']['url']}|{discussion['node']['title']}> - :speech_balloon: {discussion['node']['comments']['totalCount']} comments\n"

            channel_id = body['channel_id'][0]

            post_to_slack(message, channel_id)

            return {
                'statusCode': 200,
                'body': "Your request is being processed."
            }

        logger.warning("Unsupported event type or command not found")
        return {
            'statusCode': 200,
            'body': "Unsupported event type"
        }

    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }

def get_github_discussions(repo_owner, repo_name):
    github_api_url = 'https://api.github.com/graphql'
    
    query = f"""
    {{
      repository(owner: "{repo_owner}", name: "{repo_name}") {{
        discussions(first: 10, states: OPEN) {{
          edges {{
            node {{
              title
              url
              comments {{
                totalCount
              }}
            }}
          }}
        }}
      }}
    }}
    """
    headers = {"Authorization": f"Bearer {os.environ.get('GITHUB_TOKEN')}"}
    response = requests.post(github_api_url, json={'query': query}, headers=headers)

    try:
        discussions = response.json()['data']['repository']['discussions']['edges']
        return discussions
    except KeyError:
        print("GitHub API Response did not contain 'data'. Full response:", response.json())
        return []

def post_to_slack(message, channel_id):
    url = 'https://slack.com/api/chat.postMessage'
    headers = {'Authorization': f"Bearer {SLACK_BOT_TOKEN}"}
    data = {
        'channel': channel_id,
        'text': message
    }
    
    # Send the POST request to Slack
    response = requests.post(url, headers=headers, data=data)
    
    # Log the response from Slack
    logger.info(f"Slack API Response: {response.json()}")
    
    return response
