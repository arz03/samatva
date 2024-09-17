import os
import sys
from flask import Flask, render_template, request, jsonify
from modules.flashy.flashyweb import app as flashyweb
from modules.scenario.scenario import app as scenario
from django.core.wsgi import get_wsgi_application
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from PyCAI2 import PyAsyncCAI2
import asyncio


# Flask app setup for home and flashy
flask_app = Flask(__name__)
flask_app.secret_key = 'samatva'
flask_app.register_blueprint(flashyweb, url_prefix='/flashy')
flask_app.register_blueprint(scenario, url_prefix='/')

@flask_app.route('/')
@flask_app.route('/home')
def index():
    return render_template('home2.html')

# Django setup for codenames
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django_app = get_wsgi_application()

owner_id = 'ab0ee290e9090a3b4e2ef9c58cd54473d4ad8f26'
client = PyAsyncCAI2(owner_id)

@flask_app.route('/chatbot/')
def chatbot_index():
    return render_template('chatbot_index.html')

@flask_app.route('/chatbot/send_message', methods=['POST'])
async def send_message():
    data = request.get_json()
    user_message = data['message']
    print(user_message)
    async with client.connect(owner_id) as chat2:
        system_reply = await chat2.send_message(char='T_Vj_8U9w851RUcjdqwcQ7Zf0c6PANNH63JGk7Sik1I', text=user_message, author_name="user")
    return jsonify({'reply': system_reply})

# Combine Flask and Django to run website with codenames and flashy
application = DispatcherMiddleware(flask_app, {
    '/codenames': django_app
})

if __name__ == '__main__':
    run_simple('localhost', 5000, application, use_reloader=False, use_debugger=False)