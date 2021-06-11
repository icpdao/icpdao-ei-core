import decimal

from models.ei_issue import EiIssue

from .ei_issue_pair_issue_processor import EiIssuePairIssueProcessor
from .ei_issue_pair_voter_processor import EiIssuePairVoterProcessor
from models.ei_config import default_config


class EiProcessor(object):
    def __init__(self, period, ei_issue_list, ei_config=None, prev_voter_history_rate=None, prev_prev_voter_history_rate=None):
        self.period = period
        self.ei_issue_list = ei_issue_list

        self.ei_config = ei_config
        if not ei_config:
            self.ei_config = default_config

        self.c_dict = self.build_c_dict()

        self.ei_issue_pair_issue_processor = None
        self.ei_issue_pair_voter_processor = None
        self.prev_voter_history_rate = prev_voter_history_rate
        self.prev_prev_voter_history_rate = prev_prev_voter_history_rate

        self.c_stat_dict = self.build_c_stat_dict(self.ei_issue_list)
        self.assignees_info = {
            "period": self.period,
            "c_stat_dict": self.c_stat_dict,
            "pair_issue_info": {},
            "pair_voter_info": {},
            "pair_success": False
        }

    def pair_success(self):
        return self.assignees_info['pair_success']

    def build_c_dict(self):
        c_dict = {}
        for ei in self.ei_issue_list:
            name = ei.contributer.name
            count = c_dict.get(name, 0)
            c_dict[name] = count + 1
        return c_dict

    def build_c_stat_dict(self, ei_issue_list):
        c_stat_dict = {}
        for issue in ei_issue_list:
            user_name = issue.contributer.name
            user_stat = c_stat_dict.get(user_name, {})
            issue_count = user_stat.get("issue_count", 0)
            issue_size = user_stat.get("issue_size", decimal.Decimal('0'))
            issue_list = user_stat.get("issue_list", [])

            issue_count = issue_count + 1
            issue_size = round(issue_size + issue.size, 2)
            issue_list.append(issue.to_dict())

            c_stat_dict[user_name] = {
                "issue_count": issue_count,
                "issue_size": issue_size,
                "issue_list": issue_list
            }

        return c_stat_dict

    def process(self):
        self.ei_issue_pair_issue_processor = EiIssuePairIssueProcessor(self.ei_issue_list, self.ei_config)
        self.ei_issue_pair_issue_processor.process()

        if not self.ei_issue_pair_issue_processor.pair_success:
            return

        self.assignees_info["pair_issue_info"] = self.ei_issue_pair_issue_processor.dict_info


        ei_issue_pair_list = self.ei_issue_pair_issue_processor.info["ei_issue_pair_list"]
        self.ei_issue_pair_voter_processor = EiIssuePairVoterProcessor(ei_issue_pair_list, self.c_dict, self.ei_config, self.prev_voter_history_rate, self.prev_prev_voter_history_rate)
        self.ei_issue_pair_voter_processor.process()

        if not self.ei_issue_pair_voter_processor.pair_success:
            return

        self.assignees_info["pair_voter_info"] = self.ei_issue_pair_voter_processor.dict_info
        self.assignees_info["pair_success"] = True
