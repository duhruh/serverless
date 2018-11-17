import boto3
import os
import string

from datetime import datetime
from pprint import pprint

client = boto3.client('cloudfront')


def get_distribution():
    response = client.get_distribution(
        Id=os.environ['distribution_id']
    )
    return response

def handler(event, context):
    files = ["/*"]
    dt = datetime.utcnow()
    timestamp = ''.join(str(x) for x in (dt.year, dt.month, dt.day, dt.minute, dt.second))
    #pprint(get_distribution())
    response = client.create_invalidation(
        DistributionId=os.environ['distribution_id'],
        InvalidationBatch={
            'Paths': {
                'Quantity': len(files),
                'Items': ['/*']
            },
            'CallerReference': timestamp
        }
    )
    pprint(response)
