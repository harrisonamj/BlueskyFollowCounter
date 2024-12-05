import json
import requests
import datetime
import base64

# GitHub settings
GITHUB_TOKEN = "your_github_personal_access_token"
GITHUB_REPO = "your_github_username/your_repo_name"
GITHUB_FILE_PATH = "path/to/follower_count_log.txt"
GITHUB_BRANCH = "main"  # Replace with your branch name

API_URL = "https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor=harrisonamj.com"

def lambda_handler(event, context):
    try:
        # Get the current date
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Fetch follower count from API
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        follower_count = data.get("followersCount", "Unknown")
        log_entry = f"{current_date} - {follower_count}\n"
        
        # Fetch the existing file content from GitHub
        file_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        file_response = requests.get(file_url, headers=headers)
        file_response.raise_for_status()
        file_data = file_response.json()
        
        # Decode the existing file content
        if "content" in file_data:
            existing_content = base64.b64decode(file_data["content"]).decode("utf-8")
        else:
            existing_content = ""
        
        # Append the new log entry
        updated_content = existing_content + log_entry
        
        # Update the file on GitHub
        update_data = {
            "message": f"Update follower count on {current_date}",
            "content": base64.b64encode(updated_content.encode("utf-8")).decode("utf-8"),
            "sha": file_data["sha"],
            "branch": GITHUB_BRANCH
        }
        update_response = requests.put(file_url, headers=headers, data=json.dumps(update_data))
        update_response.raise_for_status()
        
        return {
            "statusCode": 200,
            "body": f"Appended: {log_entry}"
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }
