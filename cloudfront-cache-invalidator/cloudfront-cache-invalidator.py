import boto3
import os

from pprint import pprint

client = boto3.client('cloudfront')


def get_distribution():
    response = client.get_distribution(
        Id=os.environ['distribution_id']
    )
    return response

def handler(event, context):
    pprint(get_distribution())
