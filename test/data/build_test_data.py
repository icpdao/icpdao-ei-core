import random
import json

user_count = 5
persion_size = [5, 10, 15, 20]
persion_issue_count = 5

persion_size_range = [8, 12]
persion_issue_range = [8, 12]

org_list = {
    'org_a':["repo_a", "repo_b"],
    'org_b':["repo_c", "repo_d"]
}

labels_info = {
    "repo_a": ["ICP_A"],
    "repo_b": ["ICP_B"],
    "repo_c": ["ICP_C"],
    "repo_d": ["ICP_D"]
}

number_data = {}

def get_number(org, repo):
    global number_data
    key = "{}_{}".format(org, repo)
    value = number_data.get(key, 0) + 1
    number_data[key] = value
    return value

result = []
user_name_list = []

for i in range(user_count):
    user_name = "user_{}".format(i)
    user_name_list.append(user_name)


for user_name in user_name_list:
    index = user_name_list.index(user_name)
    count = len(user_name_list)

    reviewer_index = (index+1) % count
    reviewer = user_name_list[reviewer_index]


    for size in persion_size:
        range_count = random.randint(persion_issue_count*persion_issue_range[0], persion_issue_count*persion_issue_range[1])
        range_count = int(range_count/10)
        for issue_index in range(range_count):
            range_size = random.randint(size*persion_size_range[0], size*persion_size_range[1])
            range_size = round(range_size/100, 1)

            _type = random.choice(['issue', 'pull_request'])
            org = random.choice(list(org_list.keys()))
            repo =  random.choice(org_list[org])
            
            repo_number = get_number(org, repo)

            labels = labels_info[repo]

            pr_org = random.choice(list(org_list.keys()))
            pr_repo = random.choice(org_list[pr_org])

            result.append({
                "type": _type,
                "org": org,
                "repo": repo,
                "number": repo_number,
                "title": "{} | {} | {} | {}".format(_type, org, repo, repo_number),
                "contributer": user_name,
                "labels": labels,
                "size": range_size,
                "reviewer": reviewer,
                "pr_org": pr_org,
                "pr_repo": pr_repo 
            })

json.dump(result, open('./data.json', 'w'), ensure_ascii=False, indent=True)
