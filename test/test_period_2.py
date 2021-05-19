import json

import os
import json

from models.ei_user import EiUser
from models.ei_issue import EiIssue
from models.ei_issue_pair import EiIssuePair
from logic.issue_pair_voter_history_rate import IssuePairVoterHistoryRate
from logic.ei_processor import EiProcessor

test_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), './')


def test_first():
    issues = json.load(open(os.path.join(test_path, 'data/period_2_issues.json')))

    ei_issue_list = []
    for issue in issues:
        contributer = EiUser(
            name=issue['contributer']['name'],
            labels=issue['contributer']['labels'],
        )
        reviewer = EiUser(
            name=issue['reviewer']['name'],
            labels=issue['reviewer']['labels'],
        )
        ei_issue = EiIssue(
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
            name=issue['contributer']['name'],
            labels=issue['contributer']['labels'],
        )
        reviewer = EiUser(
            name=issue['reviewer']['name'],
            labels=issue['reviewer']['labels'],
        )
        ei_issue = EiIssue(
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
    for pair in period_1_assignees_info["ei_issue_pair_voter_processor_info"]["have_voter_ei_issue_pair_list"]:
        left = period_1_title_2_issue[pair["left"]["title"]]
        right = period_1_title_2_issue[pair["right"]["title"]]
        c = pair["user"]
        voter = EiUser(
            name=c['name'],
            labels=c['labels']
        )
        eip = EiIssuePair(left, right)
        eip.c = voter
        period_1_ei_issue_pair_list.append(eip)


    period_1_rate = IssuePairVoterHistoryRate(period_1_ei_issue_pair_list)
    ep = EiProcessor('2', ei_issue_list, prev_voter_history_rate=period_1_rate)
    ep.process()
    print(ep.assignees_info)
    # json.dump(ep.assignees_info, open(os.path.join(test_path, 'data/period_2_assignees_info.json'), "w"), ensure_ascii=False, indent=True)
