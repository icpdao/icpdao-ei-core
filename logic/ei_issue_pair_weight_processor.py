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

    def _get_history_weight(self, c):
        ri0 = self._get_history_ping_rate(self.right.c, c, self.prev_rate)
        ri1 = self._get_history_ping_rate(self.right.c, c, self.prev_prev_rate)
        li0 = self._get_history_ping_rate(self.left.c, c, self.prev_rate)
        li1 = self._get_history_ping_rate(self.left.c, c, self.prev_prev_rate)
        rr = (ri0+li0)*2 + (ri1+li1)
        return rr*(-10)

    def get_weight(self, ei_issue_pair, c):
        # TODO 需要引入 历史评价数量维度来调整配对
        weight = 0
        if c == ei_issue_pair.left.contributer or c == ei_issue_pair.right.contributer:
            weight = -100000

        # 历史review不要重复使用
        weight += self._get_history_weight(c)

        coder_ability_list_for_reviewer = self.ei_config.coder_ability_list_for_reviewer
        pair_user_ability_rate = self.ei_config.pair_user_ability_rate
        # 技术能力匹配
        if min(coder_ability_list_for_reviewer[ei_issue_pair.left.c], coder_ability_list_for_reviewer[ei_issue_pair.right.c]) > coder_ability_list_for_reviewer[c]:
            weight += -10

        ab = (coder_ability_list_for_reviewer[ei_issue_pair.left.c]+coder_ability_list_for_reviewer[ei_issue_pair.right.c])/(coder_ability_list_for_reviewer[c]*2)
        ab = ab if ab > 1 else 1/ab
        rt = 0.5 if min(coder_ability_list_for_reviewer[ei_issue_pair.left.c], coder_ability_list_for_reviewer[ei_issue_pair.right.c])>coder_ability_list_for_reviewer[c] else 1
        weight += pair_user_ability_rate * rt * 100 / ab

        pair_reviewer_rate_list = self.ei_config.pair_reviewer_rate_list
        pair_reviewer_rate = self.ei_config.pair_reviewer_rate
        # 是 reviewer
        if c == self.left.r:
            rate = pair_reviewer_rate_list.get(ei_issue_pair.left.c, {}).get(c, pair_reviewer_rate)
            weight += rate

        if c == self.right.r:
            rate = pair_reviewer_rate_list.get(ei_issue_pair.right.c, {}).get(c, pair_reviewer_rate)
            weight += rate

        result = weight*10 + (randrange(1, 100, 1)/10000)  # 在相同值的情况下增加一个随机波动

        return result
