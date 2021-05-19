from random import randrange

from models.ei_issue_pair import EiIssuePair

class EiIssueWeightProcessor:
    def __init__(self, ei_issue_pair_list, ei_config):
        self.ei_issue_pair_list = ei_issue_pair_list
        self.ei_config = ei_config

        self.issue_pair_is_in = {}
        for ep in self.ei_issue_pair_list:
            self.issue_pair_is_in[ep.id] = True

    def get_weight(self, ei_issue_1, ei_issue_2):
        # 贡献者相同
        if ei_issue_1.contributer.name == ei_issue_2.contributer.name:
            return self.ei_config.invalid_same_c_rate

        # 相同的配对
        pair = EiIssuePair(ei_issue_1, ei_issue_2)
        if self.issue_pair_is_in.get(pair.id, False):
            return self.ei_config.invalid_same_dup_rate
        
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

        return weight
