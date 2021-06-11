import json

import os
import json

from models.ei_issue import EiIssue
from models.ei_user import EiUser

from logic.ei_processor import EiProcessor

from test.conftest import get_issue_id, get_user_id

test_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), './')

def test_first():
    issues = json.load(open(os.path.join(test_path, 'data/period_two_person_equ_issues.json')))

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

    ep = EiProcessor('one_issue', ei_issue_list)
    ep.process()
    assert ep.pair_success() == True
    # json.dump(ep.assignees_info, open(os.path.join(test_path, 'data/period_two_person_equ_assignees_info.json'), "w"), ensure_ascii=False, indent=True)
