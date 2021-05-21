import logging

from .kuhn_munkres import KuhnMunkres
from models.ei_issue_pair import EiIssuePair
from .ei_issue_weight_processor import EiIssueWeightProcessor


class EiIssuePairIssueProcessor:
    """
    处理 issue 配对
    """
    def __init__(self, ei_issue_list, ei_config):
        self.ei_issue_list = ei_issue_list[:]
        self.ei_config = ei_config

        self.user_count, self.issue_count, self.issue_more_half_user_name = self.get_total_info()

        # 成功配对中，ISSUE 出现的次数
        # {'issue_id': pair_count}
        self.pair_dict = {}
        # 已经成功配对过的
        self.ei_issue_pair_is_in = {}
        # 已经尝试配对，但是不符合要求的配对
        self.ei_issue_pair_id_blacklist_is_in = {}

    def pair_success(self):
        return self.pair_success

    def process(self):
        self.ei_issue_pair_list = []
        self.un_pair_ei_issue_list = []
        self.total_weight = 0

        if len(self.ei_issue_list) == 0:
            self.pair_success = True
            return

        self.pair_success = False
        for i in range(20):
            print("开始配对，第 {} 次...".format(i+1))
            self.pair_ei_issue()
            if len(self.ei_issue_pair_list) == len(self.ei_issue_list):
                break
            print("配对数量：{}/{}".format(
                len(self.ei_issue_pair_list),
                len(self.ei_issue_list)
            ))

        if len(self.ei_issue_pair_list) == len(self.ei_issue_list):
            self.pair_success = True
        else:
            self.pair_success = False

        print("issue 配对结束：{}  配对数量：{}/{}".format(
            ("成功" if self.pair_success else "失败" ),
            len(self.ei_issue_pair_list),
            len(self.ei_issue_list)
        ))

    @property
    def info(self):
        return {
            "ei_issue_pair_list": self.ei_issue_pair_list,
            "total_weight": self.total_weight,
            "pair_success": self.pair_success
        }

    @property
    def dict_info(self):
        return {
            "ei_issue_pair_list": [item.to_dict() for item in self.ei_issue_pair_list],
            "total_weight": self.total_weight,
            "pair_success": self.pair_success
        }

    def pair_ei_issue(self):
        ei_issue_list_part_1 = self.ei_issue_list[:]
        ei_issue_list_part_2 = self.ei_issue_list[:]

        weight_processor = EiIssueWeightProcessor(self.user_count, self.issue_count, self.issue_more_half_user_name, self.ei_config, self.pair_dict, self.ei_issue_pair_id_blacklist_is_in)
        key_2_weight = {}

        # 获取权重矩阵
        weight_matrix = [[0 for i in range(len(ei_issue_list_part_2))] for i in range(len(ei_issue_list_part_1))]
        for x_index, x_ei_issue in enumerate(ei_issue_list_part_1):
            for y_index, y_ei_issue in enumerate(ei_issue_list_part_2):
                weight = weight_processor.get_weight(x_ei_issue, y_ei_issue)
                weight_matrix[x_index][y_index] = weight
                key = "{}_{}".format(x_index, y_index)
                key_2_weight[key] = weight
                ep = EiIssuePair(x_ei_issue, y_ei_issue)

        km = KuhnMunkres(weight_matrix)
        km.run()
        # [(0, 2), (1, 1), (2, 0)]

        # 获取 ISSUE PAIR
        pair = []
        for mat in km.match:
            left = ei_issue_list_part_1[mat[0]]
            right = ei_issue_list_part_2[mat[1]]
            key = "{}_{}".format(mat[0], mat[1])
            weight = key_2_weight[key]
            pair.append((weight, left, right, mat[0], mat[1]))
        ret = sorted(pair, key=lambda a: a[0], reverse=True)  # 进行排序，使得权值搞的优先进入pair

        for i in ret:
            weight = i[0]
            left = i[1]
            right = i[2]
            if self.is_valid(left, right, weight):
                self.add_ei_issue_pair(left, right, weight)
            else:
                ep = EiIssuePair(left, right)
                self.ei_issue_pair_id_blacklist_is_in[ep.id] = True

    def is_valid(self, left, right, weight):
        if weight <= 0:
            return False

        self.pair_dict.setdefault(left.id, 0)
        self.pair_dict.setdefault(right.id, 0)        
        if self.pair_dict[left.id] >= 2:
            return False
        if self.pair_dict[right.id] >= 2:
            return False

        # 配对第二次出现
        #     一个ISSUE时，允许 flag_1
        #     人数大于3时，允许 flag_2
        #     其他情况，不允许
        flag_1 = self.user_count == 1 and self.issue_count == 1
        flag_2 = self.user_count > 3
        if not flag_1 and not flag_2:
            pair = EiIssuePair(left, right)
            if self.ei_issue_pair_is_in.get(pair.id, False):
                return False

        return True
    
    def add_ei_issue_pair(self, left, right, weight):
        ep = EiIssuePair(left, right)
        self.ei_issue_pair_list.append(ep)
        self.total_weight += weight

        self.ei_issue_pair_is_in[ep.id] = True

        self.pair_dict.setdefault(left.id, 0)
        self.pair_dict.setdefault(right.id, 0)
        self.pair_dict[left.id] += 1
        self.pair_dict[right.id] += 1

    def get_total_info(self):
        issue_more_half_user_name = None
        user_count = 0
        issue_count = len(self.ei_issue_list)

        user_issue_is_in = {}
        for ei_issue in self.ei_issue_list: 
            user_issue_is_in.setdefault(ei_issue.contributer.name, {})
            user_issue_is_in[ei_issue.contributer.name][ei_issue.id] = True

        user_count = len(list(user_issue_is_in.keys()))
        for user_name in user_issue_is_in:
            count = len(user_issue_is_in[user_name].keys())
            if count * 2 > issue_count:
                issue_more_half_user_name = user_name

        return user_count, issue_count, issue_more_half_user_name
