import json

import os
import json

from models.ei_issue import EiIssue
from models.ei_user import EiUser

from logic.ei_processor import EiProcessor

test_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), './')

def test_equ():
    issues = json.load(open(os.path.join(test_path, 'data/period_3_person_equ_issues.json')))

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

    ep = EiProcessor('period_3_person_equ', ei_issue_list)
    ep.process()
    assert ep.pair_success() == True
    # json.dump(ep.assignees_info, open(os.path.join(test_path, 'data/period_3_person_equ_assignees_info.json'), "w"), ensure_ascii=False, indent=True)


def test_1():
    # 16 16 18
    issues = json.load(open(os.path.join(test_path, 'data/period_3_person_1_issues.json')))

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

    ep = EiProcessor('period_3_person_1', ei_issue_list)
    ep.process()
    assert ep.pair_success() == True
    # json.dump(ep.assignees_info, open(os.path.join(test_path, 'data/period_3_person_1_assignees_info.json'), "w"), ensure_ascii=False, indent=True)

def test_2():
    # 1 2 18
    issues = json.load(open(os.path.join(test_path, 'data/period_3_person_2_issues.json')))

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

    ep = EiProcessor('period_3_person_2', ei_issue_list)
    ep.process()
    assert ep.pair_success() == True
    # json.dump(ep.assignees_info, open(os.path.join(test_path, 'data/period_3_person_2_assignees_info.json'), "w"), ensure_ascii=False, indent=True)
