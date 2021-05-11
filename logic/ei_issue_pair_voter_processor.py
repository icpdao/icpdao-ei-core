import math
import logging
from .kuhn_munkres import KuhnMunkres
from .ei_issue_pair_weight_processor import EiIssuePairWeightProcessor


class EiIssuePairVoterProcessor:
    def __init__(self, ei_issue_pair_list, voter_dict, ei_config, prev_voter_history_rate=None, prev_prev_voter_history_rate=None):
        self.ei_issue_pair_list = ei_issue_pair_list
        self.voter_dict = voter_dict
        self.ei_config = ei_config

        self.prev_voter_history_rate = prev_voter_history_rate
        self.prev_prev_voter_history_rate = prev_prev_voter_history_rate

        self.weight_processor = EiIssuePairWeightProcessor(ei_issue_pair_list, self.ei_config, prev_voter_history_rate, prev_prev_voter_history_rate)

        new_voter_dict = dict()
        for key in self.voter_dict:
            if key in self.ei_config.tmp_skip_voter_list:
                continue
            new_voter_dict[key] = self.voter_dict[key]
        self.voter_dict = new_voter_dict

        self.have_voter_ei_issue_pair_list = []
        self.no_have_ei_issue_pair_list = []
        self.total_weight = 0

    @property
    def info(self):
        return {
            "have_voter_ei_issue_pair_list": self.have_voter_ei_issue_pair_list,
            "no_have_ei_issue_pair_list": self.no_have_ei_issue_pair_list,
            "total_weight": self.total_weight
        }

    @property
    def dict_info(self):
        return {
            "have_voter_ei_issue_pair_list": [item.to_dict() for item in self.have_voter_ei_issue_pair_list],
            "no_have_ei_issue_pair_list": [item.to_dict() for item in self.no_have_ei_issue_pair_list],
            "total_weight": self.total_weight
        }

    def process(self):
        if len(self.ei_issue_pair_list) == 0:
            return self.info

        voter_list = []
        for key in self.voter_dict:
            name = key
            count = int(self.voter_dict[key]*1.2)
            name_list = [name for i in range(count)]
            voter_list += name_list

        # 获取权重矩阵
        weight_matrix = [[0 for j in range(len(voter_list))] for i in range(len(self.ei_issue_pair_list))]
        for x_index, ei_issue_pair in enumerate(self.ei_issue_pair_list):
            for y_index, voter in enumerate(voter_list):
                weight_matrix[x_index][y_index] = self.weight_processor.get_weight(ei_issue_pair, voter)
                

        km = KuhnMunkres(weight_matrix)
        km.run()
        # [(0, 2), (1, 1), (2, 0)]

        have_voter_ei_issue_pair_list = []
        no_have_ei_issue_pair_list = []

        # 获取 ISSUE PAIR
        total_weight = 0
        for mat in km.match:
            ei_issue_pair = self.ei_issue_pair_list[mat[0]]
            c = voter_list[mat[1]]

            weight = self.weight_processor.get_weight(ei_issue_pair, c)

            if weight >= 0:
                ei_issue_pair.c = c
                have_voter_ei_issue_pair_list.append(ei_issue_pair)
                total_weight += weight
            else:
                no_have_ei_issue_pair_list.append(ei_issue_pair)

        if len(no_have_ei_issue_pair_list) != 0:
            for c in self.voter_dict:
                count = self.voter_dict[c]
                add_count = math.ceil(count * 0.1)
                current_count = 0
                tmp_list = no_have_ei_issue_pair_list[:]
                for ei_issue_pair in tmp_list:
                    weight = self.weight_processor.get_weight(ei_issue_pair, c)
                    if weight >= 0:
                        ei_issue_pair.c = c
                        have_voter_ei_issue_pair_list.append(ei_issue_pair)
                        no_have_ei_issue_pair_list.remove(ei_issue_pair)
                        total_weight += weight
                        current_count += 0
                    if current_count >= add_count:
                        break

        if len(no_have_ei_issue_pair_list) != 0:
            add_count = math.ceil(len(no_have_ei_issue_pair_list) / len(self.ei_config.other_c_list))
            for c in self.ei_config.other_c_list:
                current_count = 0
                tmp_list = no_have_ei_issue_pair_list[:]
                for ei in tmp_list:
                    weight = self.weight_processor.get_weight(ei_issue_pair, c)
                    if weight >= 0:
                        ei_issue_pair.c = c
                        have_voter_ei_issue_pair_list.append(ei)
                        no_have_ei_issue_pair_list.remove(ei)
                        total_weight += weight
                        current_count += 0
                    if current_count >= add_count:
                        break

        if len(no_have_ei_issue_pair_list) != 0:
            logging.info("pair__ei_issue_pair_and_c 分配错误")
            exit(1)

        self.have_voter_ei_issue_pair_list = have_voter_ei_issue_pair_list
        self.no_have_ei_issue_pair_list = no_have_ei_issue_pair_list
        self.total_weight = total_weight
        return
