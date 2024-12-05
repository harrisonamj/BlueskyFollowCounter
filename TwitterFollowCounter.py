import json
import requests
import datetime
import base64

# Settings
GITHUB_TOKEN = "your_github_personal_access_token"
GITHUB_REPO = "your_github_username/your_repo_name"
GITHUB_FILE_PATH = "path/to/follower_count_log.csv"
GITHUB_BRANCH = "main"  # Replace with your branch name
TWITTER_BEARER_TOKEN = "your_twitter_bearer_token"
TWITTER_USERNAME = "username"  # Replace with the Twitter username

API_URL = f"https://api.twitter.com/2/users/by/username/{TWITTER_USERNAME}?user.fields=public_metrics"

def lambda_handler(event, context):
    try:
        # Get the current date
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Fetch follower count from Twitter API
        headers = {
            "Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"
        }
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()
        data = response.json()
        follower_count = data["data"]["public_metrics"]["followers_count"]
        
        # Prepare the new CSV row
        csv_row = f"{current_date},{follower_count}\n"
        
        # Fetch the existing file content from GitHub
        file_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        file_response = requests.get(file_url, headers=headers)
        
        # Check if the file exists
        if file_response.status_code == 200:
            file_data = file_response.json()
            existing_content = base64.b64decode(file_data["content"]).decode("utf-8")
            sha = file_data["sha"]
        elif file_response.status_code == 404:
            # If the file does not exist, initialize with a header row
            existing_content = "Date,Follower Count\n"
            sha = None
        else:
            file_response.raise_for_status()
        
        # Append the new row to the existing content
        updated_content = existing_content + csv_row
        
        # Update the file on GitHub
        update_data = {
            "message": f"Update follower count on {current_date}",
            "content": base64.b64encode(updated_content.encode("utf-8")).decode("utf-8"),
            "sha": sha,
            "branch": GITHUB_BRANCH
        }
        update_response = requests.put(file_url, headers=headers, data=json.dumps(update_data))
        update_response.raise_for_status()
        
        return {
            "statusCode": 200,
            "body": f"Appended: {csv_row.strip()}"
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }
