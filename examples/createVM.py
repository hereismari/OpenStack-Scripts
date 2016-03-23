from classes.ConnectionGetter import *
from classes.UtilNova import *
from classes.UtilKeystone import *
from utils.JsonParser import *

import os
import sys
import subprocess
import time
import getpass

MIN_NUM_ARGS = 4
EMPTY_ARGS = 1
HELP_ARGS = 2

if(len(sys.argv) == EMPTY_ARGS):
    instance_name = raw_input('VM name: ')
    image_name = raw_input('image name: ')
    flavor_name = raw_input('flavor name: ')
elif len(sys.argv) == MIN_NUM_ARGS:
    instance_name = sys.argv[1]
    image_name = sys.argv[2]
    flavor_name = sys.argv[3]
else:
    exit(1)

username = raw_input('username: ')
password = getpass.getpass('password: ')

parser = JsonParser('configuration.json')
project_name = parser.get('project_name')
project_id = parser.get('project_id')
main_ip = parser.get('main_ip')

network_name = 'my-net'
key_name = 'your-key'
post_creation_file = '<OPTIONAL>'

connector = ConnectionGetter(username, password, project_name, project_id, main_ip)

nova_util = UtilNova(connector.nova())
nova_util.createInstance(instance_name, image_name, flavor_name, network_name, key_name, post_creation_file)

