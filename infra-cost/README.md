# Infra Cost Bot

This is a Slack bot using Lambda, API Gateway, and Serverless framework. When you call the bot with a valid project tag, it returns cloud infra costs of resources marked with that tag.

# Contributing

Please open a PR for any improvements and tag the infra team for review. We will review, merge, and deploy.

# Deployment

You need access to the top-level billing account to deploy this. This access is restricted to Infra admins only given the sensitive nature of the account.

`aws-okta exec billing.admin -- sls deploy`
