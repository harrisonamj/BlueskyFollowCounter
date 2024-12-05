# Bluesky Follower Counter Lambda Function

Simple serverless solution for tracking Bluesky follower counts and updating them in a GitHub-hosted CSV file.

## Description

This AWS Lambda function fetches the daily follower count of a specified Bluesky user and appends it to a CSV file in a GitHub repository. The function runs automatically at a scheduled time and integrates with the Bluesky API and GitHub.

## Getting Started

### Dependencies

* AWS CLI installed and configured.
* Python installed (version 3.7 or higher).
* GitHub Personal Access Token with `Contents` permission for public repositories or `repo` for private repositories.
* An AWS account with permissions to create Lambda functions and EventBridge rules.

### Installing

1. Create a deployment package:
   ```bash
   mkdir lambda-package
   cd lambda-package
   pip install requests -t .
   cp /path/to/your/lambda_function.py .
   zip -r lambda_function.zip .
   ```
2. Deploy the Lambda function:
   - Open the [AWS Lambda Console](https://console.aws.amazon.com/lambda/).
   - Create or select a Lambda function.
   - Upload the `lambda_function.zip` package.

3. Update the script with your configuration:
   - Edit the script to include your GitHub settings directly:
     ```python
     GITHUB_TOKEN = "your_github_personal_access_token"
     GITHUB_REPO = "your_github_username/your_repo_name"
     GITHUB_FILE_PATH = "path/to/follower_count_log.csv"
     GITHUB_BRANCH = "main"
     BLUESKY_HANDLE = "harrisonamj.com"
     ```

### Executing Program

1. Test the Lambda function:
   - Go to your Lambda function in the AWS Management Console.
   - Click **Test** and create a test event (use the default configuration).
   - Verify that the function executes without errors.

2. Schedule the function:
   - Open the [Amazon EventBridge Console](https://console.aws.amazon.com/events/).
   - Create a new rule with the following cron expression for 23:30 UTC:
     ```
     30 23 * * ? *
     ```
   - Add the Lambda function as the target and save the rule.

## Help

### Common Issues

- **`No module named 'requests'` Error:** Ensure the `requests` library is included in the deployment package.
- **File Not Updated in GitHub:** Verify that the GitHub settings in your script are correct.
- **Trigger Not Executing:** Ensure the EventBridge rule is enabled and correctly configured.

## Authors

Adam Harrison
[@harrisonamj](https://github.com/harrisonamj)

## Version History

* 0.2
    * Improved error handling
    * Documentation updates
* 0.1
    * Initial release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

## Acknowledgments

* [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
* [Bluesky API Documentation](https://docs.bsky.app/)
* [GitHub REST API Documentation](https://docs.github.com/en/rest)

