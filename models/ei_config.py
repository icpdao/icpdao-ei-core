class EiConfig:
    # 配对权重
    # 贡献者相同时，增加的权值，建议是负数
    invalid_same_c_rate = -10000

    # 配对权重
    # 相同的issue对，第两次配对时，第二个配对得到的总权重，可以为负数
    invalid_same_dup_rate = 0.1

    # 配对
    ei_p_size_weight = 100
    ei_p_label_weight = 0.9
    ei_p_reviewer_weight = 0.1

    # 匹配贡献者
    ei_pv_reviewer_weight = 15
    ei_pv_label_weight = 15

    def __init__(
        self,
        tmp_skip_voter_list,
        other_c_list,
        ei_p_size_weight_ratio=1,
        ei_p_label_weight_ratio=1,
        ei_p_reviewer_weight_ratio=1,
        ei_pv_reviewer_weight_ratio=1,
        ei_pv_label_weight_ratio=1,
        ):
        """
        # 这个列表中的用户不参与投票
        tmp_skip_voter_list = ['xxx']

        # 当投票者不够人数时，这个列表中的用户，作为额外的投票者
        other_c_list = ["georgeliuyu"]

        # 配对参数
        # size 接近的权重系数
        # 默认是 1 
        ei_p_size_weight_ratio

        # 配对参数
        # label 相同的权重系数
        # 默认是 1 
        ei_p_label_weight_ratio

        # 配对参数
        # reviewer 相同的权重系数
        # 默认是 1 
        ei_p_reviewer_weight_ratio

        # 匹配投票者
        # reviewer 相同的权重系数
        # 默认是 1 
        ei_pv_reviewer_weight_ratio

        # 匹配投票者
        # label 相同的权重系数
        # 默认是 1 
        ei_pv_label_weight_ratio
        """
        self.tmp_skip_voter_list = tmp_skip_voter_list
        self.other_c_list = other_c_list
        self.ei_p_size_weight_ratio = 1
        self.ei_p_label_weight_ratio = 1
        self.ei_p_reviewer_weight_ratio = 1
        self.ei_pv_reviewer_weight_ratio = 1
        self.ei_pv_label_weight_ratio = 1


default_config = EiConfig(
    tmp_skip_voter_list = ['user_xxx'],
    other_c_list = ["user_xxx"]
)
