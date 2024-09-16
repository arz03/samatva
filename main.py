import os
import sys
from flask import Flask, render_template
from modules.flashy.flashyweb import app as flashyweb
from django.core.wsgi import get_wsgi_application
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

# Flask app setup for home and flashy
flask_app = Flask(__name__)
flask_app.secret_key = 'samatva'
flask_app.register_blueprint(flashyweb, url_prefix='/flashy')

@flask_app.route('/')
@flask_app.route('/home')
def index():
    return render_template('home2.html')

# Django setup for codenames
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django_app = get_wsgi_application()

# Combine Flask and Django to run website with codenames and flashy
application = DispatcherMiddleware(flask_app, {
    '/codenames': django_app
})

if __name__ == '__main__':
    run_simple('localhost', 5000, application, use_reloader=True, use_debugger=True)