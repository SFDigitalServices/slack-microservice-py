"""Main application module"""
import os
import json
import jsend
import sentry_sdk
import falcon
from .resources.slack import SlackService
from .resources.welcome import Welcome

def start_service():
    """Start this service
    set SENTRY_DSN environmental variable to enable logging with Sentry
    """
    # Initialize Sentry
    sentry_sdk.init(os.environ.get('SENTRY_DSN'))
    # Initialize Falcon
    api = falcon.API()
    api.add_route('/welcome', Welcome())
    api.add_route('/slack-notification', SlackService())
    return api
