from classes.UtilSwift import *
from classes.ConnectionGetter import *
from utils.JsonParser import *

import os
import sys
import subprocess
import getpass

''' Was tested is working fine! '''

def howToUse():
     print ' ---------------------- How To Use -------------------------- '
     print '$python getObjFromSwift.py <path_to_object> <object_name> <container_name>'

def errorMessage():
    print ' ------------------ ERROR ---------------- '
    print ' wrong parameters! '
    print ' for help try : python getObjFromSwift.py --help'

MIN_NUM_ARGS = 4
HELP_ARGS = 2
EMPTY_ARGS = 1

if(len(sys.argv) == MIN_NUM_ARGS):
    path = sys.argv[1]
    object_name = sys.argv[2]
    container_name = sys.argv[3]
elif(len(sys.argv) != EMPTY_ARGS):
    errorMessage()
    exit(1)
else:
    path = raw_input('path to object: ')
    object_name = raw_input('object name: ')
    container_name = raw_input('container name: ')

password = getpass.getpass('user password: ')

parser = JsonParser('configuration.json')
user = parser.get('user')
project_name = parser.get('project_name')
project_id = parser.get('project_id')
main_ip = parser.get('main_ip')

connector = ConnectionGetter(user, password, project_name, project_id, main_ip)
swift = UtilSwift(connector.swift())
swift.getFile(path, object_name, container_name)
