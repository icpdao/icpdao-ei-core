class EiIssue(object):
    def __init__(self, id, _type, org, repo, number, title, contributer, labels, size, reviewer, pr_org, pr_repo):
        """
        :param _type: issue | pull_request
        
        :param org: issue' github org
        :param repo: issue' github repo
        :param number: issue' github number

        :param title: github issue title
        :param contributer: issue contributer  EiUser type
        :param labels: label list
        
        :param size: issue size
        :param reviewer: pr reviewer  EiUser type

        :param pr_org: issue'pr org
        :param pr_repo: issue'pr repo
        """
        self.id = id
        self.type = _type

        self.org = org
        self.repo = repo
        self.number = number

        self.title = title
        self.contributer = contributer
        self.labels = set(labels)
        self.label_info = self.parse_labels(labels)

        self.size = size
        self.reviewer = reviewer

        self.pr_org = pr_org
        self.pr_repo = pr_repo


    # lables ['XXX_0.1', 'YYY', 'ZZZ_D']
    # result {
    #   'XXX_0.1':0.1,
    #   'YYY':  1,
    #   'ZZZ_D': 1
    # }
    def parse_labels(self, labels):
        result = {}
        for label in labels:
            arr = label.split('_')
            if len(arr) == 1:
                result[label] = 1
                continue
            last = arr[-1]
            try:
                number = float(last)
                new_label = "_".join(arr[0:-1])
                result[new_label] = number
                continue
            except:
                result[label] = 1
                continue

        return result

    def __eq__(self, obj):
        return self.id == self.id

    def to_dict(self):
        if self.type == 'issue':
            return {
                "id": self.id,
                "title": self.title,
                "github_user_name": self.contributer.name,
                "type": "issue",
                "organization": self.org,
                "repository": self.repo,
                "number": self.number,
                "size": self.size,
                "reviewer": self.reviewer.name,
                "label": list(self.labels),
                "github_url": "https://github.com/{}/{}/issues/{}".format(
                    self.org,
                    self.repo,
                    self.number
                )
            }

        if self.type == 'pull_request':
            return {
                "id": self.id,
                "github_user_name": self.contributer.name,
                "type": "pull_request",
                "organization": self.org,
                "repository": self.repo,
                "number": self.number,
                "size": self.size,
                "title": self.title,
                "label": list(self.labels),
                "github_url": "https://github.com/{}/{}/pull/{}".format(
                    self.org,
                    self.repo,
                    self.number
                )
            }

    def debug_info(self):
        return "{}---{}--{}--{}--{} ".format(self.id, 'I' if self.type == 'issue' else 'P', self.size, self.labels, self.contributer.name)
