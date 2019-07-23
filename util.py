#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from github_api import *

def get_target_label(labels):
    '''
    get the target label
    '''
    target_label = []
    for label in labels:
        if label['name'] == TWO_WEEK_LABEL['NAME'] or label['name'] == THREE_WEEK_LABEL['NAME'] or \
        label['name'] == IGNORE_LABEL['NAME']:

            target_label.append(label['name'])

    return target_label


def calculate_pr_duration(create_time):
    '''
    calculate the duration of a pr
    '''

    year = int(create_time[:4])
    month = int(create_time[5:7])
    day = int(create_time[8:10])
    hour = int(create_time[11:13])
    duration_in_day = (datetime.utcnow() - datetime(year, month, day, hour)).days

    return duration_in_day*2+1
