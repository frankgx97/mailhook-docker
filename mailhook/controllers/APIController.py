#coding:utf8
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, jsonify
from sender import Mail, Message
import json
import logging
from mailhook.config import config

api = Blueprint('api', __name__)

@api.route("/<srv_name>",methods=['POST'])
def send_mail(srv_name):
    '''发送邮件'''
    data = request.get_json()
    if srv_name not in config:
        return jsonify({"status":1, "msg":"InvalidService"})
    else:
        srv_config = config[srv_name]
    if not verify_key(srv_name, data['key']):
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
        logging.info(data['mail_title'])
        logging.info(data['mail_to'])
        logging.info(data['mail_html'])
        mail.send(mail_msg)
        return jsonify({"status":0, "msg":"Success"})
    except Exception, e:
        return jsonify({"status":2, "msg":e})

def verify_key(srv, key):
    if config[srv]['key'] == key:
        return True
    else:
        return False
