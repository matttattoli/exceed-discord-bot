from os import path
import json

config_file = path.join(path.dirname(__file__), 'config.json')
with open(config_file, 'r') as config_json:
    config = json.load(config_json)

privateconfig_file = path.join(path.dirname(__file__), 'privateconfig.json')
with open(config_file, 'r') as privateconfig_json:
    privateconfig = json.load(privateconfig_json)