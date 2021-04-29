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
        label_rate = 0.9  # label分类相同权值
        user_ability_rate = 1.5   # 相同技术要求的权值
        same_repo_rate = 0.2  # 相同repo的权值
        same_size_rate = 100  # size相似的权值
        same_reviewer_rate = 0.1  # 相同reviewer的权值
        invalid_same_c_rate = -10000   # 相同贡献者的权值，建议是负数
        invalid_same_dup_rate = 0.1  # 相同的issue对，出现两次，可以是负数
        type_same = 0.9  # 相同类型，比如全是 issue 或者全是 pr
        pair_user_ability_rate = 1   # issue对与人员的对应，技术要求的权值
        pair_reviewer_rate = 15  # issue对与人员的对应，是reviewer的权值
        reserved_word = ["ICP", "IN PROGRESS", "BUG"]
        have_ci_threshold = 0.8
        pair_reviewer_rate_list = { # issue对与人员的对应，是reviewer的权值
            "nancy919": {
                "ben7th": 15  # ben7th 作为 nancy919 的 reviewer 的权值
            }
        }
        coder_ability_list = {} # 下面的参数针对的是issue配对的参数
        coder_ability_list_for_reviewer = {} # 下面的参数针对的是pair和reviewer的配对
        tmp_skip_voter_list = ['xxx']
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
