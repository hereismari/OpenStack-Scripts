from classes.UtilSwift import *
from classes.ConnectionGetter import *
from classes.UtilSahara import *
from classes.Utilpasswordstone import *
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

MIN_NUM_ARGS = 4
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

parser = JsonParser('configuration.json')
user = parser.get('user')
project_name = parser.get('project_name')
project_id = parser.get('project_id')
main_ip = parser.get('main_ip')

output_container = 'output_container'
input_container = 'input_container'

if job_name == 'Job1':
    job_id = 'job1_id'
    map_output_key = 'map_output_key'
    map_output_value = 'map_output_value' #dont need the hadoop.org....
elif job_name == 'Job2':
    job_id = 'job2_id'
    map_output_key = 'map_output_key'
    map_output_value = 'map_output_value'
else:
    print 'Job doenst exists in the script'
    exit(1)

connector = ConnectionGetter(user, password, project_name, project_id, main_ip)

keystone_util = UtilKeystone(connector.keystone())
token_ref_id = passwordstone_util.getTokenRef(user, password, project_name).id
sahara_util = UtilSahara(connector.sahara(token_ref_id))

exec_date = time.strftime('%Y%m%d%H%M%S')

input_ds_name = 'input_' + file_name + '_' + exec_date
input_ds_utl =  'swift://' + input_container + '.sahara/' + file_name

output_ds_name = 'output_' + file_name + '_' + exec_date
output_ds_url =  'swift://' + output_container + '.sahara/' + output_ds_name

input_ds = sahara_util.createDataSource(input_ds_name, input_ds_url, 'swift', user, password)
output_ds = sahara_util.createDataSource(output_ds_name, output_ds_url, 'swift', user, password)

sahara_util.runMapReduceJob(job_name, job_id, cluster_id, map_output_key, map_output_value, input_ds.id, output_ds.id)
