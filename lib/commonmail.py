#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import smtplib
import email.utils
import mimetypes
import email
from email import encoders
import getpass
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import decode_header
import smtpd
import asyncore
import pprint
import re
import base64

from numpy.compat import unicode

from lib.commonexcept import UserDefExcept
from lib.commonlog import Log

from lib.commonnoti import JandiNoti, Noti

'''
   class : CustomEmail
   description : send email to smtp server
'''


class CustomEmail:

    def __init__(self, v_logger, v_server=None, v_port=25):
        self.o_logger = v_logger
        self.s_server = v_server
        self.i_port = v_port
        self.o_msg = None

    def set_mail_header(self, v_touser, v_fromuser, v_subject):

        self.s_touser = v_touser
        self.s_fromuser = v_fromuser

        self.o_msg = MIMEMultipart()

        self.o_msg['To'] = email.utils.formataddr(('Recipient', v_touser))
        self.o_msg['From'] = email.utils.formataddr(('System', v_fromuser))
        self.o_msg['Subject'] = v_subject

    def set_mail_body(self, v_type='plain', v_content=""):

        if (v_type != 'plain') and (v_type != 'html'):
            self.o_logger.write_Log(Log.ERROR, "mail body must be text or html")
            raise UserDefExcept("mail body must be text or html")

        o_msgpart = MIMEText(v_content, v_type, 'utf-8')
        self.o_msg.attach(o_msgpart)

    def set_mail_attach(self, v_filedir=None, v_maintype='application/octet-stream'):

        s_maintype = None
        s_subtype = None
        s_filename = None
        o_msgpart = None

        if v_filedir == None:
            self.o_logger.write_Log(Log.INFO, "mail attach file is None")
            return

        if not os.path.exists(v_filedir):
            self.o_logger.write_Log(Log.INFO, "mail attach file is not exist")
            return

        s_filename = os.path.basename(v_filedir)
        s_type, s_encoding = mimetypes.guess_type(v_filedir)

        if s_type is None or s_encoding is not None:
            s_type = v_maintype  # setting default value

        s_maintype, s_subtype = s_type.split('/', 1)

        if s_maintype == 'text':
            o_fp = open(v_filedir)
            o_msgpart = MIMEText(o_fp.read(), _subtype=s_subtype)
            o_fp.close()

        elif s_maintype == 'image':
            o_fp = open(v_filedir, 'rb')
            o_msgpart = MIMEImage(o_fp.read(), _subtype=s_subtype)
            o_fp.close()

        elif s_maintype == 'audio':
            o_fp = open(v_filedir, 'rb')
            o_msgpart = MIMEAudio(o_fp.read(), _subtype=s_subtype)
            o_fp.close()

        else:
            o_fp = open(v_filedir, 'rb')
            o_msgpart = MIMEBase(s_maintype, s_subtype)
            o_msgpart.set_payload(o_fp.read())
            o_fp.close()

            encoders.encode_base64(o_msgpart)

        o_msgpart.add_header('Content-Disposition', 'attachment', filename=s_filename)

        self.o_msg.attach(o_msgpart)

    def send_mail(self, v_server=None, v_port=25):

        if v_server != None:
            self.s_server = v_server
            self.i_port = v_port

        if self.o_msg == None:
            self.o_logger.write_Log(Log.ERR, "mail header must be define")
            return

        o_mailserver = smtplib.SMTP(self.s_server, self.i_port)

        try:
            o_mailserver.sendmail(self.s_fromuser, self.s_touser, self.o_msg.as_string())
        except Exception as e:
            self.o_logger.write_Log(Log.ERR, "mail sending error : " + str(e))
        finally:
            o_mailserver.quit()
            self.o_msg = None


class CustomSMTPServer(smtpd.PureProxy):

    def set_env(self, v_logger, v_notichanl, v_notiuser):
        self.__o_Logger = v_logger
        self.__o_Slack = None
        self.__o_NtUr = v_notiuser
        self.__o_NtCl = v_notichanl
        self.__o_Jandi = None

        if v_notichanl.get("slack") != None:
            #self.__o_Slack = SlackNoti(v_logger)
            self.__o_Slack.add_token(v_notichanl['slack'])

        if len(v_notichanl.get("jandi")) > 0:
            self.__o_Jandi = JandiNoti(v_logger)
            self.__o_Jandi.add_channels(v_notichanl.get("jandi"))

        self.__o_Logger.write_Log(Log.DEBUG, pprint.saferepr(self.__o_Slack))
        self.__o_Logger.write_Log(Log.DEBUG, pprint.saferepr(v_notiuser))

    def process_message(self, v_peer, v_mailfrom, v_rcpttos, v_data):
        o_matchobj1 = None

        self.__o_Logger.write_Log(Log.DEBUG, "===== new mail info =====")
        self.__o_Logger.write_Log(Log.DEBUG, "peer : " + pprint.saferepr(v_peer))
        self.__o_Logger.write_Log(Log.DEBUG, "from : " + pprint.saferepr(v_mailfrom))
        self.__o_Logger.write_Log(Log.DEBUG, "to : " + pprint.saferepr(v_rcpttos))
        self.__o_Logger.write_Log(Log.DEBUG, "to type : " + pprint.saferepr(type(v_rcpttos)))
        self.__o_Logger.write_Log(Log.DEBUG, "data :\n" + v_data)

        for s_key, s_value in self.__o_NtUr.items():
            o_matchobj1 = re.findall(s_key, v_data, re.M | re.I)
            self.__o_Logger.write_Log(Log.DEBUG, "matching count : " + str(len(o_matchobj1)))

            if (len(o_matchobj1) >= 1 or s_key == "administatornoti"):
                #                                for s_info in o_value :
                #                                s_mail, s_notichnl = s_info.split(",")
                s_notichnl = s_key
                s_mail = s_value
                self.__o_Logger.write_Log(Log.DEBUG, "mail address : " + s_mail)
                self.__o_Logger.write_Log(Log.DEBUG, "noti chanl : " + s_notichnl)

                v_rcpttos.append(s_mail)

                s_MsgAll = email.message_from_string(v_data)
                s_Charset = s_MsgAll.get_content_charset()
                s_Header = decode_header(s_MsgAll.get('Subject', ''))
                s_Subj = unicode(s_Header[0][0], str(s_Charset), 'ignore').encode('utf8', 'replace')
                s_BodyMsg = unicode(s_MsgAll.get_payload(decode=True), str(s_Charset), 'ignore').encode('utf8',
                                                                                                        'replace')

                if self.__o_Slack != None and \
                        (s_notichnl.startswith('@') or s_notichnl.startswith('#')):
                    self.__o_Slack.send_noti(s_notichnl, "[" + s_Subj + "]\n" + s_BodyMsg, v_notiuser="ocbot")

                elif self.__o_Jandi != None:
                    self.__o_Jandi.send_noti(s_notichnl, "[" + s_Subj + "]\\n" + s_BodyMsg)

        smtpd.PureProxy.process_message(self, v_peer, v_mailfrom, v_rcpttos, v_data)