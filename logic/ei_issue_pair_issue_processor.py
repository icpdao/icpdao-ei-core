import logging

from .kuhn_munkres import KuhnMunkres
from models.ei_issue_pair import EiIssuePair
from .ei_issue_weight_processor import EiIssueWeightProcessor


class EiIssuePairIssueProcessor:
    def __init__(self, ei_issue_list, ei_config):
        self.origin_ei_issue_list = ei_issue_list[:]
        self.ei_issue_list = ei_issue_list[:]
        self.ei_config = ei_config

        self.ei_issue_pair_list = []
        self.total_weight = 0
        self.pair_count = 0
        self.pair_success = False
        self.un_pair_ei_issue_list = []
        self.try_count = 10

        # issue 数量超过了半数的 github_user_name
        self.more_than_half_github_user_name = None
        # 某一个人的 issue 数量超过了半数多少
        self.more_than_half_issue_count = None
        self.check_ei_issue_count()
        # 如果 某一个人的 issue 数量超过了半数，那么先计算出他不需要配对的 ei_issue 放在这里
        self.un_need_pair_ei_issue_list = None

    def process(self):
        if len(self.ei_issue_list) == 0:
            self.ei_issue_pair_list = []
            self.total_weight = 0
            self.pair_success = True
            self.un_pair_ei_issue_list = []
            return

        for i in range(self.try_count):
            self.pair_count += 1
            self.ei_issue_pair_list = []
            self.ei_issue_pair_count_dict = {}
            self.un_need_pair_ei_issue_list = None
            self.ei_issue_list = self.origin_ei_issue_list[:]
            for ei_issue in self.ei_issue_list:
                self.ei_issue_pair_count_dict[ei_issue.id] = 0
            print("第 {} 次配对中...".format(self.pair_count))

            self.pair_ei_issue()

            if self.more_than_half_github_user_name and self.un_need_pair_ei_issue_list is None:
                self.process_more_than()

            if len(self.ei_issue_pair_list) == len(self.ei_issue_list):
                self.pair_success = True
                break
            else:
                self.pair_success = False

        if self.un_need_pair_ei_issue_list is None:
            self.un_need_pair_ei_issue_list = []

        un_need_pair_ei_issue_list_count = len(self.un_need_pair_ei_issue_list) if self.un_need_pair_ei_issue_list else 0
        print("issue 配对结束：{}  配对数量：{}/{} 有{}不需要配对，配对次数：{}".format(
            ("成功" if self.pair_success else "失败" ),
            len(self.ei_issue_pair_list),
            len(self.ei_issue_list) + un_need_pair_ei_issue_list_count,
            un_need_pair_ei_issue_list_count,
            self.pair_count
        ))

        if not self.pair_success:
            logging.info("ei issue 分配失败")
            exit(1)

        return

    def process_more_than(self):
        un_pair_ei_issue_list = self.get_un_pair_ei_issue_list()

        if len(un_pair_ei_issue_list) != self.more_than_half_issue_count * 2:
            return
        for ei_issue in un_pair_ei_issue_list:
            if ei_issue.to_dict()["github_user_name"] != self.more_than_half_github_user_name:
                return

        un_need_pair_ei_issue_list = []
        for ei_issue in un_pair_ei_issue_list:
            if ei_issue not in un_need_pair_ei_issue_list:
                un_need_pair_ei_issue_list.append(ei_issue)

        self.un_need_pair_ei_issue_list = un_need_pair_ei_issue_list
        for ei_issue in un_need_pair_ei_issue_list:
            self.ei_issue_list.remove(ei_issue)

    def issue_count_stat(self):
        """
        {
            "github_user_name": issue_count
        }
        """
        stat = {}
        for ei_issue in self.ei_issue_list:
            github_user_name = ei_issue.to_dict()["github_user_name"]
            stat[github_user_name] = stat.get(github_user_name, 0) + 1
        return stat

    def check_ei_issue_count(self):
        stat = self.issue_count_stat()
        total_count = 0
        for github_user_name in stat:
            total_count += stat[github_user_name]
        for github_user_name in stat:
            count = stat[github_user_name]
            if count * 2 > total_count:
                # issue 数量超过了半数的 github_user_name
                self.more_than_half_github_user_name = github_user_name
                # 某一个人的 issue 数量超过了半数多少
                self.more_than_half_issue_count = count - (total_count - count)
                print("{} issue 数量超过了半数 {} 个".format(self.more_than_half_github_user_name, self.more_than_half_issue_count))

    @property
    def info(self):
        return {
            "ei_issue_pair_list": self.ei_issue_pair_list,
            "total_weight": self.total_weight,
            "pair_success": self.pair_success,
            "un_pair_ei_issue_list": self.un_pair_ei_issue_list,
            "un_need_pair_ei_issue_list": self.un_need_pair_ei_issue_list,
            "pair_count": self.pair_count
        }

    @property
    def dict_info(self):
        return {
            "ei_issue_pair_list": [item.to_dict() for item in self.ei_issue_pair_list],
            "total_weight": self.total_weight,
            "pair_success": self.pair_success,
            "un_pair_ei_issue_list": [item.to_dict() for item in self.un_pair_ei_issue_list],
            "un_need_pair_ei_issue_list": [item.to_dict() for item in self.un_need_pair_ei_issue_list],
            "pair_count": self.pair_count
        }

    def pair_ei_issue(self):
        ei_issue_list_part_1 = self.ei_issue_list[:]
        ei_issue_list_part_2 = self.ei_issue_list[:]

        weight_processor = EiIssueWeightProcessor(self.ei_issue_pair_list, self.ei_config)

        # 获取权重矩阵
        weight_matrix = [[0 for i in range(len(ei_issue_list_part_2))] for i in range(len(ei_issue_list_part_1))]
        for x_index, x_ei_issue in enumerate(ei_issue_list_part_1):
            for y_index, y_ei_issue in enumerate(ei_issue_list_part_2):
                weight_matrix[x_index][y_index] = weight_processor.get_weight(x_ei_issue, y_ei_issue)

        km = KuhnMunkres(weight_matrix)
        km.run()
        # [(0, 2), (1, 1), (2, 0)]

        # 获取 ISSUE PAIR
        pair = []
        for mat in km.match:
            left = ei_issue_list_part_1[mat[0]]
            right = ei_issue_list_part_2[mat[1]]
            weight = weight_processor.get_weight(left, right)
            pair.append((weight, left, right))
        ret = sorted(pair, key=lambda a: a[0], reverse=True)  # 进行排序，使得权值搞的优先进入pair

        for i in ret:
            if self.valid_ei_issue_pair(i[1], i[2]):
                self.add_ei_issue_pair(i[1], i[2])

    def valid_ei_issue_pair(self, left, right):
        weight = EiIssueWeightProcessor(self.ei_issue_pair_list, self.ei_config).get_weight(left, right)

        if weight <= 0:
            return False

        # TODO
        # 人数太少，还是暂时允许相同配对两次出现
        # if not self.more_than_half_github_user_name and issue_pair_is_in(self.ei_issue_pair_list, left, right):
        #     return False

        if self.ei_issue_pair_count_dict[left.id] >= 2:
            return False

        if self.ei_issue_pair_count_dict[right.id] >= 2:
            return False

        return True

    def add_ei_issue_pair(self, left, right):
        weight = EiIssueWeightProcessor(self.ei_issue_pair_list, self.ei_config).get_weight(left, right)

        ep = EiIssuePair(left, right)
        self.ei_issue_pair_list.append(ep)
        self.total_weight += weight

        self.ei_issue_pair_count_dict[left.id] = self.ei_issue_pair_count_dict[left.id] + 1
        self.ei_issue_pair_count_dict[right.id] = self.ei_issue_pair_count_dict[right.id] + 1

    def get_un_pair_ei_issue_list(self):
        if len(self.ei_issue_pair_list) == len(self.ei_issue_list):
            return []

        pair_ei_issue_list = []
        for pair in self.ei_issue_pair_list:
            ei_1 = pair.left
            ei_2 = pair.right
            pair_ei_issue_list.append(ei_1)
            pair_ei_issue_list.append(ei_2)

        all_ei_issue_list = []
        for ei_issue in self.ei_issue_list:
            all_ei_issue_list.append(ei_issue)
            all_ei_issue_list.append(ei_issue)

        un_pair_ei_issue_list = all_ei_issue_list[:]

        while len(pair_ei_issue_list) > 0:
            if pair_ei_issue_list[0] in un_pair_ei_issue_list:
                un_pair_ei_issue_list.remove(pair_ei_issue_list[0])
                pair_ei_issue_list.remove(pair_ei_issue_list[0])

        return un_pair_ei_issue_list
