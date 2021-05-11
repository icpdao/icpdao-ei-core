class EiConfig:
    def __init__(
        self,
        label_rate,
        user_ability_rate,
        same_repo_rate,
        same_size_rate,
        same_reviewer_rate,
        invalid_same_c_rate,
        invalid_same_dup_rate,
        type_same,
        pair_user_ability_rate,
        pair_reviewer_rate,
        reserved_word,
        have_ci_threshold,
        pair_reviewer_rate_list,
        coder_ability_list,
        coder_ability_list_for_reviewer,
        tmp_skip_voter_list,
        other_c_list
        ):
        """
        # 配对权重
        # 配对时，双方拥有相同 lable 时，会增加配对的权重
        # 这个值代表每个 label 分类相同增加的权值
        label_rate = 0.9

        # 配对权重
        # 配对时，双方能力接近时，会增加配对的权重
        # 这个值代表能力接近时，权重增加的大小系数，值越大，双方能力接近的配对，得到的权重越大
        user_ability_rate = 1.5   # 相同技术要求的权值

        # 配对权重
        # repo 相同时，配对增加的权值
        same_repo_rate = 0.2

        # 配对权重
        # 这个值代表size接近时，权重增加的大小，值越大，size接近的配对，得到的权重越大
        same_size_rate = 100

        # 配对权重
        # reviewer 是 合并 PR 的人
        # reviewer 相同时，配对增加的权值
        same_reviewer_rate = 0.1

        # 配对权重
        # 贡献者相同时，增加的权值，建议是负数
        invalid_same_c_rate = -10000   

        # 配对权重
        # 相同的issue对，第两次配对时，第二个配对得到的总权重，可以为负数
        invalid_same_dup_rate = 0.1

        # 配对权重
        # 相同类型，比如双方全是 issue 或者全是 pr 时，增加的权重值
        type_same = 0.9

        # 匹配投票者权重
        # 根据 coder_ability_list_for_reviewer 查询每个投票者的投票能力，值越大，代表能力越大
        # 这个值代表 能力大的投票者，可以增加的权重大小系数
        pair_user_ability_rate = 1   # issue对与人员的对应，技术要求的权值

        # 匹配投票者权重
        # 如果投票者是配对中 ISSUE 的 REVIEWER 时，会增加权重
        # 这个值代表 增加的权重的默认系数
        # 如果 pair_reviewer_rate_list 中设置了，会按照 pair_reviewer_rate_list 的值
        pair_reviewer_rate = 15  # issue对与人员的对应，是reviewer的权值

        # 没有用到
        reserved_word = ["ICP", "IN PROGRESS", "BUG"]
        
        # 没有用到
        have_ci_threshold = 0.8

        # 匹配投票者权重
        # 如果投票者是配对中 ISSUE 的 REVIEWER 时，会增加权重
        # pair_reviewer_rate 代表默认增加的权重的系数
        # 也可以在这个配置里，单独对每一个人设置
        pair_reviewer_rate_list = {
            "nancy919": {
                "ben7th": 15  # ben7th 作为 nancy919 的 reviewer 的权值
            }
        }

        # 配对权重
        # 这个配置可以设置每个成员的能力只
        # 配对双方能力值越接近，获得的权重相对越高
        coder_ability_list = {
            "user_xxx":   0.9
        }

        # 匹配投票者权重
        # 根据 coder_ability_list_for_reviewer 查询每个投票者的投票能力，值越大，代表能力越大
        # 投票者的这个值如果大于配对中双方的值，增加的权重系数是 1， 否则是 0.5
        # TODO 这里感觉以前实现有BUG，需要确认
        coder_ability_list_for_reviewer = {
            "user_xxx":   0.9
        }

        # 这个列表中的用户不参与投票
        tmp_skip_voter_list = ['xxx']

        # 当投票者不够人数时，这个列表中的用户，作为额外的投票者
        other_c_list = ["georgeliuyu"]
        """
        self.label_rate = label_rate
        self.user_ability_rate = user_ability_rate
        self.same_repo_rate = same_repo_rate
        self.same_size_rate = same_size_rate
        self.same_reviewer_rate = same_reviewer_rate
        self.invalid_same_c_rate = invalid_same_c_rate
        self.invalid_same_dup_rate = invalid_same_dup_rate
        self.type_same = type_same
        self.pair_user_ability_rate = pair_user_ability_rate
        self.pair_reviewer_rate = pair_reviewer_rate
        self.reserved_word = reserved_word
        self.have_ci_threshold = have_ci_threshold
        self.pair_reviewer_rate_list = pair_reviewer_rate_list
        self.coder_ability_list = coder_ability_list
        self.coder_ability_list_for_reviewer = coder_ability_list_for_reviewer
        self.tmp_skip_voter_list = tmp_skip_voter_list
        self.other_c_list = other_c_list


default_config = EiConfig(
    label_rate = 0.9,
    user_ability_rate = 1.5,
    same_repo_rate = 0.2,
    same_size_rate = 100,
    same_reviewer_rate = 0.1,
    invalid_same_c_rate = -10000,
    invalid_same_dup_rate = 0.1,
    type_same = 0.9,
    pair_user_ability_rate = 1,
    pair_reviewer_rate = 15,
    reserved_word = ["ICP", "IN PROGRESS", "BUG"],
    have_ci_threshold = 0.8,
    pair_reviewer_rate_list = {
        "user_xxx": {
            "user_yyy": 15
        }
    },
    coder_ability_list = {
        "user_xxx":   0.9
    },
    coder_ability_list_for_reviewer = {
        "user_xxx":   0.9
    },
    tmp_skip_voter_list = ['user_xxx'],
    other_c_list = ["user_xxx"]
)
