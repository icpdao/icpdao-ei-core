import json

import os
import json

from models.ei_issue import EiIssue
from logic.ei_processor import EiProcessor

test_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), './')

def test_first():
    issues = json.load(open(os.path.join(test_path, 'data/period_1_issues.json')))

    ei_issue_list = []
    for issue in issues:
        ei_issue = EiIssue(
            _type = issue['type'],
            org = issue['org'],
            repo = issue['repo'],
            number = issue['number'],
            title = issue['title'],
            contributer = issue['contributer'],
            labels = issue['labels'],
            size = issue['size'],
            reviewer = issue['reviewer'],
            pr_org = issue['pr_org'],
            pr_repo = issue['pr_repo']
        )
        ei_issue_list.append(ei_issue)


    ep = EiProcessor('first', ei_issue_list)
    ep.process()
    print(ep.assignees_info)
    # json.dump(ep.assignees_info, open(os.path.join(test_path, 'data/period_1_assignees_info.json'), "w"), ensure_ascii=False, indent=True)
