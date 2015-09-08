from classes.UtilSwift import *
from classes.ConnectionGetter import *
from classes.UtilSahara import *
from classes.UtilKeystone import *
import os
import sys
import subprocess
import time

def howToUse():
    how_to_use = '$python runHadoopJob.py <user> <password> <job> <file_name>'
    print 'How to use:'
    print how_to_use

def askForHelp():
    print 'Wrong parameters!'
    print '-----------------'
    print 'for help try: $python runHadoopJob.py --help'

MIN_NUM_ARGS = 5
EMPTY_ARGS = 1
HELP_ARGS = 2

if(len(sys.argv) == HELP_ARGS):
    howToUse()
    exit(0)
elif(len(sys.argv) == EMPTY_ARGS):
    user = raw_input('username: ')
    key = raw_input('password: ')
    job_name = raw_input('job name: ')
    file_name = raw_input('file name: ')
elif len(sys.argv) == MIN_NUM_ARGS:
    user = sys.argv[1]
    key = sys.argv[2]
    job_name = sys.argv[3]
    file_name = sys.argv[4]
else:
    askForHelp()
    exit(1)

project_name = 'project_name'
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
    howToUse()
    exit(1)

cluster_id = 'cluster_id'
project_id = 'project_id'

connector = ConnectionGetter(user, key, project_name, project_id, 'openstack_IP')

keystone_util = UtilKeystone(connector.keystone())
token_ref_id = keystone_util.getTokenRef(user, key, project_name).id
sahara_util = UtilSahara(connector.sahara(token_ref_id))

exec_date = time.strftime('%Y%m%d%H%M%S')
input_ds_name = 'input_' + file_name + '_' + exec_date
output_ds_name = 'output_' + file_name + '_' + exec_date
input_ds = sahara_util.createDataSource(input_ds_name, input_container, 'swift://' + input_container + '.sahara/' + file_name, user, key)
output_ds = sahara_util.createDataSource(output_ds_name, output_container, 'swift://' + output_container + '.sahara/' + output_ds_name, user, key)

sahara_util.runJob(job_name, job_id, cluster_id, map_output_key, map_output_value,
        input_ds.id, output_ds.id)

