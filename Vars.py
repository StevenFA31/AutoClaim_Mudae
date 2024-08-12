import json

def get_config(name):
    with open('config.json', 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)
    return config.get(name)