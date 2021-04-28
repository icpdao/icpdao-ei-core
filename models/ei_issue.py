class EiIssue(object):
    def __init__(self, _type, org, repo, number, title, contributer, labels, size, reviewer, pr_org, pr_repo):
        """
        :param _type: issue | pull_request
        
        :param org: issue' github org
        :param repo: issue' github repo
        :param number: issue' github number

        :param title: github issue title
        :param contributer: issue contributer
        :param labels: label list
        
        :param size: issue size
        :param reviewer: pr reviewer

        :param pr_org: issue'pr org
        :param pr_repo: issue'pr repo
        """
        self.type = _type

        self.org = self.org
        self.repo = self.repo
        self.number = self.number

        self.title = title
        self.contributer = contributer
        self.labels = labels
        
        self.size = size
        self.reviewer = reviewer

        self.pr_org = pr_org
        self.pr_repo = pr_repo

        self.id = self.build_id()

    def build_id(self):
        return "{}/{}/{}".format(self.org, self.repo, self.number)

    def __eq__(self, obj):
        return self.id == self.id

    def to_dict(self):
        if self.type == 'issue':
            return {
                "title": self.title,
                "github_user_name": self.contributer,
                "type": "issue",
                "organization": self.org,
                "repository": self.repo,
                "number": self.number,
                "size": self.size,
                "reviewer": self.reviewer,
                "label": list(self.labels),
                "github_url": "https://github.com/{}/{}/issues/{}".format(
                    self.org,
                    self.repo,
                    self.number
                )
            }

        if self.type == 'pull_request':
            return {
                "github_user_name": self.contributer,
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
        return "{}---{}--{}--{}--{} ".format(self.id, 'I' if self.type == 'issue' else 'P', self.size, self.labels, self.contributer)
