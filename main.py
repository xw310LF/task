#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
tast target:
1.At end of two weeks: inform pull request owners/reviewers that pull request has been open for two weeks
2.At end of three weeks: inform that pull request will be closed next day
3.Close expired pull request
'''

import time
from github_api import *
from util import *

def PR_helper():
    '''
    main process
    '''
    print('enter main process\n')

    # get issues
    all_issues = get_all_issues()

    for issue in all_issues:
        if 'pull_request' in issue:
            create_time = issue['created_at']
            issue_number = issue['number']
            issue_title = issue['title']
            html_url = issue['html_url']
            print('processing pull request {}, which is created at {}'.format(issue_number, create_time))

            # check time
            duration_in_day = calculate_pr_duration(create_time)
            # check existing labels
            labels = issue['labels']
            target_label = get_target_label(labels)
            print('duration of this pull request is: {} days'.format(duration_in_day))
            print('target label of this pull request: {}'.format(target_label))

            if IGNORE_LABEL['NAME'] in target_label:
                print('{} label found, skip pull request {}\n'.format(IGNORE_LABEL['NAME'], issue_number))
                continue

            if TWO_WEEK_LABEL['NAME'] not in target_label \
                and THREE_WEEK_LABEL['NAME'] not in target_label \
                and duration_in_day >= DURATION_MAP['TWO_WEEK']:

                add_label_to_issue(TWO_WEEK_LABEL['NAME'], issue_number)
                add_comment_to_issue(TWO_WEEK_LABEL['COMMENT_TEMPLATE'], issue_number, issue_title, html_url)
                print('{} label is added to pull request {}\n'.format(TWO_WEEK_LABEL['NAME'], issue_number))

            else:
                if TWO_WEEK_LABEL['NAME'] in target_label and duration_in_day >= DURATION_MAP['THREE_WEEK']:
                    delete_label_from_issue(TWO_WEEK_LABEL['NAME'], issue_number)
                    add_label_to_issue(THREE_WEEK_LABEL['NAME'], issue_number)
                    add_comment_to_issue(THREE_WEEK_LABEL['COMMENT_TEMPLATE'], issue_number, issue_title, html_url)
                    print('{} label is added to pull request {}\n'.format(THREE_WEEK_LABEL['NAME'], issue_number))

                elif THREE_WEEK_LABEL['NAME'] in target_label and duration_in_day >= DURATION_MAP['FINAL_DAY']:
                    close_pr(issue_number)
                    print('pull request {} is closed\n'.format(issue_number))

                else:
                    print('no operation for pull request {}\n'.format(issue_number))
                    pass

    print('main process ends\n################\n################\n\n')



################
if __name__ == '__main__':
    PR_helper()
