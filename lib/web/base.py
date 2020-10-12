# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, abort, request, current_app, session, url_for, flash, g
from jinja2 import TemplateNotFound
from flask_mail import Mail, Message
from flask import jsonify
from functools import wraps
from flask_httpauth import HTTPBasicAuth
from flask_ldapconn import LDAPConn
from ldap3 import SUBTREE
import lib.commonhttpcode as  http_status


""" register blueprint (define: static_folder,static_url_path,template_folder,url_prefix etc) """
base = Blueprint('base', __name__, template_folder='templates', static_folder='static')


""" defin httpauth object """
auth = HTTPBasicAuth()

@base.route('/')
@auth.login_required
def login():
    i_code = http_status.HTTP_200_OK
    s_desc = "/ access is test ok..."
    o_ldap = None

    with current_app.app_context():
        o_ldap = LDAPConn(current_app)

    print(o_ldap)

    return jsonify(code=i_code, desc=s_desc)

@auth.verify_password
def authorized_user(v_userid, v_passwd):
    b_retval = False

    print("userid : " + v_userid)
    print("userpass : " + v_passwd)

    if v_userid == 'test' and v_passwd == 'test1234' :
        b_retval = True

    return b_retval
