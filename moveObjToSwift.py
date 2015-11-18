from classes.UtilSwift import *
from classes.ConnectionGetter import *
import os
import sys
import subprocess

''' Was tested is working fine! '''
def howToUse():
     print ' ---------------------- How To Use -------------------------- '
     print '$python moveObjToSwift.py <user> <password> <path_to_object> <object_name> <container_name>'

def errorMessage():
    print ' ------------------ ERROR ---------------- '
    print ' wrong parameters! '
    print ' for help try : python moveObjToSwift.py --help'

MIN_NUM_ARGS = 6
HELP_ARGS = 2
EMPTY_ARGS = 1

if(len(sys.argv) == HELP_ARGS and sys.argv[1] == '--help'):
    howToUse()
    exit(0)

elif(len(sys.argv) == MIN_NUM_ARGS):
    user = sys.argv[1]
    key = sys.argv[2]
    path = sys.argv[3]
    object_name = sys.argv[4]
    container_name = sys.argv[5]

elif(len(sys.argv) != EMPTY_ARGS):
    errorMessage()
    exit(1)

else:
    user = raw_input('swift user: ')
    key = raw_input('swift key: ')
    path = raw_input('path to object: ')
    object_name = raw_input('object name: ')
    container_name = raw_input('container name: ')

connector = ConnectionGetter(user, key, 'project_name', 'project_id', 'openstack_IP')
swift = UtilSwift(connector.swift())
swift.storeFile(path, object_name, container_name)
