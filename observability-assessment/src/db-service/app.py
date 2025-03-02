from flask import (
    Flask, 
    render_template,
    request
)

# WSGI app wrapper
app = Flask(__name__)


USERS = [
    {
        'user': 'a',
        'data': ':)'
    },
    {
        'user': 'b',
        'data': ':)'
    },
    {
        'user': 'c',
        'data': ':)'
    },
    {
        'user': 'd',
        'data': ':)'
    },
    {
        'user': 'e',
        'data': ':)'
    },
    {
        'user': 'f',
        'data': ':)'
    },
    {
        'user': 'g',
        'data': ':)'
    },
    {
        'user': 'h',
        'data': ':)'
    },
    
]

# Simple route returing hardcoded JSON data. (Flask handles jsonifying it.)
@app.route('/users/')
def users():
    return USERS


@app.route('/users/<int:index>')
def user(index: int):
    return USERS[index]
    
