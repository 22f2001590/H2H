from flask import Flask, jsonify, make_response, request, render_template, session, flash, redirect, url_for, flash
from flask_jwt_extended import JWTManager, get_jwt, get_jwt_identity, verify_jwt_in_request
# from flask_restful import Api, Resource
from datetime import timedelta
from backend.tabels import *
import flask_excel as excel
from flask_cors import CORS
from flask_caching import Cache
from backend.celery.celery_factory import celery_init_app

class Config:
    SQLALCHEMY_DATABASE_URI='sqlite:///h2h.db'
    SQLALCHEMY_TRACK_MODIFICATION=False
    SECRET_KEY='This is very much a scret key of sujay'
    UPLOAD_FOLDER = 'uploads'

    JWT_SECRET_KEY = 'mysupersecretkey'
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=365)
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"

    CACHE_TYPE = 'RedisCache'
    CACHE_DEFAULT_TIMEOUT = 10
    CACHE_REDIS_PORT = 6379

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)
db.init_app(app)
app.cache = Cache(app)
CORS(app, supports_credentials=True)
celery_app = celery_init_app(app)
# api = Api(app)

with app.app_context():
    db.create_all(); setup_data()

from backend.controller.login import *
from backend.controller.admin_actions import *
from backend.controller.customer_actions import *
from backend.controller.professional_actions import *


excel.init_excel(app)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    
    
 