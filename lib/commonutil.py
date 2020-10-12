# -*- coding: utf-8 -*-

import datetime


def convert_to_epoch(v_timestamp):
    o_timestamp = v_timestamp.replace(tzinfo=None)
    o_diff = (v_timestamp - datetime(1970,1,1))
    o_seconds = o_diff.total_seconds()

    return o_seconds