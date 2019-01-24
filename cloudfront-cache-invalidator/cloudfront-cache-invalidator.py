import boto3
import os
import sys
import json
import logging

from datetime import datetime
from pprint import pformat


logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
					datefmt='%Y-%m-%d %H:%M:%S',
					stream=sys.stdout,
					level=logging.DEBUG)
logger = logging.getLogger('cloudfront-cache-invalidator.py')

client = boto3.client('cloudfront')


def handler(event, context):
    files = ["/*"]
    dt = datetime.utcnow()
    timestamp = ''.join(str(x) for x in (dt.year, dt.month, dt.day, dt.minute, dt.second))

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
    logger.debug(pformat(response))
    return json.dumps(response, indent=4, default=str)
