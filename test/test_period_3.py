import json

import os
import json

from models.ei_user import EiUser
from models.ei_issue import EiIssue
from models.ei_issue_pair import EiIssuePair
from logic.issue_pair_voter_history_rate import IssuePairVoterHistoryRate
from logic.ei_processor import EiProcessor

from test.conftest import get_issue_id, get_user_id

test_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), './')


def test_period_3():
    issues = json.load(open(os.path.join(test_path, 'data/period_3_issues.json')))

    ei_issue_list = []
    for issue in issues:
        contributer = EiUser(
            id=get_user_id(issue['contributer']['name']),
            name=issue['contributer']['name'],
            labels=issue['contributer']['labels'],
        )
        reviewer = EiUser(
            id=get_user_id(issue['reviewer']['name']),
            name=issue['reviewer']['name'],
            labels=issue['reviewer']['labels'],
        )
        ei_issue = EiIssue(
            id=get_issue_id(issue['org'], issue['repo'], issue['number'], issue['type']),
            _type = issue['type'],
            org = issue['org'],
            repo = issue['repo'],
            number = issue['number'],
            title = issue['title'],
            contributer = contributer,
            labels = issue['labels'],
            size = issue['size'],
            reviewer = reviewer,
            pr_org = issue['pr_org'],
            pr_repo = issue['pr_repo']
        )
        ei_issue_list.append(ei_issue)


    period_1_issues = json.load(open(os.path.join(test_path, 'data/period_1_issues.json')))
    period_1_title_2_issue = {}
    for issue in period_1_issues:
        contributer = EiUser(
            id=get_user_id(issue['contributer']['name']),
            name=issue['contributer']['name'],
            labels=issue['contributer']['labels'],
        )
        reviewer = EiUser(
            id=get_user_id(issue['reviewer']['name']),
            name=issue['reviewer']['name'],
            labels=issue['reviewer']['labels'],
        )
        ei_issue = EiIssue(
            id=get_issue_id(issue['org'], issue['repo'], issue['number'], issue['type']),
            _type = issue['type'],
            org = issue['org'],
            repo = issue['repo'],
            number = issue['number'],
            title = issue['title'],
            contributer = contributer,
            labels = issue['labels'],
            size = issue['size'],
            reviewer = reviewer,
            pr_org = issue['pr_org'],
            pr_repo = issue['pr_repo']
        )
        period_1_title_2_issue[issue['title']] = ei_issue

    period_1_ei_issue_pair_list = []
    period_1_assignees_info = json.load(open(os.path.join(test_path, 'data/period_1_assignees_info.json')))
    for pair in period_1_assignees_info["pair_voter_info"]["ei_issue_pair_list"]:
        left = period_1_title_2_issue[pair["left"]["title"]]
        right = period_1_title_2_issue[pair["right"]["title"]]
        c = pair["user"]
        voter = EiUser(
            id=c['id'],
            name=c['name'],
            labels=c['labels'],
        )
        eip = EiIssuePair(left, right)
        eip.c = voter
        period_1_ei_issue_pair_list.append(eip)


    period_2_issues = json.load(open(os.path.join(test_path, 'data/period_2_issues.json')))
    period_2_title_2_issue = {}
    for issue in period_2_issues:
        contributer = EiUser(
            id=get_user_id(issue['contributer']['name']),
            name=issue['contributer']['name'],
            labels=issue['contributer']['labels'],
        )
        reviewer = EiUser(
            id=get_user_id(issue['reviewer']['name']),
            name=issue['reviewer']['name'],
            labels=issue['reviewer']['labels'],
        )
        ei_issue = EiIssue(
            id=get_issue_id(issue['org'], issue['repo'], issue['number'], issue['type']),
            _type = issue['type'],
            org = issue['org'],
            repo = issue['repo'],
            number = issue['number'],
            title = issue['title'],
            contributer = contributer,
            labels = issue['labels'],
            size = issue['size'],
            reviewer = reviewer,
            pr_org = issue['pr_org'],
            pr_repo = issue['pr_repo']
        )
        period_2_title_2_issue[issue['title']] = ei_issue

    period_2_ei_issue_pair_list = []
    period_2_assignees_info = json.load(open(os.path.join(test_path, 'data/period_2_assignees_info.json')))
    for pair in period_2_assignees_info["pair_voter_info"]["ei_issue_pair_list"]:
        left = period_2_title_2_issue[pair["left"]["title"]]
        right = period_2_title_2_issue[pair["right"]["title"]]
        c = pair["user"]
        voter = EiUser(
            id=c['id'],
            name=c['name'],
            labels=c['labels'],
        )
        eip = EiIssuePair(left, right)
        eip.c = voter
        period_2_ei_issue_pair_list.append(eip)


    period_1_rate = IssuePairVoterHistoryRate(period_1_ei_issue_pair_list)
    period_2_rate = IssuePairVoterHistoryRate(period_2_ei_issue_pair_list)
    ep = EiProcessor('2', ei_issue_list, prev_voter_history_rate=period_1_rate, prev_prev_voter_history_rate=period_2_rate)
    ep.process()
    assert ep.pair_success() == True
    # print(ep.assignees_info)
    # json.dump(ep.assignees_info, open(os.path.join(test_path, 'data/period_3_assignees_info.json'), "w"), ensure_ascii=False, indent=True)
