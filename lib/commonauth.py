# -*- coding: utf-8 -*-

import os
import sys
import pprint
import re
import ldap

import base64
from Crypto.Cipher import AES
from Crypto import Random

import lib.commonhttpcode as httpcode
from lib.commonexcept import UserDefExcept
from lib.commonlog import Log


'''
    class : AESCipher
    description : encrypt or decrypt message using AES algorithm
'''

class AESCipher(object):
    def __init__(self, v_key=None):
        self.s_key = v_key
        self.i_bs = 32

        if self.s_key is None :
            raise UserDefExcept("It must define key")

        if len(self.s_key) % 16 != 0 :
            raise UserDefExcept("AES key size must be either 16, 24, or 32 bytes")

    def encrypt(self, v_raw_message=None):

        if v_raw_message is None:
            raise UserDefExcept("It must provide message")

        s_pad_message = self._pad(v_raw_message)
        s_iv = Random.new().read(AES.block_size)
        o_cipher = AES.new(self.s_key, AES.MODE_CBC, s_iv)

        return base64.b64encode(s_iv + o_cipher.encrypt(s_pad_message))

    def decrypt(self, v_enc_message=None):
        if v_enc_message is None:
            raise UserDefExcept("It must provide encrypted message")

        s_enc_message = base64.b64decode(v_enc_message)
        s_iv = s_enc_message[:AES.block_size]
        o_cipher = AES.new(self.s_key, AES.MODE_CBC, s_iv)

        return self._unpad(o_cipher.decypt(s_enc_message[AES.block_size:])).decode('utf-8')

    def _pad(self, v_block_text):
        return v_block_text + (self.i_bs - len(v_block_text) % self.i_bs) * \
                chr(self.i_bs - len(v_block_text) % self.i_bs)

    def _unpad(self, v_block_text):
        return v_block_text[:-ord(v_block_text[len(v_block_text)-1:])]



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
