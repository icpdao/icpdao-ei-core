class IssuePairVoterHistoryRate:
    """
    vote_count_stat 格式 {
        # user1 是 被投票者
        # vote_user 是 投票者
        # count 是 被投票者 和 投票者 被分配到一起的次数
        "user1": {
            "vote_user": count,
            "vote_user2": count 
        }
        "user2": {
            "vote_user": rate,
            "vote_user2": rate
        }
    }

    issue_pari_count_stat 格式 {
        # user1 是 被投票者
        # count 是 被投票者 的 issue_pari 总数量
        "user1": count,
        "user2": count
    }

    rate 格式 {
        # user1 是 被投票者
        # vote_user 是 投票者
        # rate 的计算方式是 被分配到一起的次数 / 被投票者 的 issue_pari 总数量
        "user1": {
            "vote_user": rate, 
            "vote_user2": rate
        }
        "user2": {
            "vote_user": rate,
            "vote_user2": rate
        }
    }
    """
    def __init__(self, period_ei_issue_pair_list):
        self.period_ei_issue_pair_list = period_ei_issue_pair_list

        self.vote_count_stat = {}
        self.issue_pari_count_stat = {}
        self.rate = {}

        self.stat()

    def stat(self):
        for eip in self.period_ei_issue_pair_list:
            left = eip.left.contributer
            right = eip.right.contributer
            c = eip.c

            self._set_issue_pari_count_stat(left, 1)
            self._set_issue_pari_count_stat(right, 1)

            self._set_vote_count_stat_value(left, c, 1)
            self._set_vote_count_stat_value(right, c, 1)

        for u1 in self.vote_count_stat:
            for u2 in self.vote_count_stat[u1]:
                vote_count = self.vote_count_stat[u1][u2]
                issue_pari_count = self.issue_pari_count_stat[u1]

                _set_rate(u1, u2, vote_count/issue_pari_count)

    def _set_issue_pari_count_stat(self, key, add_value):
        old_value = self.issue_pari_count_stat.get(key, 0)
        self.issue_pari_count_stat[key] = old_value + add_value

    def _set_vote_count_stat_value(self, key1, key2, add_value):
        _dict2 = self.vote_count_stat.get(key1, {})
        old_value = _dict2.get(key2, 0)
        _dict2[key2] = old_value + add_value
        self.vote_count_stat[key1] = _dict2

    def _set_rate(self, key1, key2, new_value):
        _dict2 = self.rate.get(key1, {})
        _dict2[key2] = round(new_value, 2)
        self.rate[key1] = _dict2
