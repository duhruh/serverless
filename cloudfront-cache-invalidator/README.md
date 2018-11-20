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
