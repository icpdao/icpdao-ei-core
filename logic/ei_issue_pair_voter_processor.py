import math
import logging
from .kuhn_munkres import KuhnMunkres
from .ei_issue_pair_weight_processor import EiIssuePairWeightProcessor
from models.ei_issue_pair import EiIssuePair


class EiIssuePairVoterProcessor:
    """
    匹配投票者
    """
    def __init__(self, ei_issue_pair_list, voter_count_dict, ei_config, prev_voter_history_rate=None, prev_prev_voter_history_rate=None):
        self.ei_issue_pair_list = ei_issue_pair_list
        self.voter_count_dict = voter_count_dict
        self.ei_config = ei_config

        self.voter_info_dict = self.build_voter_info_dict(self.ei_issue_pair_list)
        self.build_voter_count_dict_by_tmp_skip_voter_list()

        self.prev_voter_history_rate = prev_voter_history_rate
        self.prev_prev_voter_history_rate = prev_prev_voter_history_rate

        self.have_voter_ei_issue_pair_list = []
        self.no_have_ei_issue_pair_list = []
        self.total_weight = 0

        self.user_count, self.issue_count, self.issue_more_half_user_name = self.get_total_info()

    def pair_success(self):
        return self.pair_success

    def build_voter_count_dict_by_tmp_skip_voter_list(self):
        new_voter_count_dict = dict()
        for key in self.voter_count_dict:
            if key in self.ei_config.tmp_skip_voter_list:
                continue
            new_voter_count_dict[key] = self.voter_count_dict[key]
        self.voter_count_dict = new_voter_count_dict

    def build_voter_info_dict(self, ei_issue_pair_list):
        res = {}
        for ei_issue_pair in ei_issue_pair_list:
            leftc = ei_issue_pair.left.contributer
            rightc = ei_issue_pair.right.contributer
            if not res.get(leftc.name):
                res[leftc.name] = leftc
            if not res.get(rightc.name):
                res[rightc.name] = rightc
        return res

    @property
    def info(self):
        return {
            "ei_issue_pair_list": self.have_voter_ei_issue_pair_list,
            "total_weight": self.total_weight,
            "pair_success": self.pair_success
        }

    @property
    def dict_info(self):
        return {
            "ei_issue_pair_list": [item.to_dict() for item in self.have_voter_ei_issue_pair_list],
            "total_weight": self.total_weight,
            "pair_success": self.pair_success
        }

    def first_voter_list(self):
        voter_list = []
        for name in self.voter_count_dict:
            count = math.ceil(self.voter_count_dict[name]*1.2)
            name_list = [name for i in range(count)]
            voter_list += name_list
        return voter_list

    def addi_voter_list(self):
        voter_list = []
        for name in self.voter_count_dict:
            count = math.ceil(self.voter_count_dict[name]*0.3)
            name_list = [name for i in range(count)]
            voter_list += name_list
        return voter_list

    def other_c_voter_list(self, no_have_ei_issue_pair_list):
        unpair_count = len(no_have_ei_issue_pair_list)
        voter_list = []
        if len(self.ei_config.other_c_list) > 0:
            # pre_count = math.ceil(unpair_count / len(self.ei_config.other_c_list))
            for name in self.ei_config.other_c_list:
                count = unpair_count
                name_list = [name for i in range(count)]
                voter_list += name_list
        
        if len(voter_list) == 0:
            # pre_count = math.ceil(len(no_have_ei_issue_pair_list) / len(list(self.voter_count_dict.keys())))
            for name in self.voter_count_dict:
                count = unpair_count
                name_list = [name for i in range(count)]
                voter_list += name_list
        return voter_list

    def process(self):
        if len(self.ei_issue_pair_list) == 0:
            return self.info

        # 正常匹配
        voter_list = self.first_voter_list()
        self.total_weight += self.pair(voter_list, self.ei_issue_pair_list)
        print("第 1 次匹配投票者结束")

        # 匹配不全时，给每个人多分几票
        if len(self.no_have_ei_issue_pair_list) == 0:
            self.pair_success = True
            return

        voter_list = self.addi_voter_list()
        self.total_weight += self.pair(voter_list, self.no_have_ei_issue_pair_list)
        print("第 2 次匹配投票者结束")

        # 仍然匹配不全时，剩下的给 other_c_list
        if len(self.no_have_ei_issue_pair_list) == 0:
            self.pair_success = True
            return

        voter_list = self.other_c_voter_list(self.no_have_ei_issue_pair_list)
        self.total_weight += self.pair(voter_list, self.no_have_ei_issue_pair_list)
        print("第 3 次匹配投票者结束")

        if len(self.no_have_ei_issue_pair_list) == 0:
            self.pair_success = True
            return

        self.pair_success = False

    def pair(self, voter_list, ei_issue_pair_list):
        self.weight_processor = EiIssuePairWeightProcessor(self.user_count, self.issue_count, self.issue_more_half_user_name, self.ei_config, self.prev_voter_history_rate, self.prev_prev_voter_history_rate)

        # 获取权重矩阵
        key_2_weight = {}
        weight_matrix = [[0 for j in range(len(voter_list))] for i in range(len(ei_issue_pair_list))]
        for x_index, ei_issue_pair in enumerate(ei_issue_pair_list):
            for y_index, voter_name in enumerate(voter_list):
                voter = self.voter_info_dict[voter_name]
                weight = self.weight_processor.get_weight(ei_issue_pair, voter)
                weight_matrix[x_index][y_index] = weight
                key = "{}_{}".format(x_index, y_index)
                key_2_weight[key] = weight
                self.weight_processor.add_pair(ei_issue_pair, voter)

        km = KuhnMunkres(weight_matrix)

        km.run()
        # [(0, 2), (1, 1), (2, 0)]

        # 获取 ISSUE PAIR
        pair = []
        res = km.match[0]
        key = "{}_{}".format(res[0], res[1])
        weight = key_2_weight[key]
        for mat in km.match:
            ei_issue_pair = ei_issue_pair_list[mat[0]]
            c = voter_list[mat[1]]
            key = "{}_{}".format(mat[0], mat[1])
            weight = key_2_weight[key]
            pair.append([weight, ei_issue_pair, c, mat[0], mat[1]])
        ret = sorted(pair, key=lambda a: a[0], reverse=True)

        total_weight = 0
        count = 0
        for i in ret:
            ei_issue_pair = i[1]
            c = i[2]
            weight = i[0]

            if ei_issue_pair.c:
                continue

            if weight > 0:
                voter = self.voter_info_dict[c]
                ei_issue_pair.c = voter
                total_weight += weight

        self.have_voter_ei_issue_pair_list, self.no_have_ei_issue_pair_list = self.check_ei_issue_pair_list_c()
        return total_weight

    def check_ei_issue_pair_list_c(self):
        no_have_ei_issue_pair_list = []
        have_ei_issue_pair_list = []
        for issue_pair in self.ei_issue_pair_list:
            if not issue_pair.c:
                no_have_ei_issue_pair_list.append(issue_pair)
            else:
                have_ei_issue_pair_list.append(issue_pair)
        return have_ei_issue_pair_list, no_have_ei_issue_pair_list

    def get_total_info(self):
        user_issue_is_in = {}
        issue_is_in = {}

        for ep in self.ei_issue_pair_list:
            issue_is_in[ep.left.id] = True
            issue_is_in[ep.right.id] = True

            user_issue_is_in.setdefault(ep.left.contributer.name, {})
            user_issue_is_in.setdefault(ep.right.contributer.name, {})

            user_issue_is_in[ep.left.contributer.name][ep.left.id] = True
            user_issue_is_in[ep.right.contributer.name][ep.right.id] = True

        user_count = len(list(user_issue_is_in.keys()))
        issue_count = len(list(issue_is_in.keys()))

        issue_more_half_user_name = None
        for user_name in user_issue_is_in:
            count = len(user_issue_is_in[user_name].keys())
            if count * 2 > issue_count:
                issue_more_half_user_name = user_name

        return user_count, issue_count, issue_more_half_user_name
