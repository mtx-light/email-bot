import json

dative_dict = {}
with open('./email_bot/utils/dativ.txt', encoding='utf-8-sig') as f:
    lines = f.readlines()
for l in lines:
    t = l.strip().split("  ")
    dative_dict[int(t[0])] = t[1]

with open("./email_bot/entities/employee/mapping.json", "r") as f:
    mapping = json.load(f)


def find_id(name):
    for e in mapping['entities']:
        if e['cname'] == name:
            return int(e['id'])
    raise ValueError(f"Name {name} not found in mapping")


def get_dative(name):
    employee_id = find_id(name)
    return dative_dict[employee_id]
