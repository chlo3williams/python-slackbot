import unittest
import json
import os
from unittest.mock import patch, MagicMock

os.environ["SLACK_BOT_TOKEN"] = "slack-token"
os.environ["GITHUB_TOKEN"] = "github-token"
os.environ["SLACK_CHANNEL"] = "C123456"
os.environ["REPO_OWNER"] = "owner"
os.environ["REPO_NAME"] = "repo"

from slack_github_discussions import lambda_handler

class TestLambdaFunction(unittest.TestCase):

    @patch("slack_github_discussions.requests.post")  # Mock API request
    def test_lambda_handler_success(self, mock_post):
        """Test the lambda function with a valid Slack event."""

        # Mock GitHub API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "repository": {
                    "discussions": {
                        "edges": [
                            {"node": {"title": "Test Discussion", "url": "https://github.com/test", "comments": {"totalCount": 5}}}
                        ]
                    }
                }
            }
        }
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        event = {
            "body": "command=/latest-discussions&channel_id=C123456"
        }
        response = lambda_handler(event, {})

        self.assertEqual(response["statusCode"], 200)
        self.assertIn("Your request is being processed.", response["body"])
    
    @patch("slack_github_discussions.requests.post")  # Mock API request
    def test_lambda_handler_invalid_event(self, mock_post):
        """Test the lambda function with an invalid event."""
        event = {"body": "invalid_data"}
        response = lambda_handler(event, {})

        self.assertEqual(response["statusCode"], 200)
        self.assertIn("Unsupported event type", response["body"])
    
    @patch("slack_github_discussions.requests.post")  # Mock API request
    def test_lambda_handler_exception(self, mock_post):
        """Test error handling in lambda function."""
        
        # Simulate GitHub API returning an error
        mock_response = MagicMock()
        mock_response.json.return_value = {"message": "Bad credentials"}
        mock_response.status_code = 401
        mock_post.return_value = mock_response

        event = {""}  
        response = lambda_handler(event, {})

        self.assertEqual(response["statusCode"], 500)
        self.assertIn("Error", response["body"])
  
if __name__ == "__main__":
    unittest.main()