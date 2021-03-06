from random import randrange

from models.ei_issue_pair import EiIssuePair

class EiIssueWeightProcessor:
    """
    issue 配对权重计算
    """
    def __init__(self, user_count, issue_count, issue_more_half_user_name, ei_config, prev_issue_count, ei_issue_pair_id_blacklist_is_in):
        self.issue_more_half_user_name = issue_more_half_user_name
        self.user_count = user_count
        self.issue_count = issue_count
        self.ei_config = ei_config

        self.prev_issue_count = prev_issue_count

        self.ei_issue_pair_id_blacklist_is_in = ei_issue_pair_id_blacklist_is_in
        self.has_blacklist = len(list(self.ei_issue_pair_id_blacklist_is_in.keys())) > 0

    def get_weight(self, ei_issue_1, ei_issue_2):
        # 如果该配对在上几轮配对中已经尝试，并且不符合要求
        if self.has_blacklist:
            pair = EiIssuePair(ei_issue_1, ei_issue_2)
            if self.ei_issue_pair_id_blacklist_is_in.get(pair.id, False):
                return -10000

        # 非第一轮匹配需要查看 ISSUE 出现次数
        count_1 = self.prev_issue_count.get(ei_issue_1.id, 0)
        count_2 = self.prev_issue_count.get(ei_issue_2.id, 0)
        if count_1 >= 2 or count_2 >= 2:
            return -10000

        # 配对的两个ISSUE相同
        #     一个ISSUE时，允许 flag_1
        #     其他情况，不允许
        flag_1 = self.issue_count == 1 and self.user_count == 1
        if not flag_1:
            if ei_issue_1.id == ei_issue_2.id:
                return -10000

        # 两个贡献者相同
        #     一个人时，允许 flag_1
        #     非一个人时，某人的ISSUE过半时，允许这个人出现贡献者相同的配对 flag_2
        #     其他情况，不允许
        i_1_c = ei_issue_1.contributer.name
        i_2_c = ei_issue_2.contributer.name

        flag_1 = self.user_count == 1
        flag_2 = not flag_1 and self.issue_more_half_user_name == i_1_c and i_1_c == i_2_c

        if not flag_1 and not flag_2:
            if i_1_c == i_2_c:
                return -10000

        weight = 0
        # 如果某人 ISSUE 数量过半，需要分两个阶梯
        #   某人的 两个 ISSUE 进行配对 权重要低一个阶梯
        #   其他配对  权重要高一个阶梯
        if self.issue_more_half_user_name:
            i_1_c = ei_issue_1.contributer.name
            i_2_c = ei_issue_2.contributer.name
            h_c = self.issue_more_half_user_name
            if i_1_c == i_2_c and i_2_c == h_c:
                weight += 2500
            else:
                weight += 5000

        # lable
        ei_issue_1_lable_info = ei_issue_1.label_info
        ei_issue_2_lable_info = ei_issue_2.label_info

        lables = set(ei_issue_1_lable_info.keys()) & set(ei_issue_2_lable_info.keys())
        for label in lables:
            weight += ei_issue_1_lable_info[label] * self.ei_config.ei_p_label_weight * self.ei_config.ei_p_label_weight_ratio

        # size
        if ei_issue_1.size > ei_issue_2.size:
            sr = ei_issue_1.size / ei_issue_2.size
        else:
            sr = ei_issue_2.size / ei_issue_1.size
        sr = float(sr)
        weight += self.ei_config.ei_p_label_weight_ratio * (self.ei_config.ei_p_size_weight / sr)

        # reviewer
        if ei_issue_1.reviewer == ei_issue_2.reviewer:
            weight += self.ei_config.ei_p_reviewer_weight * self.ei_config.ei_p_reviewer_weight_ratio

        # 在相同值的情况下增加一个随机波动
        weight = weight*10 + (randrange(1, 100, 1)/10000)

        return weight
