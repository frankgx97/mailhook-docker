#coding:utf8
import datetime
import json
import logging

from flask import (Blueprint, flash, g, jsonify, redirect, render_template,
                   request, session, url_for)
from sender import Mail, Message

from mailhook.config import config

logging.basicConfig(filename="mailhook.log", level=logging.INFO)

api = Blueprint('api', __name__)

@api.route("/<srv_name>",methods=['POST'])
def send_mail(srv_name):
    '''发送邮件'''
    data = request.get_json()
    if srv_name not in config:
        logging.warning('!!!'+str(datetime.datetime.now())+'InvalidService!!!')
        return jsonify({"status":1, "msg":"InvalidService"})
    else:
        srv_config = config[srv_name]
    if not verify_key(srv_name, data['key']):
        logging.warning('!!!'+str(datetime.datetime.now())+'InvalidKey!!!')
        return jsonify({"status":1, "msg":"InvalidKey"})

    mail_msg = Message(data['mail_title'], fromaddr=srv_config['mail_from'], to=data['mail_to'])
    mail_msg.html = data['mail_html']
    mail = Mail(
        srv_config['smtp'],
        port=srv_config['port'],
        username=srv_config['mail_from'],
        password=srv_config['smtppass'],
        use_tls=srv_config['tls'],
        use_ssl=srv_config['ssl'],
        debug_level=None
        )
    try:
        logging.info('--------'+str(datetime.datetime.now())+'--------------')
        logging.info(data['mail_title'])
        logging.info(data['mail_to'])
        logging.info(data['mail_html'])
        logging.info('=======================================================')
        mail.send(mail_msg)
        return jsonify({"status":0, "msg":"Success"})
    except Exception as e:
        logging.warning('!!!'+str(datetime.datetime.now())+'!!!')
        logging.warning(str(e))
        return jsonify({"status":2, "msg":str(e)})

def verify_key(srv, key):
    if config[srv]['key'] == key:
        return True
    else:
        return False
