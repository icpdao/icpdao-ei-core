class EiIssuePair:
    def __init__(self, ei_issue_1, ei_issue_2):
        self.left = ei_issue_1
        self.right = ei_issue_2
        self.id = self.build_id()
        self.c = None

    def build_id(self):
        return "|".join(sorted([self.left.id, self.right.id]))
    
    def pair_hash(self):
        return "|".join([self.left.id, self.right.id])

    def other_pair_hash(self):
        return "|".join([self.right.id, self.left.id])

    def to_dict(self):
        return {
            "left": self.left.to_dict(),
            "right": self.right.to_dict(),
            "user": self.c.to_dict() if self.c else {}
        }

    def debug_info(self):
        return "{} <===>  {}   user:{}".format(
            self.left.debug_info(),
            self.right.debug_info(),
            self.c.name if self.c else ""
        )
