import json


def load_json(filepath):
    with open(filepath, encoding='utf-8') as f:
        data_dicts_list = json.load(f)
        print(len(data_dicts_list))


if __name__ == '__main__':
    load_json("../data/diaries_processed.json")
