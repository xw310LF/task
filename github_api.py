#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import requests
import sys

GITHUB_API = {
    #URL_BASE
    'URL_BASE': 'https://api.github.com/repos/',
    # authorization
    'REQUEST_HEADER': {'Authorization': 'token 1855dee3c9ada36d773e17a1918b75826eadcf2b'},
    # URL_ISSUES_LIST
    'URL_ISSUES': 'https://api.github.com/repos/xw310/Test/issues',
    # URL_PULLS_LIST
    'URL_PULLS': 'https://api.github.com/repos/xw310/Test/pulls',
    # URL_LABELS_LIST
    'URL_LABELS': 'https://api.github.com/repos/xw310/Test/labels'
}

DURATION_MAP = {
    'TWO_WEEK': 3,
    'THREE_WEEK': 4,
    'FINAL_DAY': 5
}

TWO_WEEK_LABEL = {
    #TWO_WEEK_LABEL & comment
    'NAME': 'open 2 weeks ago',
    'DESCRIPTION': 'open for two weeks',
    'COLOR': 'c0ff93',

    'COMMENT_TEMPLATE': 'The pull request {} has been open for two weeks,  \
                        please deal with it ASAP by following link:\n {}'
}

THREE_WEEK_LABEL = {
    #THREE_WEEK_LABEL & comment
    'NAME': 'open 3 weeks ago',
    'DESCRIPTION': 'open for three weeks, will be deleted',
    'COLOR': 'a2e06b',

    'COMMENT_TEMPLATE': 'The pull request {} has been open for three weeks, \
                        it will be closed tomorrow. Sorry for the convenience. \
                        please deal with it ASAP by following link:\n {}',

    'COMMENT_TEMPLATE_UNDER_IGONRE': 'The pull request {} has been open for three weeks.\
                                    please deal with it ASAP by following link:\n {}\n \
                                    This pull request was added a ignore_label, so it will \
                                    not be closed. If you want to close it, you can either \
                                    manually close it or remove the ignore_label of it (This \
                                    pull request will be closed when it reaches deleting time.'
}

IGNORE_LABEL = {
    #IGNORE_label
    'NAME': 'ignore auto close',
    'DESCRIPTION': 'ingore this label ',
    'COLOR': 'f4f954',
}


def print_time():
    print(datetime.utcnow().strftime( '%Y-%m-%dT%H:%M:%SZ' ))    #type string


def create_new_label(name, description, color):
    '''
    creat new label according to flag value
    '''

    request_body = {
        "name": name,
        "description": description,
        "color": color
    }
    try:
        response = requests.post(url=GITHUB_API['URL_LABELS'], json=request_body, headers=GITHUB_API['REQUEST_HEADER'])
        if response.status_code != 201:
            print(f'creating {name} label exit with status code {response.status_code}\n')
            sys.exit(1)
    except requests.exceptions.RequestException as error:
        ####
        # add monitor here
        ####
        print(f'creating {name} label fails due to exception. rerun or add it manually\n')
        print(error, '\n')
        sys.exit(1)


def get_all_labels():
    '''
    get all existing labels
    '''
    try:
        response = requests.get(url=GITHUB_API['URL_LABELS'], headers=GITHUB_API['REQUEST_HEADER'])
        if response.status_code != 200:
            print(f'getting all labels exit with status code {response.status_code}\n')
            sys.exit(1)
        return response.json()

    except requests.exceptions.RequestException as error:
        print(f'getting all labels fails due to exception. rerun it\n')
        print(error, '\n')
        sys.exit(1)


def get_all_issues():
    '''
    get all open issues
    '''
    try:
        response = requests.get(url=GITHUB_API['URL_ISSUES'], headers=GITHUB_API['REQUEST_HEADER'])
        if response.status_code != 200:
            print(f'getting all issues exit with status code {response.status_code}\n')
            sys.exit(1)
        return response.json()
    except requests.exceptions.RequestException as error:
        print(f'getting all issues fails due to exception\n')
        print(error, '\n')


def add_label_to_issue(name, issue_number):
    '''
    add a label to an issue according to flag value
    '''

    url_issue_label = url_issue_label = '{}/{}/labels'.format(GITHUB_API['URL_ISSUES'], issue_number)

    request_body = {
        "labels": [name]
    }

    try:
        response = requests.post(url=url_issue_label, json=request_body, headers=GITHUB_API['REQUEST_HEADER'])
        if response.status_code != 200:
            print(f'adding label to issue exit with status code {response.status_code}\n')
            sys.exit(1)
    except requests.exceptions.RequestException as error:
        print(f'adding {name} label to issue {issue_number} fails due to exception\n')
        print(error, '\n')


def add_comment_to_issue(comment, issue_number, issue_title, html_url):
    '''
    add a comment to an issue according to flag value
    '''

    url_issue_comment = '{}/{}/comments'.format(GITHUB_API['URL_ISSUES'], issue_number)

    body = comment.format(issue_title, html_url)
    request_body = {
        "body": body
    }

    try:
        response = requests.post(url=url_issue_comment, json=request_body, headers=GITHUB_API['REQUEST_HEADER'])
        if response.status_code != 201:
            print(f'adding comment to issue exit with status code {response.status_code}\n')
            sys.exit(1)
    except requests.exceptions.RequestException as error:
        print(f'adding a comment to issue {issue_number} fails due to exception\n')
        print(error, '\n')


def delete_label_from_issue(name, issue_number):
    '''
    delete two_weeks_already label before adding three_weeks_already label
    '''

    url_issue_label_delete = '{}/{}/labels/{}'.format(GITHUB_API['URL_ISSUES'], issue_number, name)

    try:
        response = requests.delete(url=url_issue_label_delete, headers=GITHUB_API['REQUEST_HEADER'])
        if response.status_code != 200:
            print(f'deleting label exit with status code {response.status_code}\n')
            sys.exit(1)
    except requests.exceptions.RequestException as error:
        print(f'deleting {name} label from issue {issue_number} fails due to exception\n')
        print(error, '\n')


def close_pr(issue_number):
    '''
    close expired pr
    '''
    url_pr_close = '{}/{}'.format(GITHUB_API['URL_PULLS'], issue_number)

    request_body = {
        "state": "closed"
    }

    try:
        re = requests.patch(url=url_pr_close, json=request_body, headers=GITHUB_API['REQUEST_HEADER'])
        if re.status_code != 200:
            print(f'closing pr {issue_number} exit with status code {re.status_code}\n')
            sys.exit(1)
    except requests.exceptions.RequestException as error:
        print(f'closing pull request {issue_number} fails due to exception\n')
        print(error, '\n')
