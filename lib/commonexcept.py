# -*- coding: utf-8 -*-

class UserDefExcept(Exception):
    def __init__(self, v_errmsg):
        self.value = v_errmsg