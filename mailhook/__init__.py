#coding:utf8
from flask import Flask, current_app, render_template, request
from .controllers.APIController import api

app = Flask(__name__, static_url_path='/static')  # 定义/static目录为静态文件目录

app.register_blueprint(api)

@app.route("/")
def index():
    return 'Helloworld'