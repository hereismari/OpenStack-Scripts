from classes.UtilSwift import *
from classes.ConnectionGetter import *
from classes.UtilSahara import *
from classes.UtilKeystone import *
from utils.JsonParser import *

import os
import sys
import subprocess
import time
import getpass

def howToUse():
    how_to_use = '$python runHadoopJob.py <job> <file_name> <cluster_id>'
    print 'How to use:'
    print how_to_use

def askForHelp():
    print 'Wrong parameters!'
    print '-----------------'
    print 'for help try: $python runHadoopJob.py --help'

MIN_NUM_ARGS = 5
EMPTY_ARGS = 1

if(len(sys.argv) == EMPTY_ARGS):
    job_name = raw_input('job name: ')
    file_name = raw_input('file name: ')
	cluster_id = raw_input('cluster id: ')
elif len(sys.argv) == MIN_NUM_ARGS:
    job_name = sys.argv[1]
    file_name = sys.argv[2]
	cluster_id = sys.argv[3]
else:
    askForHelp()
    exit(1)

password = getpass.getpass('password: ')
template_id = "" #TODO
image_id = "" #TODO

parser = JsonParser('configuration.json')
user = parser.get('user')
project_name = parser.get('project_name')
project_id = parser.get('project_id')
main_ip = parser.get('main_ip')
net_id = parser.get('net_id')

connector = ConnectionGetter(user, key, project_name, project_id, main_ip)

keystone_util = UtilKeystone(connector.keystone())
token_ref_id = keystone_util.getTokenRef(user, key, project_name).id
sahara_util = UtilSahara(connector.sahara(token_ref_id))

cluster_name = 'hadoop-create'
sahara_util.createClusterHadoop(cluster_name, image_id, template_id, net_id)

