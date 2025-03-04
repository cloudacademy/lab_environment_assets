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

'''
############################# Task: Custom Metric #############################
    
    Create a counter that is incremented for each call of the make_url function.

    Replace the MagicMock bound to urls_made with a Counter.
    
    The make_url is already configured to increment the counter and include 
    the URL as an attribute. No further changes are required.
    
    REQUIREMENTS
    
    1.) Set the urls_made binding below to a otel Counter with the name: urls.made
        The name of the counter is the only required name / value. 
        The name of the meter and metric description are left to your creativity.
    
    Documentation is available at: 
        
    https://opentelemetry.io/docs/languages/python/getting-started/#metrics
    
###############################################################################
'''
from opentelemetry import metrics

# Edit urls_made to bind to an OTel Counter metric 
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



from opentelemetry import trace
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Setup the TracerProvider which is the main entry to the tracing API.
provider = TracerProvider()

# Set up the exporter that sends the trace data to an OpenTelemetry collector.
# OTLPSpanExporter uses the OpenTelemetry Protocol over HTTP.
processor = BatchSpanProcessor(OTLPSpanExporter())

# The BatchSpanProcessor gathers spans and batches them for efficient sending.
provider.add_span_processor(processor)

# Set the global default TracerProvider. This is a necessary step to make the created Tracer available globally.
trace.set_tracer_provider(provider)

# Get a Tracer instance from the global TracerProvider. This is used to start manual spans.
tracer = trace.get_tracer("profile.tracer")

@app.route('/<int:index>')
def profile(index: int):
    '''
    ############################# Task: Custom Traces #############################
        
        Create nested spans with custom attributes.
    
        EXAMPLE STRUCTURE:
        
        - SPAN: profile
            - Attribute: user_id = index
            
            - SPAN: details
                - Attribute: user_name = user["user"]
                - Attribute: user_data = user["data"]
                
        
        REQUIREMENTS
        
        Use the global tracer created above or create your own.
        
        1.) Edit this function to include a root span named: profile
            a.) Set an attribute named user_id to the value of index.
            
        2.) Create a span named: details that's nested under profile.
            a.) Set an attribute named user_name to the value of user["user"]
            b.) Set an attribute named user_data to the value of user["data"]
            
        3.) Ensure the substance of the function is unchanged.
            - The HTTP request made to the db-service must be called.
            - The HTML content must be returned.
            
        Documentation is available at: 
            
        https://opentelemetry.io/docs/languages/python/instrumentation/#creating-nested-spans
        https://opentelemetry.io/docs/languages/python/instrumentation/#add-attributes-to-a-span
        
    ###############################################################################
    '''
    
    # Call the db-service.
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
