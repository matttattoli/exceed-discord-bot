from os import path
import json

config_file = path.join(path.dirname(__file__), 'config.json')
privateconfig_file = path.join(path.dirname(__file__), 'privateconfig.json')

config = json.load(open(config_file, 'r'))
privateconfig = json.load(open(privateconfig_file, 'r'))
#  TODO: add removeaccess database. add live database
