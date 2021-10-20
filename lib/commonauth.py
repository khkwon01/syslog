# -*- coding: utf-8 -*-

import os
import sys
import pprint
import re
import ldap

import base64
from cryptography.fernet import Fernet

import lib.commonhttpcode as httpcode
from lib.commonexcept import UserDefExcept
from lib.commonlog import Log


'''
    class : AESCipher
    description : encrypt or decrypt message using AES algorithm
    refer url : https://cryptography.io/
'''
class AESCipher(object):
    def __init__(self, v_key=None):
        self.s_key = v_key
        self.i_bs = 32

        if self.s_key is None:
            self.s_key = Fernet.generate_key()
            print(f'key : { self.s_key }')

        self.o_crypto = Fernet(self.s_key)

    def encrypt(self, v_raw_message=None):

        if v_raw_message is None:
            raise UserDefExcept("It must provide message")

        s_enc_message = self.o_crypto.encrypt(v_raw_message.encode("utf8"))

        return base64.b64encode(s_enc_message)


    def decrypt(self, v_enc_message=None):
        if v_enc_message is None:
            raise UserDefExcept("It must provide encrypted message")

        s_dec_message = base64.b64decode(v_enc_message)
        s_dec_message = self.o_crypto.decrypt(s_dec_message)

        return s_dec_message


'''
    class : Authldap
    descritpion : authenticate ldap user
'''
class Authldap:
    def __init__(self, v_logger, v_ldapurl, v_ldapbase=None, v_referrals=0, v_protocol_ver=ldap.VERSION3):
        self.o_logger = v_logger
        self.o_ldapsess = None
        self.s_ldapurl = v_ldapurl
        self.s_basedn = v_ldapbase
        self.i_referrals = v_referrals
        self.i_protocol_ver = v_protocol_ver

    def _ldapinit(self):
        self.o_ldapsess = ldap.initialize(self.s_ldapurl)
        self.o_ldapsess.set_option(ldap.OPT_REFERRALS, self.i_referrals)
        self.o_ldapsess.set_option(ldap.OPT_PROTOCOL_VERSION, self.i_protocol_ver)

    def auth_user(self, v_username=None, v_password=None):
        o_result = None

        self._ldapinit()

        if v_username is None:
            self.o_logger.write_log(Log.ERROR, "Ldap user id is null")
            raise UserDefExcept("It must define username for ldap")

        if v_password is None:
            self.o_logger.write_log(Log.ERROR, "Ldap user pass is null")
            raise UserDefExcept("It must define user password for ldap")

        try:
            o_result = self.o_ldapsess.simple_bind_s(v_username, v_password)
            o_result = self.o_ldapsess.search_s(self.s_basedn, ldap.SCOPE_SUBTREE,
                                                "userPrincipalName=" + v_username, ['memberOf'])
            o_result = o_result[0][0].decode('utf-8')
        except ldap.INVALID_CREDENTIALS as e:
            o_result = httpcode.HTTP_401_UNAUTHORIZED
            self.o_logger.write_log(Log.ERROR, "Ldap user auth failed : " + e.message['desc'])
        except ldap.SERVER_DOWN as e:
            o_result = httpcode.HTTP_500_INTERNAL_SERVER_ERROR
            self.o_logger.write_log(Log.ERROR, "Ldap server is down : " + e.message['desc'])
        except ldap.LDAPError as e:
            o_result = httpcode.HTTP_500_INTERNAL_SERVER_ERROR
            self.o_logger.write_log(Log.ERROR, "Ldap user auth failed : " + e.message['desc'])
        finally:
            if self.o_ldapsess is not None:
                self.o_ldapsess.ubind_s()

        return o_result


if __name__ == '__main__':
    o_auth = AESCipher('gl1rdnaieUBMI6B1ypTmSgPLWcr3CJgvmIPmM4hy86k=')

    s_enctext = o_auth.encrypt("무엇을 해야할지 생각 좀 해 봐야겠어요. 갈데가 없네요.")
    print(s_enctext)

    s_dectext = o_auth.decrypt(s_enctext)
    print(s_dectext.decode('utf8'))