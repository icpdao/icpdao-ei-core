from random import randrange

from models.ei_issue_pair import EiIssuePair

class EiIssuePairWeightProcessor:
    """
    pair 匹配投票者权重计算
    """
    def __init__(self, user_count, issue_count, issue_more_half_user_name, ei_config, prev_voter_history_rate=None, prev_prev_voter_history_rate=None):
        self.user_count = user_count
        self.issue_count = issue_count
        self.issue_more_half_user_name = issue_more_half_user_name
        self.ei_config = ei_config

        self.prev_rate = prev_voter_history_rate
        self.prev_prev_rate = prev_prev_voter_history_rate

        self.issue_pair_voter_name_dict = {}

    def _get_history_ping_rate(self, pinged, ping, rate):
        if rate and pinged in rate.rate and ping in rate.rate[pinged]:
            return rate.rate[pinged][ping]
        else:
            return 0

    def _get_history_weight(self, ei_issue_pair, c):
        ri0 = self._get_history_ping_rate(ei_issue_pair.right.contributer.name, c, self.prev_rate)
        ri1 = self._get_history_ping_rate(ei_issue_pair.right.contributer.name, c, self.prev_prev_rate)
        li0 = self._get_history_ping_rate(ei_issue_pair.left.contributer.name, c, self.prev_rate)
        li1 = self._get_history_ping_rate(ei_issue_pair.left.contributer.name, c, self.prev_prev_rate)
        rr = (ri0+li0)*2 + (ri1+li1)
        return rr*(-10)

    def add_pair(self, ei_issue_pair, voter):
        self.issue_pair_voter_name_dict.setdefault(ei_issue_pair.pair_hash(), {})
        self.issue_pair_voter_name_dict[ei_issue_pair.pair_hash()][voter.name] = True

    def get_weight(self, ei_issue_pair, voter):
        c = voter.name
        weight = 0

        # 投票者和贡献者相同
        #     一个人时，允许 flag_1
        #     其他情况，不允许
        i_1_c = ei_issue_pair.left.contributer.name
        i_2_c = ei_issue_pair.right.contributer.name
        flag_1 = self.user_count == 1
        if not flag_1:
            if c == i_1_c or c == i_2_c:
                return -20000

        # 配对第二次出现时
        #     一个人时，允许投票者和第一次相同 flag_1
        #     其他情况，不允许投票者和第一次相同
        flag_1 = self.user_count == 1
        if not flag_1:
            pair = EiIssuePair(ei_issue_pair.left, ei_issue_pair.right)
            has = self.issue_pair_voter_name_dict.get(pair.other_pair_hash(), {}).get(c, None)
            if has:
                return -20000

        # 历史 review 和当前配对相同，减少一些权重
        weight += self._get_history_weight(ei_issue_pair, c)

        ## labels
        c_label_info = voter.label_info
        c_label_set = set(c_label_info.keys())
        for issue in [ei_issue_pair.left, ei_issue_pair.right]:
            issue_label_info = issue.label_info
            issue_label_set  = set(issue_label_info.keys())
            bing = issue_label_set & c_label_set
            for label in list(bing):
                value = c_label_info[label]
                weight += value * self.ei_config.ei_pv_label_weight * self.ei_config.ei_pv_label_weight_ratio

        # reviewer
        for reviewer in [ei_issue_pair.left.reviewer, ei_issue_pair.right.reviewer]:
            name = reviewer.name
            if c == name:
                weight += self.ei_config.ei_pv_reviewer_weight * self.ei_config.ei_pv_reviewer_weight_ratio

        result = weight*10 + (randrange(1, 100, 1)/10000)  # 在相同值的情况下增加一个随机波动

        return result
