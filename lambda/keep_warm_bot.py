"""
Keeps other lambdas nice and toasty
"""

import os
import requests


def lambda_handler(event, context):
    """
    Entry point for this lambda
    """
    requests.get(os.environ.get("URL"))
