import configparser
import os

def create_config(config_file=None):
    parser = configparser.SafeConfigParser()
    parser.optionxform = str
    parser.read(config_file)
    return parser

config_file = os.path.join(os.path.join(os.path.dirname(__file__)), 'B000_Config.ini')
Config = create_config(config_file)

anritsu_file = os.path.join(os.path.join(os.path.dirname(__file__)), 'Anritsu_MT8870A.ini')
MT8870A_Config = create_config(anritsu_file)