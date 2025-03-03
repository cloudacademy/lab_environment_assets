import os
from collections import namedtuple
from unittest.mock import MagicMock

from flask import (
    Flask, 
    render_template,
    request
)

import requests as req

# WSGI app wrapper
app = Flask(__name__)

db_service = namedtuple('db_service', 'host port'.split())
db_service.host = os.getenv('DB_SERVICE_HOST', 'db_service')
db_service.port = os.getenv('DB_SERVICE_PORT', 9000)

###############################################################################
####### Task: 
#######
####### Create a counter that is incremented for each call of the make_url function.
####### The urls_made variable is currently bound to a mock object that enables 
####### calls to made to disparate methods without raising an exception.
#######
####### REQUIREMENTS 
####### 
####### 1.) Set the urls_made binding below to a otel Counter with the name: urls.made
#######     The description can be set to an empty string. 
#######
####### Documentation is available at: 
####### https://opentelemetry.io/docs/languages/python/getting-started/#metrics
#######
#####################
from opentelemetry import metrics

urls_made = MagicMock()


def make_url(path: str=None):
    path = (path or '').lstrip('/') # Ensure any preceeding slash is removed.
    path = f'http://{db_service.host}:{db_service.port}/{path}'
    # Increment the urls.made counter and include an attribute named url set to the value of the path binding.
    urls_made.add(1, {'url': path})
    return path

@app.route('/')
def index():
    # call the service.
    users = req.get(make_url('/users/')).json()
    users = [f'<li>{user["user"]}</li>' for user in users]
    users = ''.join(users)
    
    return f'''
    <!DOCTYPE html>
    <html lang="en">
        <meta charset="UTF-8">
        <title>Users</title>
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <body>
            <ul>{users}</ul>
        </body>
    </html>
    '''


@app.route('/<int:index>')
def profile(index: int):
    # call the service.
    user = req.get(make_url(f'/users/{index}')).json()
    
    return f'''
        <!DOCTYPE html>
        <html lang="en">
            <meta charset="UTF-8">
            <title>Users</title>
            <meta name="viewport" content="width=device-width,initial-scale=1">
            <body>
                Name: {user["user"]}<br>
                Data: {user["data"]}<br>
            </body>
        </html>
    '''
