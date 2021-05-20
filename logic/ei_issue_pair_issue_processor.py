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

    def pair_success(self):
        return self.pair_success

    def process(self):
        self.ei_issue_pair_list = []
        self.un_pair_ei_issue_list = []
        self.total_weight = 0

        if len(self.ei_issue_list) == 0:
            self.pair_success = True
            return

        print("开始配对...")
        self.pair_success = False
        self.pair_ei_issue()

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

        weight_processor = EiIssueWeightProcessor(self.ei_issue_list, self.ei_config)
        key_2_weight = {}

        # 获取权重矩阵        
        weight_matrix = [[0 for i in range(len(ei_issue_list_part_2))] for i in range(len(ei_issue_list_part_1))]
        for x_index, x_ei_issue in enumerate(ei_issue_list_part_1):
            for y_index, y_ei_issue in enumerate(ei_issue_list_part_2):
                # print("y_index {}".format(y_index))
                weight = weight_processor.get_weight(x_ei_issue, y_ei_issue)
                weight_matrix[x_index][y_index] = weight
                key = "{}_{}".format(x_index, y_index)
                key_2_weight[key] = weight
                ep = EiIssuePair(x_ei_issue, y_ei_issue)
                weight_processor.add_pair(ep)

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
            pair.append((weight, left, right))
        ret = sorted(pair, key=lambda a: a[0], reverse=True)  # 进行排序，使得权值搞的优先进入pair

        for i in ret:
            weight = i[0]
            if weight > 0:
                self.add_ei_issue_pair(i[1], i[2], weight)

    def add_ei_issue_pair(self, left, right, weight):
        ep = EiIssuePair(left, right)
        self.ei_issue_pair_list.append(ep)
        self.total_weight += weight
