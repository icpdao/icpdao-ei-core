from random import randrange

from models.ei_issue_pair import EiIssuePair

class EiIssueWeightProcessor:
    """
    issue 配对权重计算
    """
    def __init__(self, ei_issue_list, ei_config):
        self.ei_issue_list = ei_issue_list
        self.ei_config = ei_config
        self.issue_pair_is_in = {}

        self.issue_more_half_user_name = None
        self.user_count = 0
        self.issue_count = len(self.ei_issue_list)

        user_issue_is_in = {}
        for ei_issue in self.ei_issue_list: 
            user_issue_is_in.setdefault(ei_issue.contributer.name, {})
            user_issue_is_in[ei_issue.contributer.name][ei_issue.id] = True

        self.user_count = len(list(user_issue_is_in.keys()))
        for user_name in user_issue_is_in:
            count = len(user_issue_is_in[user_name].keys())
            if count * 2 > self.issue_count:
                self.issue_more_half_user_name = user_name

    def add_pair(self, pair):
        self.issue_pair_is_in[pair.pair_hash()] = True

    def get_weight(self, ei_issue_1, ei_issue_2):
        ratio = 1
        # 处理贡献者相同问题
            # 一个人，允许两个贡献者相同  flag_1
            # 非一个人时，某人的ISSUE过半，允许这个人出现贡献者相同的配对？ flag_2
            # 其他情况不允许两个贡献者相同

        i_1_c = ei_issue_1.contributer.name
        i_2_c = ei_issue_2.contributer.name

        flag_1 = self.user_count == 1

        flag_2 = not flag_1 and self.issue_more_half_user_name == i_1_c and i_1_c == i_2_c

        if not flag_1 and not flag_2:
            if i_1_c == i_2_c:
                return -10000

        # 处理配对相同问题
        #     一个人，一个ISSUE时，允许配对相同 flag_1
        #     其他情况权重减半
        flag_1 = self.user_count == 1 and self.issue_count == 1

        if not flag_1:
            pair = EiIssuePair(ei_issue_1, ei_issue_2)
            if self.issue_pair_is_in.get(pair.pair_hash(), False):
                raise "配对错误"
            if self.issue_pair_is_in.get(pair.other_pair_hash(), False):
                ratio = 0

        # lable
        ei_issue_1_lable_info = ei_issue_1.label_info
        ei_issue_2_lable_info = ei_issue_2.label_info

        weight = 0
        lables = set(ei_issue_1_lable_info.keys()) & set(ei_issue_2_lable_info.keys())
        for label in lables:
            weight += ei_issue_1_lable_info[label] * self.ei_config.ei_p_label_weight * self.ei_config.ei_p_label_weight_ratio

        # size
        if ei_issue_1.size > ei_issue_2.size:
            sr = ei_issue_1.size / ei_issue_2.size
        else:
            sr = ei_issue_2.size / ei_issue_1.size
        weight += self.ei_config.ei_p_label_weight_ratio * (self.ei_config.ei_p_size_weight / sr)

        # reviewer
        if ei_issue_1.reviewer == ei_issue_2.reviewer:
            weight += self.ei_config.ei_p_reviewer_weight * self.ei_config.ei_p_reviewer_weight_ratio

        # 在相同值的情况下增加一个随机波动
        weight = weight*10 + (randrange(1, 100, 1)/10000)

        # 给处理配对相同问题 加一个阶梯
        weight = weight + ratio * 10000

        return weight
