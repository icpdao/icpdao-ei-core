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
        if ei_issue_1.contributer == ei_issue_2.contributer:
            return self.ei_config.invalid_same_c_rate

        pair = EiIssuePair(ei_issue_1, ei_issue_2)
        if self.issue_pair_is_in.get(pair.id, False):
            return self.ei_config.invalid_same_dup_rate

        coder_ability_list = self.ei_config.coder_ability_list

        if coder_ability_list.get(ei_issue_2.contributer, 1) > coder_ability_list.get(ei_issue_1.contributer, 1):
            cr = coder_ability_list.get(ei_issue_2.contributer, 1) / coder_ability_list.get(ei_issue_1.contributer, 1)
        else:
            cr = coder_ability_list.get(ei_issue_1.contributer, 1) / coder_ability_list.get(ei_issue_2.contributer, 1)

        weight = self.ei_config.user_ability_rate / cr
        
        weight += len(ei_issue_1.labels & ei_issue_2.labels) * self.ei_config.label_rate   # 每多一个相同的label就增加一个值

        if ei_issue_1.pr_org == ei_issue_2.pr_org and ei_issue_1.pr_repo == ei_issue_2.pr_repo:   # 相同的repo
            weight += self.ei_config.same_repo_rate

        sr = (ei_issue_1.size / ei_issue_2.size) if (ei_issue_1.size > ei_issue_2.size) else (ei_issue_2.size / ei_issue_1.size )
        weight += self.ei_config.same_size_rate/sr  # 偏差越大权值越低

        if ei_issue_1.reviewer == ei_issue_2.reviewer:
            weight += self.ei_config.same_reviewer_rate

        if ei_issue_1.type == ei_issue_2.type:
            weight += self.ei_config.type_same

        return weight*10 + (randrange(1, 100, 1)/10000)  # 在相同值的情况下增加一个随机波动
