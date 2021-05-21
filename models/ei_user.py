class EiUser(object):
    def __init__(self, name, labels):
        self.name = name
        self.labels = labels

        self.label_info = self.parse_labels(labels)

        self.vote_count = 0

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

    def to_dict(self):
        return {
            "name": self.name,
            "labels": self.labels
        }
