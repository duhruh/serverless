# cloudfront-cache-invalidator
Invalidates Cloudfront cache using Lambda via Serverless framework

Deployed to AWS and invoked manually when a cache invalidation for the docs/www/blog distribution is desired.

# Deploy
>sls deploy -v --stage [docs/www/blog]

# Run once-off
>sls invoke -l -f cache-invalidator --stage [docs/www/blog]

# Development
You need Serverless installed:
>npm install -g serverless

When you make any changes, you must deploy them (see above) to take effect.

## cloudfront-cache-invalidator.py
The code that is run. Should be unnecessary to change anything here usually.

## serverless.yaml
Defines the Lambda function, IAM roles, custom variables, etc.

# Triggering a cache invalidation
## docs
`aws lambda invoke --function-name docs-cache-invalidator out.txt`

## www
`aws lambda invoke --function-name www-cache-invalidator out.txt`

## blog
`aws lambda invoke --function-name blog-cache-invalidator out.txt`

`out.txt` is an output file that contains the response from the execution of your Lambda function.

# Notes
Granular IAM permission policies are set up so that each user is only granted permissions to invoke a specific Lambda function.

Each Lambda function is associated with a respective IAM policy. Example IAM policy for the `blog-cache-invalidator` function:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PermissionToInvoke",
            "Effect": "Allow",
            "Action": "lambda:InvokeFunction",
            "Resource": "arn:aws:lambda:us-east-1:710015040892:function:blog-cache-invalidator"
        }
    ]
}
```

# Troubleshooting
1. `AccessDeniedException`
```
AccessDeniedException: User: arn:aws:iam::1221321312:user/cli is not authorized to perform: lambda:InvokeFunction on resource: arn:aws:lambda:us-east-1:710015040892:function:docs-cache-invalidator
```
Why? You do not have the proper permissions to invoke the specific lambda function.

Solution: File a [Jira](https://docker.atlassian.net/projects/IN) ticket for us and we'll get you access asap.

2. `ResourceNotFoundException`
```
An error occurred (ResourceNotFoundException) when calling the Invoke operation: Function not found: arn:aws:lambda:us-east-1:912514925074:function:docs-cache-invalidator
```
Why? You are using an access key ID and secret key from a different AWS account

Solution: You need to use the access key ID and secret key from the `dockerinc` AWS account (710015040892), check your `~/.aws/credentials` file. If you do not have access to this AWS  account, file a [Jira](https://docker.atlassian.net/projects/IN) ticket for us and we'll get you access asap.
