from random import randrange


class EiIssuePairWeightProcessor:
    def __init__(self, ei_issue_pair_list, ei_config, prev_voter_history_rate=None, prev_prev_voter_history_rate=None):
        self.ei_issue_pair_list = ei_issue_pair_list
        self.ei_config = ei_config

        self.prev_rate = prev_voter_history_rate
        self.prev_prev_rate = prev_prev_voter_history_rate

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

    def get_weight(self, ei_issue_pair, voter):
        c = voter.name

        weight = 0

        # 贡献者和投票者相同
        if c == ei_issue_pair.left.contributer.name or c == ei_issue_pair.right.contributer.name:
            weight = -100000

        # 历史 review 和当前配对相同，减少一些权重
        weight += self._get_history_weight(ei_issue_pair, c)

        coder_ability_list_for_reviewer = self.ei_config.coder_ability_list_for_reviewer
        pair_user_ability_rate = self.ei_config.pair_user_ability_rate

        left_c_coder_ability_list_for_reviewer = coder_ability_list_for_reviewer.get(ei_issue_pair.left.contributer.name, 1)
        right_c_coder_ability_list_for_reviewer = coder_ability_list_for_reviewer.get(ei_issue_pair.right.contributer.name, 1)
        c_coder_ability_list_for_reviewer = coder_ability_list_for_reviewer.get(c, 1)

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
