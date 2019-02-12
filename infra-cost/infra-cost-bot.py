import boto3
import json
import logging
import os

from base64 import b64decode
from urllib.parse import parse_qs
from datetime import datetime
from calendar import monthrange
from botocore.vendored import requests


SLACK_TOKEN_KEY = "/infra-cost/slack_token"
PROJECTS_LIST_URL_KEY = "/infra-cost/projects_list_url"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_ssm_param(key,encrypted):
    client = boto3.client('ssm')
    response = client.get_parameter(
        Name=key,
        WithDecryption=encrypted
    )
    return response['Parameter']['Value']


def respond(err, res=None):
    res['response_type'] = "in_channel"
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def validate_project_code(project):
    #TODO accept valid wildcard project name
    project_list_url = get_ssm_param(PROJECTS_LIST_URL_KEY,False)
    project_list = requests.get(project_list_url).text.splitlines()
    return project in project_list


def aws_cost(project, start, end):
    client = boto3.client('ce')
    #TODO accept wildcard in project name
    cost_response = client.get_cost_and_usage(
        TimePeriod={
            'Start': start,
            'End': end
        },
        Granularity='MONTHLY',
        Filter={
            'Tags': {
                'Key': 'project',
                'Values': [
                    project,
                ]
            }
        },
        Metrics=[
            'BlendedCost',
        ],
    )
    cost = str(round(float(cost_response['ResultsByTime'][0]['Total']['BlendedCost']['Amount']),2))
    return cost

def lambda_handler(event, context):
    
    # check for valid token in request from Slack
    params = parse_qs(event['body'])
    expected_token = get_ssm_param(SLACK_TOKEN_KEY,True)
    token = params['token'][0]
    if token != expected_token:
        logger.error("Request token (%s) does not match expected", token)
        return respond(Exception('Invalid request token'))

    # grab params from the request
    user = params['user_name'][0]
    command = params['command'][0]
    channel = params['channel_name'][0]
    project = params['text'][0]

    # validate project code
    if not validate_project_code(project):
        logger.error("Invalid project code: " + project)
        return respond(None, {"text": "Error: Invalid project code"})
    
    # set up start and end dates
    year = datetime.today().year
    month = datetime.today().month
    start = "%s-%02d-01" % (year, month)
    endday = monthrange(year, month)[1]
    end = "%s-%02d-%s" % (year, month, endday)
    
    # issue requests to each infra provider
    aws = aws_cost(project, start, end)
    # TODO GCP
    # TODO Azure
    
    # build and issue the response
    response_text = "Infra costs for project '%s' so far this month:\n AWS: $%s" % (project, aws)
    response = {"text": response_text}
    return respond(None, response)
