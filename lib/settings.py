from yaml import load
import argparse

parser = argparse.ArgumentParser(description='Facebook auto commenter')
parser.add_argument('configfile', metavar='N', type=argparse.FileType("r"), default="settings.yaml",
                    help='Config YAML')


args = parser.parse_args()

SETTINGS = load(args.configfile)

def get_settings():
    return SETTINGS