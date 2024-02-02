import csv
import json


from law_articles_extractor import count_tokens

MAX_TOKENS = 1500
csv_file_path = '../data/csv/pytania_edustrefa-6.csv'


def load_csv():
    KEYS = ['id', 'name1', 'nb', 'name2', 'date', 'topic', 'question', 'answer']

    data_dict_list = []

    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data_dict_list.append(dict(zip(KEYS, row)))
    print(f'Data len: {len(data_dict_list)}')
    print(data_dict_list[501])
    # i=0
    # longer_entries = []
    # for d in data_dict_list:
    #     tokens_q = count_tokens(d['question'])
    #     tokens_a = count_tokens(d['answer'])
    #
    #     if tokens_q + tokens_a > MAX_TOKENS:#206979 or tokens_a > MAX_TOKENS:
    #         i+=1
    #         print('----------------------------------------------------------')
    #         idd = d['id']
    #         print(f'{i}. {idd} num tokens: {tokens_a + tokens_q}')
    #         longer_entries.append(d)
    #
    # with open('longer_than_2k.json', 'w+', encoding='utf-8') as f:
    #     json.dump(longer_entries, f)


if __name__ == '__main__':
    load_csv()