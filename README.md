# Testing-Lamnda-AWS
Script aligned with security practices recommended by AWS.

## Check on the following key aspects:

1. 'Least Privilege Principle:' Verify that associated roles have only the necessary permissions.
2. 'Configuration Security:' Ensure that the Lambda function does not have configurations that could compromise security.
3. Security of Environment Variables: Review environment variables to avoid sensitive information.
4. VPC Usage: Validate that the feature is correctly configured to work in a VPC if necessary.
5. IAM Policies: Verify that the policies associated with the roles are secure and do not grant excessive permissions.
