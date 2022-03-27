import json

to_json_list = []

with open('ban_word_list.txt', encoding='utf-8') as i:
    for line in i:
        l = line.lower().split('\n')[0]
        if l != '':
            to_json_list.append(l)

with open('ban_word_list.json', 'w', encoding='utf-8') as i:
    json.dump(to_json_list, i)