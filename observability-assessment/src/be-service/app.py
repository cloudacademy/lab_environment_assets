import os
from collections import namedtuple

from flask import (
    Flask, 
    render_template,
    request
)

import requests as req

# WSGI app wrapper
app = Flask(__name__)

db_service = namedtuple('db_service', ['host', 'port', 'path'])
db_service.host = os.getenv('DB_SERVICE_HOST', 'db_service')
db_service.port = os.getenv('DB_SERVICE_PORT', 9000)

@app.route('/')
def index():
    # call the service.
    users = req.get(f'http://{db_service.host}:{db_service.port}/').json()
    users = [f'<li>{user.name}</li>' for user in users]
    users = '\n'.join(users)
    
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



@app.route('/<index: int>')
def profile(index: int):
    # call the service.
    user = req.get(f'http://{db_service.host}:{db_service.port}/{index}').json()
    
    return f'''
        <!DOCTYPE html>
        <html lang="en">
            <meta charset="UTF-8">
            <title>Users</title>
            <meta name="viewport" content="width=device-width,initial-scale=1">
            <body>
                Name: {user.name}<br>
                Data: {user.data}<br>
            </body>
        </html>
        
        '''
